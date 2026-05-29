import { apiClient } from "./client";
import { AnalyticsSummary, Report } from "../types";

export async function getSummary(clientId: number, days = 30): Promise<AnalyticsSummary> {
  const { data } = await apiClient.get<AnalyticsSummary>("/analytics/summary", {
    params: { client_id: clientId, days },
  });
  return data;
}

export async function generateMockData(clientId: number, days = 30): Promise<number> {
  const { data } = await apiClient.post<{ created: number }>(
    "/analytics/generate",
    {},
    { params: { client_id: clientId, days } }
  );
  return data.created;
}

export async function listReports(clientId?: number): Promise<Report[]> {
  const params = clientId ? { client_id: clientId } : undefined;
  const { data } = await apiClient.get<Report[]>("/analytics/reports", { params });
  return data;
}

export async function createReport(clientId: number, periodDays = 30): Promise<Report> {
  const { data } = await apiClient.post<Report>("/analytics/reports", {
    client_id: clientId,
    period_days: periodDays,
  });
  return data;
}
