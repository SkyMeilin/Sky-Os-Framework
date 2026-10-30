import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const API_BASE = '/api/v1';

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    const token = localStorage.getItem('skyos_token');
    if (token) {
      try {
        const res = await fetch(`${API_BASE}/auth/github/me`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
          const data = await res.json();
          setUser(data);
        }
      } catch (e) {
        console.error('Auth check failed', e);
      }
    }
    setLoading(false);
  };

  const handleLogin = async () => {
    const res = await fetch(`${API_BASE}/auth/github/login`);
    const data = await res.json();
    window.location.href = data.authorization_url;
  };

  const handleLogout = () => {
    localStorage.removeItem('skyos_token');
    setUser(null);
  };

  if (loading) {
    return <div className="loading">Loading SkyOS Open Core...</div>;
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>🛡️ SkyOS Open Core</h1>
        <nav>
          {user ? (
            <>
              <span>Willkommen, {user.username}!</span>
              <button onClick={handleLogout}>Logout</button>
            </>
          ) : (
            <button onClick={handleLogin}>Login mit GitHub</button>
          )}
        </nav>
      </header>

      <main>
        <section className="features">
          <div className="feature-card">
            <h2>📄 OCR-Bescheid-Scanner</h2>
            <p>Scannen und Parsen von Behördenbescheiden</p>
            {user && <a href="/scanner">Zum Scanner</a>}
          </div>
          <div className="feature-card">
            <h2>🚨 Notfall-Leitfäden</h2>
            <p>OBG NRW §14 Notfallgenehmigungen</p>
            {user && <a href="/emergency">Zu den Leitfäden</a>}
          </div>
          <div className="feature-card">
            <h2>🔒 DSGVO-Anonymizer</h2>
            <p>Privacy-by-Design Telemetry</p>
            {user && <a href="/anonymizer">Zum Anonymizer</a>}
          </div>
        </section>
      </main>

      <footer>
        <p>SkyOS Open Core &copy; 2025 Pascal Weidermann, Hückelhoven</p>
      </footer>
    </div>
  );
}

export default App;
