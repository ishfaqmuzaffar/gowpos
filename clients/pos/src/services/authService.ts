import { apiClient } from './apiClient';
import type { UserProfile } from '../types';

interface AuthResponse {
  token: string;
  user: UserProfile;
}

export const login = (email: string, password: string) =>
  apiClient<AuthResponse>('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password })
  });

export const register = (payload: { email: string; password: string; displayName: string }) =>
  apiClient<AuthResponse>('/auth/register', {
    method: 'POST',
    body: JSON.stringify(payload)
  });
