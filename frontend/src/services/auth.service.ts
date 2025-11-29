import { apiClient } from './api';
import type { User, AuthTokens, LoginCredentials, RegisterData } from '@/types';

export const authService = {
    async register(data: RegisterData): Promise<User> {
        const response = await apiClient.post<User>('/api/v1/auth/register', data);
        return response.data;
    },

    async login(credentials: LoginCredentials): Promise<AuthTokens> {
        const response = await apiClient.post<AuthTokens>('/api/v1/auth/login', credentials);
        const tokens = response.data;

        // Store tokens
        localStorage.setItem('access_token', tokens.access_token);
        localStorage.setItem('refresh_token', tokens.refresh_token);

        return tokens;
    },

    async logout(): Promise<void> {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
    },

    async getCurrentUser(): Promise<User> {
        const response = await apiClient.get<User>('/api/v1/users/me');
        return response.data;
    },

    isAuthenticated(): boolean {
        return !!localStorage.getItem('access_token');
    },
};
