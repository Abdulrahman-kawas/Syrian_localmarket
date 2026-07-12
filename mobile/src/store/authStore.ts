import { create } from 'zustand';
import * as SecureStore from 'expo-secure-store';
import { api } from '../api/client';

const TOKEN_KEY = 'lm_token';

interface User {
  id: string;
  email: string | null;
  phone: string;
  role: 'consumer' | 'seller' | 'admin';
  verificationStatus: 'pending' | 'verified' | 'failed';
}

interface ApiUser {
  id: string;
  email: string | null;
  phone: string;
  role: 'consumer' | 'seller' | 'admin';
  verification_status: 'pending' | 'verified' | 'failed';
}

function mapUser(u: ApiUser): User {
  return {
    id: u.id,
    email: u.email,
    phone: u.phone,
    role: u.role,
    verificationStatus: u.verification_status,
  };
}

interface SignupInput {
  email: string;
  phone: string;
  password: string;
  role: 'consumer' | 'seller';
  verificationMethod: 'email' | 'whatsapp';
}

interface AuthState {
  user: User | null;
  token: string | null;
  hydrated: boolean;
  isLoading: boolean;
  error: string | null;
  hydrate: () => Promise<void>;
  login: (emailOrPhone: string, password: string) => Promise<void>;
  signup: (data: SignupInput) => Promise<void>;
  verify: (emailOrPhone: string, code: string) => Promise<void>;
  logout: () => Promise<void>;
  setUser: (user: User | null) => void;
}

function isEmail(value: string): boolean {
  return value.includes('@');
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  hydrated: false,
  isLoading: false,
  error: null,

  hydrate: async () => {
    try {
      const token = await SecureStore.getItemAsync(TOKEN_KEY);
      if (token) {
        api.setToken(token);
        set({ token });
      }
    } finally {
      set({ hydrated: true });
    }
  },

  login: async (emailOrPhone, password) => {
    set({ isLoading: true, error: null });
    try {
      const body = isEmail(emailOrPhone)
        ? { email: emailOrPhone, password }
        : { phone: emailOrPhone, password };
      const res = await api.post<{ access_token: string; user: ApiUser }>('/auth/login', body);
      api.setToken(res.access_token);
      await SecureStore.setItemAsync(TOKEN_KEY, res.access_token);
      set({ user: mapUser(res.user), token: res.access_token, isLoading: false });
    } catch (err) {
      set({ error: 'Login failed', isLoading: false });
      throw err;
    }
  },

  signup: async (data) => {
    set({ isLoading: true, error: null });
    try {
      await api.post('/auth/signup', {
        email: data.email,
        phone: data.phone,
        password: data.password,
        role: data.role,
        verification_method: data.verificationMethod,
      });
      set({ isLoading: false });
    } catch (err) {
      set({ error: 'Signup failed', isLoading: false });
      throw err;
    }
  },

  verify: async (emailOrPhone, code) => {
    set({ isLoading: true, error: null });
    try {
      const body = isEmail(emailOrPhone) ? { email: emailOrPhone, code } : { phone: emailOrPhone, code };
      const res = await api.post<{ access_token: string; user: ApiUser }>('/auth/verify', body);
      api.setToken(res.access_token);
      await SecureStore.setItemAsync(TOKEN_KEY, res.access_token);
      set({ user: mapUser(res.user), token: res.access_token, isLoading: false });
    } catch (err) {
      set({ error: 'Verification failed', isLoading: false });
      throw err;
    }
  },

  logout: async () => {
    api.setToken(null);
    await SecureStore.deleteItemAsync(TOKEN_KEY);
    set({ user: null, token: null });
  },

  setUser: (user) => set({ user }),
}));
