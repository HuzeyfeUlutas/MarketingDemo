import { apiClient } from "./client";
import { Backlink, Keyword, SiteAudit } from "../types";

// ---- Anahtar kelimeler ----

export async function listKeywords(clientId: number): Promise<Keyword[]> {
  const { data } = await apiClient.get<Keyword[]>("/seo/keywords", {
    params: { client_id: clientId },
  });
  return data;
}

export async function createKeyword(payload: {
  client_id: number;
  term: string;
  target_url?: string | null;
  search_volume?: number;
}): Promise<Keyword> {
  const { data } = await apiClient.post<Keyword>("/seo/keywords", payload);
  return data;
}

export async function deleteKeyword(id: number): Promise<void> {
  await apiClient.delete(`/seo/keywords/${id}`);
}

// ---- Site denetimi ----

export async function listSiteAudits(clientId: number): Promise<SiteAudit[]> {
  const { data } = await apiClient.get<SiteAudit[]>("/seo/site-audits", {
    params: { client_id: clientId },
  });
  return data;
}

export async function runSiteAudit(clientId: number): Promise<SiteAudit> {
  const { data } = await apiClient.post<SiteAudit>(
    "/seo/site-audits",
    {},
    { params: { client_id: clientId } }
  );
  return data;
}

// ---- Backlink ----

export async function listBacklinks(clientId: number): Promise<Backlink[]> {
  const { data } = await apiClient.get<Backlink[]>("/seo/backlinks", {
    params: { client_id: clientId },
  });
  return data;
}

export async function generateBacklinks(clientId: number, count = 8): Promise<number> {
  const { data } = await apiClient.post<{ created: number }>(
    "/seo/backlinks/generate",
    {},
    { params: { client_id: clientId, count } }
  );
  return data.created;
}
