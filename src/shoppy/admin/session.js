/**
 * Admin session (frontend only). No credentials live in this file.
 * Real sign-in posts to the store service; "preview" mode is a clearly simulated local session.
 */
import { API_BASE } from '../services/api';
const KEY = 'agentcart_admin_session';

export function getAdminSession() {
  if (typeof window === 'undefined') return null;
  try { return JSON.parse(sessionStorage.getItem(KEY) || 'null'); } catch { return null; }
}
export function startPreviewSession() {
  const s = { mode: 'preview', role: 'admin', name: 'Preview admin' };
  sessionStorage.setItem(KEY, JSON.stringify(s));
  window.dispatchEvent(new Event('agentcart-admin'));
  return s;
}
export async function signInAdmin(email, password) {
  if (!API_BASE) throw new Error('Admin sign-in needs the store service, which is not connected yet.');
  const res = await fetch(`${API_BASE}/api/admin/login`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email, password }) });
  if (!res.ok) { const e = await res.json().catch(() => ({})); throw new Error(e.detail || 'Sign-in failed. Check your email and password.'); }
  const data = await res.json();
  const s = { mode: 'live', role: data.role || 'staff', name: data.name || email, token: data.access_token };
  sessionStorage.setItem(KEY, JSON.stringify(s));
  window.dispatchEvent(new Event('agentcart-admin'));
  return s;
}
export function signOutAdmin() {
  sessionStorage.removeItem(KEY);
  window.dispatchEvent(new Event('agentcart-admin'));
}
