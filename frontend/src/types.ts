// Backend ile paylaşılan ortak tipler.

export type UserRole =
  | "admin"
  | "manager"
  | "content_creator"
  | "analyst"
  | "seo_specialist";

export const USER_ROLES: { value: UserRole; label: string }[] = [
  { value: "admin", label: "Admin" },
  { value: "manager", label: "Account Manager" },
  { value: "content_creator", label: "Content Creator" },
  { value: "analyst", label: "Analyst" },
  { value: "seo_specialist", label: "SEO Specialist" },
];

export function roleLabel(role: UserRole): string {
  return USER_ROLES.find((r) => r.value === role)?.label ?? role;
}

export interface User {
  id: number;
  email: string;
  full_name: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface UserSummary {
  id: number;
  full_name: string;
  role: UserRole;
}

// ---- Müşteri (Client) ----

export type ClientStatus = "active" | "paused" | "archived";

export const CLIENT_STATUSES: { value: ClientStatus; label: string }[] = [
  { value: "active", label: "Aktif" },
  { value: "paused", label: "Duraklatıldı" },
  { value: "archived", label: "Arşivlendi" },
];

export function clientStatusLabel(status: ClientStatus): string {
  return CLIENT_STATUSES.find((s) => s.value === status)?.label ?? status;
}

export type SocialPlatform =
  | "instagram"
  | "facebook"
  | "x"
  | "linkedin"
  | "tiktok"
  | "youtube";

export const SOCIAL_PLATFORMS: { value: SocialPlatform; label: string }[] = [
  { value: "instagram", label: "Instagram" },
  { value: "facebook", label: "Facebook" },
  { value: "x", label: "X (Twitter)" },
  { value: "linkedin", label: "LinkedIn" },
  { value: "tiktok", label: "TikTok" },
  { value: "youtube", label: "YouTube" },
];

export function platformLabel(p: SocialPlatform): string {
  return SOCIAL_PLATFORMS.find((s) => s.value === p)?.label ?? p;
}

export interface SocialAccount {
  id: number;
  client_id: number;
  platform: SocialPlatform;
  handle: string;
  follower_count: number;
  avatar_url: string | null;
  created_at: string;
  updated_at: string;
}

export interface Client {
  id: number;
  name: string;
  industry: string | null;
  website: string | null;
  notes: string | null;
  status: ClientStatus;
  manager_id: number | null;
  manager: UserSummary | null;
  social_accounts: SocialAccount[];
  created_at: string;
  updated_at: string;
}
