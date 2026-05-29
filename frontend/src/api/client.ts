import axios from "axios";

// Backend API base URL'i ortam değişkeninden okunur (secret değildir).
const baseURL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export const apiClient = axios.create({
  baseURL,
  headers: { "Content-Type": "application/json" },
});

// Faz 1'de buraya JWT access token ekleyen request interceptor gelecek.
// apiClient.interceptors.request.use((config) => { ... });

export interface HealthResponse {
  status: string;
  environment: string;
  project: string;
}

export async function fetchHealth(): Promise<HealthResponse> {
  const { data } = await apiClient.get<HealthResponse>("/health");
  return data;
}
