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
