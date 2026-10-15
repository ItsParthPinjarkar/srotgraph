"use client";

import { useEffect, useState } from "react";

interface HealthStatus {
  status: string;
  version: string;
  environment: string;
  timestamp: string;
}

export default function Home() {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/health")
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP ${res.status}`);
        }
        return res.json();
      })
      .then(setHealth)
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);

  return (
    <main style={{ padding: "2rem", maxWidth: "600px", margin: "0 auto" }}>
      <h1 style={{ fontSize: "1.5rem", marginBottom: "1rem" }}>
        SrotGraph Status
      </h1>

      {loading && <p>Loading...</p>}

      {error && (
        <div style={{ color: "red", marginBottom: "1rem" }}>
          <p>Failed to connect to API: {error}</p>
          <p>Make sure the backend is running on <code>localhost:8000</code></p>
        </div>
      )}

      {health && (
        <div
          style={{
            border: "1px solid #ccc",
            borderRadius: "8px",
            padding: "1rem",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
            <span
              style={{
                width: "12px",
                height: "12px",
                borderRadius: "50%",
                backgroundColor:
                  health.status === "ok" ? "green" : "red",
              }}
            />
            <span style={{ fontWeight: "bold", fontSize: "1.1rem" }}>
              {health.status === "ok" ? "System Online" : health.status}
            </span>
          </div>

          <dl style={{ marginTop: "1rem", display: "grid", gap: "0.5rem" }}>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <dt>Version</dt>
              <dd>{health.version}</dd>
            </div>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <dt>Environment</dt>
              <dd>{health.environment}</dd>
            </div>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <dt>Timestamp</dt>
              <dd>{new Date(health.timestamp).toLocaleString()}</dd>
            </div>
          </dl>

          <div style={{ marginTop: "1rem" }}>
            <a
              href="/api/health"
              target="_blank"
              rel="noopener noreferrer"
              style={{
                color: "#0066cc",
                textDecoration: "none",
              }}
            >
              View raw health endpoint →
            </a>
          </div>
        </div>
      )}

      <footer
        style={{
          marginTop: "2rem",
          paddingTop: "1rem",
          borderTop: "1px solid #eee",
          fontSize: "0.875rem",
          color: "#666",
        }}
      >
        <p>SrotGraph v0.1.0 — Evidence-Preserving Intelligence System</p>
      </footer>
    </main>
  );
}
