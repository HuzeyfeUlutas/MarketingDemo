import {
  Alert,
  Box,
  Button,
  Chip,
  IconButton,
  MenuItem,
  Paper,
  Stack,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Tabs,
  TextField,
  Typography,
} from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import { LineChart } from "@mui/x-charts/LineChart";
import { useEffect, useState } from "react";

import { listClients } from "../../api/clients";
import {
  createKeyword,
  deleteKeyword,
  generateBacklinks,
  listBacklinks,
  listKeywords,
  listSiteAudits,
  runSiteAudit,
} from "../../api/seo";
import { useAuth } from "../../auth/AuthContext";
import { Backlink, Client, Keyword, SiteAudit } from "../../types";

const severityColor: Record<string, "default" | "warning" | "error"> = {
  low: "default",
  medium: "warning",
  high: "error",
};

function currentPosition(kw: Keyword): number | null {
  return kw.rankings.length ? kw.rankings[kw.rankings.length - 1].position : null;
}

export default function SeoPage() {
  const { user } = useAuth();
  const canManage =
    user?.role === "admin" || user?.role === "manager" || user?.role === "seo_specialist";

  const [clients, setClients] = useState<Client[]>([]);
  const [clientId, setClientId] = useState<number | "">("");
  const [tab, setTab] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const [keywords, setKeywords] = useState<Keyword[]>([]);
  const [selectedKw, setSelectedKw] = useState<Keyword | null>(null);
  const [newTerm, setNewTerm] = useState("");

  const [audits, setAudits] = useState<SiteAudit[]>([]);
  const [backlinks, setBacklinks] = useState<Backlink[]>([]);

  useEffect(() => {
    listClients()
      .then((cs) => {
        setClients(cs);
        if (cs.length && clientId === "") setClientId(cs[0].id);
      })
      .catch(() => setError("Müşteriler yüklenemedi."));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const loadAll = () => {
    if (clientId === "") return;
    listKeywords(clientId).then(setKeywords).catch(() => setKeywords([]));
    listSiteAudits(clientId).then(setAudits).catch(() => setAudits([]));
    listBacklinks(clientId).then(setBacklinks).catch(() => setBacklinks([]));
    setSelectedKw(null);
  };

  useEffect(loadAll, [clientId]);

  const handleAddKeyword = async () => {
    if (clientId === "" || !newTerm.trim()) return;
    await createKeyword({ client_id: clientId, term: newTerm.trim() });
    setNewTerm("");
    listKeywords(clientId).then(setKeywords);
  };

  const handleDeleteKeyword = async (id: number) => {
    await deleteKeyword(id);
    if (selectedKw?.id === id) setSelectedKw(null);
    if (clientId !== "") listKeywords(clientId).then(setKeywords);
  };

  const handleAudit = async () => {
    if (clientId === "") return;
    await runSiteAudit(clientId);
    listSiteAudits(clientId).then(setAudits);
  };

  const handleBacklinks = async () => {
    if (clientId === "") return;
    await generateBacklinks(clientId, 8);
    listBacklinks(clientId).then(setBacklinks);
  };

  const latestAudit = audits[0] ?? null;

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        SEO Araçları
      </Typography>

      <TextField
        select
        size="small"
        label="Müşteri"
        value={clientId}
        onChange={(e) => setClientId(Number(e.target.value))}
        sx={{ minWidth: 220, mb: 2 }}
      >
        {clients.map((c) => (
          <MenuItem key={c.id} value={c.id}>
            {c.name}
          </MenuItem>
        ))}
      </TextField>

      {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>{error}</Alert>}

      <Tabs value={tab} onChange={(_, v) => setTab(v)} sx={{ mb: 2 }}>
        <Tab label="Anahtar Kelimeler" />
        <Tab label="Site Denetimi" />
        <Tab label="Backlink'ler" />
      </Tabs>

      {/* Anahtar Kelimeler */}
      {tab === 0 && (
        <Stack spacing={2}>
          {canManage && (
            <Stack direction="row" spacing={1}>
              <TextField
                size="small"
                label="Yeni anahtar kelime"
                value={newTerm}
                onChange={(e) => setNewTerm(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleAddKeyword()}
              />
              <Button variant="contained" onClick={handleAddKeyword}>
                Ekle
              </Button>
            </Stack>
          )}
          <Paper>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>Terim</TableCell>
                  <TableCell>Arama Hacmi</TableCell>
                  <TableCell>Güncel Sıra</TableCell>
                  <TableCell align="right">İşlem</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {keywords.map((kw) => (
                  <TableRow
                    key={kw.id}
                    hover
                    selected={selectedKw?.id === kw.id}
                    sx={{ cursor: "pointer" }}
                    onClick={() => setSelectedKw(kw)}
                  >
                    <TableCell>{kw.term}</TableCell>
                    <TableCell>{kw.search_volume.toLocaleString("tr-TR")}</TableCell>
                    <TableCell>{currentPosition(kw) ?? "—"}</TableCell>
                    <TableCell align="right" onClick={(e) => e.stopPropagation()}>
                      {canManage && (
                        <IconButton
                          size="small"
                          color="error"
                          onClick={() => handleDeleteKeyword(kw.id)}
                        >
                          <DeleteIcon fontSize="small" />
                        </IconButton>
                      )}
                    </TableCell>
                  </TableRow>
                ))}
                {keywords.length === 0 && (
                  <TableRow>
                    <TableCell colSpan={4} align="center">
                      Anahtar kelime yok.
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </Paper>

          {selectedKw && selectedKw.rankings.length > 0 && (
            <Paper sx={{ p: 2 }}>
              <Typography variant="subtitle1" gutterBottom>
                "{selectedKw.term}" — Sıralama Trendi (1 = en iyi)
              </Typography>
              <LineChart
                height={280}
                xAxis={[
                  { scaleType: "point", data: selectedKw.rankings.map((r) => r.date.slice(5)) },
                ]}
                yAxis={[{ reverse: true }]}
                series={[
                  { data: selectedKw.rankings.map((r) => r.position), label: "Pozisyon" },
                ]}
              />
            </Paper>
          )}
        </Stack>
      )}

      {/* Site Denetimi */}
      {tab === 1 && (
        <Stack spacing={2}>
          {canManage && (
            <Box>
              <Button variant="contained" onClick={handleAudit}>
                Denetim Çalıştır (mock)
              </Button>
            </Box>
          )}
          {latestAudit ? (
            <Paper sx={{ p: 2 }}>
              <Stack direction="row" alignItems="center" spacing={2} mb={1}>
                <Typography variant="h3" color={latestAudit.score >= 70 ? "success.main" : "warning.main"}>
                  {latestAudit.score}
                </Typography>
                <Box>
                  <Typography variant="subtitle1">SEO Skoru / 100</Typography>
                  <Typography variant="caption" color="text.secondary">
                    Son denetim: {latestAudit.date}
                  </Typography>
                </Box>
              </Stack>
              <Typography variant="subtitle2" gutterBottom>
                Tespit edilen sorunlar
              </Typography>
              <Stack spacing={1}>
                {latestAudit.issues.map((iss, i) => (
                  <Stack key={i} direction="row" spacing={1} alignItems="center">
                    <Chip
                      size="small"
                      label={iss.severity}
                      color={severityColor[iss.severity] ?? "default"}
                    />
                    <Typography variant="body2">{iss.title}</Typography>
                  </Stack>
                ))}
              </Stack>
            </Paper>
          ) : (
            <Alert severity="info">Henüz site denetimi yok.</Alert>
          )}
        </Stack>
      )}

      {/* Backlink'ler */}
      {tab === 2 && (
        <Stack spacing={2}>
          {canManage && (
            <Box>
              <Button variant="contained" onClick={handleBacklinks}>
                Backlink Üret (mock)
              </Button>
            </Box>
          )}
          <Paper>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>Kaynak URL</TableCell>
                  <TableCell>Otorite</TableCell>
                  <TableCell>Keşif</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {backlinks.map((b) => (
                  <TableRow key={b.id} hover>
                    <TableCell>{b.source_url}</TableCell>
                    <TableCell>
                      <Chip
                        size="small"
                        label={b.authority}
                        color={b.authority >= 60 ? "success" : b.authority >= 30 ? "warning" : "default"}
                      />
                    </TableCell>
                    <TableCell>{new Date(b.discovered_at).toLocaleDateString("tr-TR")}</TableCell>
                  </TableRow>
                ))}
                {backlinks.length === 0 && (
                  <TableRow>
                    <TableCell colSpan={3} align="center">
                      Backlink yok.
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </Paper>
        </Stack>
      )}
    </Box>
  );
}
