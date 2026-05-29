import { apiClient } from "./client";
import { ContentItem, ContentStatus, SocialPlatform } from "../types";

export interface ContentPayload {
  client_id: number;
  title: string;
  body?: string;
  platforms?: SocialPlatform[];
  scheduled_at?: string | null;
}

export interface ContentUpdatePayload {
  title?: string;
  body?: string;
  platforms?: SocialPlatform[];
  scheduled_at?: string | null;
}

export async function listContent(clientId?: number): Promise<ContentItem[]> {
  const params = clientId ? { client_id: clientId } : undefined;
  const { data } = await apiClient.get<ContentItem[]>("/content-items", { params });
  return data;
}

export async function createContent(payload: ContentPayload): Promise<ContentItem> {
  const { data } = await apiClient.post<ContentItem>("/content-items", payload);
  return data;
}

export async function updateContent(
  id: number,
  payload: ContentUpdatePayload
): Promise<ContentItem> {
  const { data } = await apiClient.patch<ContentItem>(`/content-items/${id}`, payload);
  return data;
}

export async function deleteContent(id: number): Promise<void> {
  await apiClient.delete(`/content-items/${id}`);
}

export async function changeContentStatus(
  id: number,
  status: ContentStatus,
  scheduledAt?: string | null
): Promise<ContentItem> {
  const { data } = await apiClient.post<ContentItem>(`/content-items/${id}/status`, {
    status,
    scheduled_at: scheduledAt ?? null,
  });
  return data;
}
