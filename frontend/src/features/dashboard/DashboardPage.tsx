import { Alert, Card, CardContent, Chip, Grid, Stack, Typography } from "@mui/material";
import { useEffect, useState } from "react";

import { fetchHealth, HealthResponse } from "../../api/client";

// Faz 0 örnek dashboard'u: backend bağlantısını doğrular ve modül kartlarını
// gösterir. Gerçek metrikler Faz 4'te (Analytics) gelecek.
const moduleCards = [
  { title: "Müşteriler", desc: "Ajansın yönettiği şirketler ve sosyal hesaplar." },
  { title: "İçerik Takvimi", desc: "Gönderi planlama ve onay akışı." },
  { title: "Analytics", desc: "Performans metrikleri ve raporlar." },
  { title: "SEO", desc: "Anahtar kelime, sıralama ve site denetimi." },
];

export default function DashboardPage() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchHealth()
      .then(setHealth)
      .catch(() => setError("Backend'e bağlanılamadı (API çalışıyor mu?)."));
  }, []);

  return (
    <Stack spacing={3}>
      <Typography variant="h4">Dashboard</Typography>

      {error && <Alert severity="warning">{error}</Alert>}
      {health && (
        <Alert severity="success">
          Backend bağlantısı OK — ortam:{" "}
          <Chip size="small" label={health.environment} sx={{ ml: 1 }} />
        </Alert>
      )}

      <Grid container spacing={2}>
        {moduleCards.map((m) => (
          <Grid item xs={12} sm={6} md={3} key={m.title}>
            <Card>
              <CardContent>
                <Typography variant="h6">{m.title}</Typography>
                <Typography variant="body2" color="text.secondary">
                  {m.desc}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Stack>
  );
}
