import AutoGraphIcon from "@mui/icons-material/AutoGraph";
import DescriptionIcon from "@mui/icons-material/Description";
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Divider,
  Grid,
  MenuItem,
  Paper,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import { LineChart } from "@mui/x-charts/LineChart";
import { useEffect, useState } from "react";

import { createReport, generateMockData, getSummary, listReports } from "../../api/analytics";
import { listClients } from "../../api/clients";
import { useAuth } from "../../auth/AuthContext";
import { AnalyticsSummary, Client, Report } from "../../types";

function StatCard({ label, value, hint }: { label: string; value: string; hint?: string }) {
  return (
    <Card>
      <CardContent>
        <Typography variant="overline" color="text.secondary">
          {label}
        </Typography>
        <Typography variant="h5">{value}</Typography>
        {hint && (
          <Typography variant="caption" color="text.secondary">
            {hint}
          </Typography>
        )}
      </CardContent>
    </Card>
  );
}

const nf = (n: number) => n.toLocaleString("tr-TR");

export default function AnalyticsPage() {
  const { user } = useAuth();
  const canManage = user?.role === "admin" || user?.role === "manager";

  const [clients, setClients] = useState<Client[]>([]);
  const [clientId, setClientId] = useState<number | "">("");
  const [days, setDays] = useState(30);
  const [summary, setSummary] = useState<AnalyticsSummary | null>(null);
  const [reports, setReports] = useState<Report[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    listClients()
      .then((cs) => {
        setClients(cs);
        if (cs.length && clientId === "") setClientId(cs[0].id);
      })
      .catch(() => setError("Müşteriler yüklenemedi."));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const load = () => {
    if (clientId === "") return;
    getSummary(clientId, days)
      .then(setSummary)
      .catch(() => setError("Metrikler yüklenemedi."));
    listReports(clientId).then(setReports).catch(() => setReports([]));
  };

  useEffect(load, [clientId, days]);

  const handleGenerate = async () => {
    if (clientId === "") return;
    setBusy(true);
    try {
      await generateMockData(clientId, 90);
      load();
    } finally {
      setBusy(false);
    }
  };

  const handleReport = async () => {
    if (clientId === "") return;
    await createReport(clientId, days);
    listReports(clientId).then(setReports);
  };

  const ts = summary?.timeseries ?? [];
  const hasData = ts.length > 0;
  const dates = ts.map((p) => p.date.slice(5)); // MM-DD

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Analytics & Raporlama
      </Typography>

      <Stack direction="row" spacing={2} mb={2} flexWrap="wrap" useFlexGap>
        <TextField
          select
          size="small"
          label="Müşteri"
          value={clientId}
          onChange={(e) => setClientId(Number(e.target.value))}
          sx={{ minWidth: 200 }}
        >
          {clients.map((c) => (
            <MenuItem key={c.id} value={c.id}>
              {c.name}
            </MenuItem>
          ))}
        </TextField>
        <TextField
          select
          size="small"
          label="Dönem"
          value={days}
          onChange={(e) => setDays(Number(e.target.value))}
          sx={{ minWidth: 120 }}
        >
          <MenuItem value={7}>7 gün</MenuItem>
          <MenuItem value={30}>30 gün</MenuItem>
          <MenuItem value={90}>90 gün</MenuItem>
        </TextField>
        {canManage && (
          <Button
            variant="outlined"
            startIcon={<AutoGraphIcon />}
            disabled={busy || clientId === ""}
            onClick={handleGenerate}
          >
            Mock veri üret
          </Button>
        )}
      </Stack>

      {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>{error}</Alert>}

      {!hasData && (
        <Alert severity="info" sx={{ mb: 2 }}>
          Bu müşteri için henüz metrik yok.
          {canManage ? ' "Mock veri üret" ile örnek veri oluşturabilirsiniz.' : ""}
        </Alert>
      )}

      {summary && hasData && (
        <>
          <Grid container spacing={2} mb={2}>
            <Grid item xs={6} md={3}>
              <StatCard
                label="Takipçi"
                value={nf(summary.current_followers)}
                hint={`${summary.follower_growth >= 0 ? "+" : ""}${nf(summary.follower_growth)} (dönem)`}
              />
            </Grid>
            <Grid item xs={6} md={3}>
              <StatCard label="Toplam Erişim" value={nf(summary.total_reach)} />
            </Grid>
            <Grid item xs={6} md={3}>
              <StatCard label="Toplam Gösterim" value={nf(summary.total_impressions)} />
            </Grid>
            <Grid item xs={6} md={3}>
              <StatCard label="Etkileşim Oranı" value={`%${summary.engagement_rate}`} />
            </Grid>
          </Grid>

          <Paper sx={{ p: 2, mb: 2 }}>
            <Typography variant="h6" gutterBottom>
              Performans Trendi
            </Typography>
            <LineChart
              height={320}
              xAxis={[{ scaleType: "point", data: dates }]}
              series={[
                { data: ts.map((p) => p.reach), label: "Erişim" },
                { data: ts.map((p) => p.impressions), label: "Gösterim" },
                { data: ts.map((p) => p.engagement), label: "Etkileşim" },
              ]}
            />
          </Paper>

          <Paper sx={{ p: 2 }}>
            <Stack direction="row" justifyContent="space-between" alignItems="center">
              <Typography variant="h6">Raporlar</Typography>
              {canManage && (
                <Button size="small" startIcon={<DescriptionIcon />} onClick={handleReport}>
                  Rapor oluştur ({days} gün)
                </Button>
              )}
            </Stack>
            <Divider sx={{ my: 1 }} />
            <Stack spacing={1}>
              {reports.map((r) => (
                <Box key={r.id}>
                  <Typography variant="body2" fontWeight={600}>
                    {r.title}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {r.period_start} → {r.period_end} · Erişim {nf(r.summary.total_reach ?? 0)} ·
                    Etkileşim %{r.summary.engagement_rate ?? 0}
                  </Typography>
                </Box>
              ))}
              {reports.length === 0 && (
                <Typography variant="caption" color="text.secondary">
                  Henüz rapor yok.
                </Typography>
              )}
            </Stack>
          </Paper>
        </>
      )}
    </Box>
  );
}
