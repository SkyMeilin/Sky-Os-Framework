(globalThis["TURBOPACK"] || (globalThis["TURBOPACK"] = [])).push([typeof document === "object" ? document.currentScript : undefined,
"[turbopack]/shared/module-cache.ts [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "cache",
    ()=>cache
]);
'use turbopack: no side effects';
const moduleCache = __turbopack_context__.c;
/**
 * Property keys always reach a `Proxy` trap as strings, but `ModuleId` is
 * `string | number` and the id kind is fixed for a build: either every id is a
 * number or every id is a string. Detect this by testing our own id.
 */ const idsAreNumeric = typeof __turbopack_context__.m.id === 'number';
// Coerce a string object propty to a ModuleId so it can match the cache.
function toKey(key) {
    if (!idsAreNumeric) return key;
    // A non-canonical spelling (`"0123"`, `"1e3"`, `" 1"`) is not any module's
    // id, so leave it as a string: it will simply miss, as it would have against
    // the object cache.  Without this "1x" would coerce to 1 which might match a module, incorrectly
    const numeric = Number(key);
    return String(numeric) === key ? numeric : key;
}
const cache = new Proxy(// Use an empty object as the 'target' so we can implement ownKeys
{}, {
    get (_target, key) {
        if (typeof key !== 'string') return undefined;
        return moduleCache.get(toKey(key));
    },
    set (_target, key, value) {
        if (typeof key !== 'string') return false;
        moduleCache.set(toKey(key), value);
        return true;
    },
    has (_target, key) {
        return typeof key === 'string' && moduleCache.has(toKey(key));
    },
    deleteProperty (_target, key) {
        if (typeof key !== 'string') return false;
        moduleCache.delete(toKey(key));
        return true;
    },
    ownKeys () {
        return Array.from(moduleCache.keys(), String);
    },
    // `ownKeys` alone is not enough: `Object.keys()` filters by enumerability, so
    // it invokes this trap for every key returned above.
    getOwnPropertyDescriptor (_target, key) {
        if (typeof key !== 'string') return undefined;
        const id = toKey(key);
        if (!moduleCache.has(id)) return undefined;
        return {
            value: moduleCache.get(id),
            writable: true,
            enumerable: true,
            configurable: true
        };
    }
});
}),
]);

//# sourceMappingURL=%5Bturbopack%5D_shared_module-cache_ts_1tsb92xtq_skk._.js.map