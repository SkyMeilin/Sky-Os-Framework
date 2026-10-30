-- ============================================================================
-- SkyOS Core: Revisionssicheres PostgreSQL WORM-Ledger (Audit Trail)
-- Compliance: BSI § 8a BSIG & ISO/IEC 27037
-- Architecture: SHA-256 Hashverkettung + Trigger-basierter Schreibschutz
-- ============================================================================

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 1. Haupt-Tabelle für den WORM Audit Log
CREATE TABLE IF NOT EXISTS audit_worm_ledger (
    entry_id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    actor TEXT NOT NULL,
    verb TEXT NOT NULL CHECK (verb IN ('SEARCH', 'RESOLVE', 'PREVIEW', 'HUMAN_GATE', 'EXECUTE', 'VERIFY')),
    resource_id TEXT NOT NULL,
    payload_hash VARCHAR(64) NOT NULL,
    previous_hash VARCHAR(64) NOT NULL,
    current_hash VARCHAR(64) NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Index für performante Abfragen & Verifizierungen
CREATE INDEX IF NOT EXISTS idx_worm_ledger_created_at ON audit_worm_ledger (created_at);
CREATE INDEX IF NOT EXISTS idx_worm_ledger_verb ON audit_worm_ledger (verb);

-- 2. Trigger-Funktion: Strikter Schutz gegen UPDATE und DELETE (WORM-Prinzip)
CREATE OR REPLACE FUNCTION fn_reject_audit_tampering()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'WORM Ledger Compliance Violation: UPDATE or DELETE operations are strictly prohibited on table audit_worm_ledger [BSI § 8a BSIG]. Action attempted by user: %', CURRENT_USER
        USING ERRCODE = '55000'; -- object_not_in_prerequisite_state
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger für UPDATE und DELETE binden
DROP TRIGGER IF EXISTS trg_prevent_update ON audit_worm_ledger;
CREATE TRIGGER trg_prevent_update
BEFORE UPDATE ON audit_worm_ledger
FOR EACH ROW
EXECUTE FUNCTION fn_reject_audit_tampering();

DROP TRIGGER IF EXISTS trg_prevent_delete ON audit_worm_ledger;
CREATE TRIGGER trg_prevent_delete
BEFORE DELETE ON audit_worm_ledger
FOR EACH ROW
EXECUTE FUNCTION fn_reject_audit_tampering();

-- 3. Trigger-Funktion: Automatische SHA-256 Hashverkettung vor jedem INSERT
CREATE OR REPLACE FUNCTION fn_calculate_worm_hash()
RETURNS TRIGGER AS $$
DECLARE
    last_hash VARCHAR(64);
    genesis_seed CONSTANT VARCHAR(64) := '0000000000000000000000000000000000000000000000000000000000000000';
    hash_payload TEXT;
BEGIN
    -- Holen des Hash-Werts des vorherigen Eintrags
    SELECT current_hash INTO last_hash
    FROM audit_worm_ledger
    ORDER BY entry_id DESC
    LIMIT 1;

    -- Falls erster Eintrag (Genesis)
    IF last_hash IS NULL THEN
        last_hash := genesis_seed;
    END IF;

    NEW.previous_hash := last_hash;

    -- Zusammensetzen des zu hashenden Strings
    hash_payload := COALESCE(NEW.previous_hash, '') || '|' ||
                    TO_CHAR(NEW.created_at AT TIME ZONE 'UTC', 'YYYY-MM-DD"T"HH24:MI:SS.US"Z"') || '|' ||
                    COALESCE(NEW.actor, '') || '|' ||
                    COALESCE(NEW.verb, '') || '|' ||
                    COALESCE(NEW.resource_id, '') || '|' ||
                    COALESCE(NEW.payload_hash, '');

    -- Berechnung des SHA-256 Hashes
    NEW.current_hash := encode(digest(hash_payload, 'sha256'), 'hex');

    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger für automatische Hashberechnung vor INSERT binden
DROP TRIGGER IF EXISTS trg_calculate_worm_hash ON audit_worm_ledger;
CREATE TRIGGER trg_calculate_worm_hash
BEFORE INSERT ON audit_worm_ledger
FOR EACH ROW
EXECUTE FUNCTION fn_calculate_worm_hash();

-- 4. Audit-Integritätsprüfungs-Funktion (Prüfung der gesamten Kette)
CREATE OR REPLACE FUNCTION fn_verify_worm_ledger_integrity()
RETURNS TABLE (
    total_records BIGINT,
    is_valid BOOLEAN,
    corrupted_entry_id BIGINT,
    error_reason TEXT
) AS $$
DECLARE
    rec RECORD;
    prev_h VARCHAR(64) := '0000000000000000000000000000000000000000000000000000000000000000';
    calc_h VARCHAR(64);
    h_payload TEXT;
    record_count BIGINT := 0;
BEGIN
    FOR rec IN SELECT * FROM audit_worm_ledger ORDER BY entry_id ASC LOOP
        record_count := record_count + 1;
        
        -- Prüfe Vorläufer-Hash
        IF rec.previous_hash <> prev_h THEN
            RETURN QUERY SELECT record_count, FALSE, rec.entry_id, 'Broken previous_hash link detected.'::TEXT;
            RETURN;
        END IF;

        -- Rekonstruiere Hash
        h_payload := COALESCE(rec.previous_hash, '') || '|' ||
                     TO_CHAR(rec.created_at AT TIME ZONE 'UTC', 'YYYY-MM-DD"T"HH24:MI:SS.US"Z"') || '|' ||
                     COALESCE(rec.actor, '') || '|' ||
                     COALESCE(rec.verb, '') || '|' ||
                     COALESCE(rec.resource_id, '') || '|' ||
                     COALESCE(rec.payload_hash, '');
        
        calc_h := encode(digest(h_payload, 'sha256'), 'hex');

        IF rec.current_hash <> calc_h THEN
            RETURN QUERY SELECT record_count, FALSE, rec.entry_id, 'Hash mismatch detected.'::TEXT;
            RETURN;
        END IF;

        prev_h := rec.current_hash;
    END LOOP;

    RETURN QUERY SELECT record_count, TRUE, NULL::BIGINT, 'Ledger integrity verified successfully.'::TEXT;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
