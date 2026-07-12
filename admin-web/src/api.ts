// Thin API client for the admin back-office. Talks to the FastAPI backend.

const API_URL: string =
  (import.meta.env.VITE_API_URL as string) || 'http://localhost:8000/api/v1';

const TOKEN_KEY = 'lm_admin_token';

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string | null): void {
  if (token) localStorage.setItem(TOKEN_KEY, token);
  else localStorage.removeItem(TOKEN_KEY);
}

export interface ApiError {
  code: string;
  message: string;
}

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(init.headers as Record<string, string>),
  };
  const token = getToken();
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(`${API_URL}${path}`, { ...init, headers });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    const err: ApiError = body?.error || { code: 'ERROR', message: 'Request failed' };
    throw new Error(err.message);
  }
  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}

export const api = {
  get: <T>(path: string) => request<T>(path),
  post: <T>(path: string, body: unknown) =>
    request<T>(path, { method: 'POST', body: JSON.stringify(body) }),
  put: <T>(path: string, body: unknown) =>
    request<T>(path, { method: 'PUT', body: JSON.stringify(body) }),
};

// --- Domain types -----------------------------------------------------------
export interface LoginResponse {
  access_token: string;
  user: { id: string; role: string };
}

export interface Complaint {
  id: string;
  reporter_id: string;
  target_id: string;
  target_type: string;
  listing_id: string | null;
  reason: string;
  status: string;
  created_at: string;
}

export interface AdminUser {
  id: string;
  email: string | null;
  phone: string;
  role: string;
  verification_status: string;
  reputation_score: string;
  is_suspended: boolean;
  created_at: string;
}

export interface AdminActionRow {
  id: string;
  admin_id: string;
  action_type: string;
  target_id: string;
  target_type: string;
  notes: string | null;
  created_at: string;
}
