import { Route, Routes } from "react-router-dom";

import PlaceholderPage from "../components/PlaceholderPage";
import DashboardPage from "../features/dashboard/DashboardPage";

// Faz 1'de korumalı (auth gerektiren) route yapısı eklenecek.
export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<DashboardPage />} />
      <Route path="/clients" element={<PlaceholderPage title="Müşteriler" />} />
      <Route path="/content" element={<PlaceholderPage title="İçerik Takvimi" />} />
      <Route path="/analytics" element={<PlaceholderPage title="Analytics" />} />
      <Route path="/seo" element={<PlaceholderPage title="SEO" />} />
    </Routes>
  );
}
