// Use /api in dev (Vite proxies to backend); or full URL when set (e.g. Docker)
const API_BASE = import.meta.env.VITE_API_BASE_URL ?? '/api';

export async function analyzeClaim(claimRequest) {
  const res = await fetch(`${API_BASE}/claims/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(claimRequest),
  });
  if (!res.ok) {
    const text = await res.text();
    let msg = text;
    try {
      const json = JSON.parse(text);
      msg = json.message || json.error || text;
    } catch (_) {}
    throw new Error(msg || `HTTP ${res.status}`);
  }
  return res.json();
}
