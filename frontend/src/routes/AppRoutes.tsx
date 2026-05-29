import { Route, Routes } from "react-router-dom";

import PlaceholderPage from "../components/PlaceholderPage";
import ProtectedRoute from "../components/ProtectedRoute";
import AnalyticsPage from "../features/analytics/AnalyticsPage";
import LoginPage from "../features/auth/LoginPage";
import ClientDetailPage from "../features/clients/ClientDetailPage";
import ClientsPage from "../features/clients/ClientsPage";
import ContentPage from "../features/content/ContentPage";
import DashboardPage from "../features/dashboard/DashboardPage";
import UsersPage from "../features/users/UsersPage";
import AppLayout from "../layouts/AppLayout";

export default function AppRoutes() {
  return (
    <Routes>
      {/* Public */}
      <Route path="/login" element={<LoginPage />} />

      {/* Korumalı alan (giriş gerektirir) */}
      <Route
        path="/*"
        element={
          <ProtectedRoute>
            <AppLayout>
              <Routes>
                <Route path="" element={<DashboardPage />} />
                <Route path="clients" element={<ClientsPage />} />
                <Route path="clients/:id" element={<ClientDetailPage />} />
                <Route path="content" element={<ContentPage />} />
                <Route path="analytics" element={<AnalyticsPage />} />
                <Route path="seo" element={<PlaceholderPage title="SEO" />} />
                <Route
                  path="users"
                  element={
                    <ProtectedRoute adminOnly>
                      <UsersPage />
                    </ProtectedRoute>
                  }
                />
              </Routes>
            </AppLayout>
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}
