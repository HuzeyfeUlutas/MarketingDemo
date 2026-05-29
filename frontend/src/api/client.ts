import axios, { AxiosError, InternalAxiosRequestConfig } from "axios";

import { tokenStorage } from "../auth/tokenStorage";

// Backend API base URL'i ortam değişkeninden okunur (secret değildir).
const baseURL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";
const API_V1 = "/api/v1";

export const apiClient = axios.create({
  baseURL: `${baseURL}${API_V1}`,
  headers: { "Content-Type": "application/json" },
});

// Her isteğe access token ekle.
apiClient.interceptors.request.use((config) => {
  const token = tokenStorage.getAccess();
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// 401 alınca bir kez refresh dene; başarısızsa oturumu temizle.
let isRefreshing = false;

apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const original = error.config as InternalAxiosRequestConfig & { _retry?: boolean };
    const refresh = tokenStorage.getRefresh();

    if (error.response?.status === 401 && refresh && !original._retry && !isRefreshing) {
      original._retry = true;
      isRefreshing = true;
      try {
        const { data } = await axios.post<{ access_token: string }>(
          `${baseURL}${API_V1}/auth/refresh`,
          { refresh_token: refresh }
        );
        tokenStorage.setAccess(data.access_token);
        isRefreshing = false;
        original.headers.Authorization = `Bearer ${data.access_token}`;
        return apiClient(original);
      } catch (refreshError) {
        isRefreshing = false;
        tokenStorage.clear();
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export interface HealthResponse {
  status: string;
  environment: string;
  project: string;
}

// Health endpoint'i kökte (/health), API_V1 dışında.
export async function fetchHealth(): Promise<HealthResponse> {
  const { data } = await axios.get<HealthResponse>(`${baseURL}/health`);
  return data;
}
