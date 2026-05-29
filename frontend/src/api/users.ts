import { apiClient } from "./client";
import { User, UserRole } from "../types";

export interface UserCreatePayload {
  email: string;
  full_name: string;
  role: UserRole;
  password: string;
  is_active?: boolean;
}

export interface UserUpdatePayload {
  full_name?: string;
  role?: UserRole;
  is_active?: boolean;
  password?: string;
}

export async function listUsers(): Promise<User[]> {
  const { data } = await apiClient.get<User[]>("/users");
  return data;
}

export async function createUser(payload: UserCreatePayload): Promise<User> {
  const { data } = await apiClient.post<User>("/users", payload);
  return data;
}

export async function updateUser(id: number, payload: UserUpdatePayload): Promise<User> {
  const { data } = await apiClient.patch<User>(`/users/${id}`, payload);
  return data;
}

export async function deleteUser(id: number): Promise<void> {
  await apiClient.delete(`/users/${id}`);
}
