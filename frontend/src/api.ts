export const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'
export const WS_BASE = import.meta.env.VITE_WS_BASE || 'ws://localhost:8000'

export async function getSummary(){ const r=await fetch(`${API_BASE}/api/summary`); return r.json() }
export async function getTracks(){ const r=await fetch(`${API_BASE}/api/tracks`); return r.json() }
export async function getAnalytics(){ const r=await fetch(`${API_BASE}/api/analytics`); return r.json() }
