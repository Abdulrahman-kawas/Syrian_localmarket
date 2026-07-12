import { createContext, useContext, useState, type ReactNode } from 'react';
import { api, getToken, setToken, type LoginResponse } from './api';

interface AuthState {
  isAuthed: boolean;
  role: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [role, setRole] = useState<string | null>(null);
  const [isAuthed, setIsAuthed] = useState<boolean>(Boolean(getToken()));

  async function login(email: string, password: string): Promise<void> {
    const res = await api.post<LoginResponse>('/auth/login', { email, password });
    if (res.user.role !== 'admin') {
      throw new Error('This account is not an administrator');
    }
    setToken(res.access_token);
    setRole(res.user.role);
    setIsAuthed(true);
  }

  function logout(): void {
    setToken(null);
    setRole(null);
    setIsAuthed(false);
  }

  return (
    <AuthContext.Provider value={{ isAuthed, role, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthState {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}
