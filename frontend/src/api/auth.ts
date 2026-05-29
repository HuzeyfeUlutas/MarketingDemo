import { apiClient } from "./client";
import { User } from "../types";

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

// Backend login endpoint'i OAuth2 form (x-www-form-urlencoded) bekler.
export async function login(email: string, password: string): Promise<TokenResponse> {
  const form = new URLSearchParams();
  form.append("username", email);
  form.append("password", password);
  const { data } = await apiClient.post<TokenResponse>("/auth/login", form, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  return data;
}

export async function getMe(): Promise<User> {
  const { data } = await apiClient.get<User>("/auth/me");
  return data;
}
