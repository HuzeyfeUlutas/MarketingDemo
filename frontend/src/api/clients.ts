import { apiClient } from "./client";
import {
  Client,
  ClientStatus,
  SocialAccount,
  SocialPlatform,
  UserSummary,
} from "../types";

export interface ClientPayload {
  name: string;
  industry?: string | null;
  website?: string | null;
  notes?: string | null;
  status?: ClientStatus;
  manager_id?: number | null;
}

export async function listClients(): Promise<Client[]> {
  const { data } = await apiClient.get<Client[]>("/clients");
  return data;
}

export async function getClient(id: number): Promise<Client> {
  const { data } = await apiClient.get<Client>(`/clients/${id}`);
  return data;
}

export async function createClient(payload: ClientPayload): Promise<Client> {
  const { data } = await apiClient.post<Client>("/clients", payload);
  return data;
}

export async function updateClient(id: number, payload: ClientPayload): Promise<Client> {
  const { data } = await apiClient.patch<Client>(`/clients/${id}`, payload);
  return data;
}

export async function deleteClient(id: number): Promise<void> {
  await apiClient.delete(`/clients/${id}`);
}

export async function listAssignableManagers(): Promise<UserSummary[]> {
  const { data } = await apiClient.get<UserSummary[]>("/clients/assignable-managers");
  return data;
}

// ---- Sosyal hesaplar ----

export interface SocialAccountPayload {
  platform: SocialPlatform;
  handle: string;
  follower_count?: number;
  avatar_url?: string | null;
}

export async function addSocialAccount(
  clientId: number,
  payload: SocialAccountPayload
): Promise<SocialAccount> {
  const { data } = await apiClient.post<SocialAccount>(
    `/clients/${clientId}/social-accounts`,
    payload
  );
  return data;
}

export async function deleteSocialAccount(
  clientId: number,
  accountId: number
): Promise<void> {
  await apiClient.delete(`/clients/${clientId}/social-accounts/${accountId}`);
}
