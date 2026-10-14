const API_BASE = window.location.port === '5173' ? 'http://127.0.0.1:8000/api' : '/api';

export async function fetchHealth() {
  const res = await fetch(`${API_BASE}/health`);
  return res.json();
}

export async function fetchInitialGreeting(language = 'en') {
  const res = await fetch(`${API_BASE}/initial-greeting?language=${language}`);
  return res.json();
}

export async function sendChatMessage(messages, apiKey = null, language = 'en') {
  const res = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      messages,
      api_key: apiKey || null,
      language
    })
  });
  return res.json();
}

export async function fetchLoans(filters = {}) {
  const params = new URLSearchParams();
  if (filters.destination) params.append('destination', filters.destination);
  if (filters.amount) params.append('amount', filters.amount);
  if (filters.collateral_free !== undefined) params.append('collateral_free', filters.collateral_free);
  if (filters.category) params.append('category', filters.category);

  const res = await fetch(`${API_BASE}/loans?${params.toString()}`);
  return res.json();
}

export async function fetchSchemes() {
  const res = await fetch(`${API_BASE}/schemes`);
  return res.json();
}

export async function calculateEmi(payload) {
  const res = await fetch(`${API_BASE}/calculate-emi`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  return res.json();
}

export async function checkEligibility(payload) {
  const res = await fetch(`${API_BASE}/eligibility`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  return res.json();
}

export async function fetchDocumentChecklist(payload) {
  const res = await fetch(`${API_BASE}/documents`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  return res.json();
}
