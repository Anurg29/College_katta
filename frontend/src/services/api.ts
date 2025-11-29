import axios, { AxiosInstance, AxiosError } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class ApiClient {
    private client: AxiosInstance;

    constructor() {
        this.client = axios.create({
            baseURL: API_BASE_URL,
            headers: {
                'Content-Type': 'application/json',
            },
        });

        // Request interceptor to add auth token
        this.client.interceptors.request.use(
            (config) => {
                const token = localStorage.getItem('access_token');
                if (token) {
                    config.headers.Authorization = `Bearer ${token}`;
                }
                return config;
            },
            (error) => Promise.reject(error)
        );

        // Response interceptor to handle token refresh
        this.client.interceptors.response.use(
            (response) => response,
            async (error: AxiosError) => {
                const originalRequest = error.config as any;

                if (error.response?.status === 401 && !originalRequest._retry) {
                    originalRequest._retry = true;

                    try {
                        const refreshToken = localStorage.getItem('refresh_token');
                        if (refreshToken) {
                            const response = await axios.post(`${API_BASE_URL}/api/v1/auth/refresh`, {
                                refresh_token: refreshToken,
                            });

                            const { access_token, refresh_token } = response.data;
                            localStorage.setItem('access_token', access_token);
                            localStorage.setItem('refresh_token', refresh_token);

                            originalRequest.headers.Authorization = `Bearer ${access_token}`;
                            return this.client(originalRequest);
                        }
                    } catch (refreshError) {
                        localStorage.removeItem('access_token');
                        localStorage.removeItem('refresh_token');
                        window.location.href = '/login';
                        return Promise.reject(refreshError);
                    }
                }

                return Promise.reject(error);
            }
        );
    }

    get<T>(url: string, params?: any) {
        return this.client.get<T>(url, { params });
    }

    post<T>(url: string, data?: any) {
        return this.client.post<T>(url, data);
    }

    put<T>(url: string, data?: any) {
        return this.client.put<T>(url, data);
    }

    delete<T>(url: string) {
        return this.client.delete<T>(url);
    }
}

export const apiClient = new ApiClient();
