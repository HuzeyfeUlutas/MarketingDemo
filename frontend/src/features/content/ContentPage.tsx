import AddIcon from "@mui/icons-material/Add";
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  MenuItem,
  Paper,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import { useEffect, useState } from "react";

import { listClients } from "../../api/clients";
import {
  ContentPayload,
  changeContentStatus,
  createContent,
  deleteContent,
  listContent,
  updateContent,
} from "../../api/content";
import { useAuth } from "../../auth/AuthContext";
import { CONTENT_STATUSES, Client, ContentItem, ContentStatus } from "../../types";
import ContentFormDialog from "./ContentFormDialog";

function fmtDate(iso: string | null): string {
  if (!iso) return "";
  return new Date(iso).toLocaleString("tr-TR", { dateStyle: "short", timeStyle: "short" });
}

export default function ContentPage() {
  const { user } = useAuth();
  const canApprove = user?.role === "admin" || user?.role === "manager";
  const canEdit = canApprove || user?.role === "content_creator";

  const [items, setItems] = useState<ContentItem[]>([]);
  const [clients, setClients] = useState<Client[]>([]);
  const [filterClient, setFilterClient] = useState<number | "">("");
  const [error, setError] = useState<string | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editing, setEditing] = useState<ContentItem | null>(null);

  const load = () => {
    listContent(filterClient === "" ? undefined : filterClient)
      .then(setItems)
      .catch(() => setError("İçerikler yüklenemedi."));
  };

  useEffect(() => {
    listClients().then(setClients).catch(() => setClients([]));
  }, []);
  useEffect(load, [filterClient]);

  const handleSubmit = async (data: ContentPayload) => {
    if (editing) await updateContent(editing.id, data);
    else await createContent(data);
    setDialogOpen(false);
    setEditing(null);
    load();
  };

  const handleStatus = async (
    item: ContentItem,
    target: ContentStatus,
    scheduledAt?: string | null
  ) => {
    try {
      await changeContentStatus(item.id, target, scheduledAt);
      load();
    } catch {
      setError(
        target === "scheduled"
          ? "Zamanlama için önce içeriği düzenleyip planlanan tarihi girin."
          : "Durum değiştirilemedi."
      );
    }
  };

  const handleDelete = async (item: ContentItem) => {
    if (!confirm(`"${item.title}" silinsin mi?`)) return;
    await deleteContent(item.id);
    load();
  };

  // Bir içeriğin mevcut durumuna göre yapılabilecek aksiyonlar.
  const actionsFor = (item: ContentItem) => {
    const a: { label: string; run: () => void; disabled?: boolean }[] = [];
    switch (item.status) {
      case "draft":
        if (canEdit)
          a.push({ label: "İncelemeye gönder", run: () => handleStatus(item, "pending_review") });
        break;
      case "pending_review":
        if (canApprove) {
          a.push({ label: "Onayla", run: () => handleStatus(item, "approved") });
          a.push({ label: "Taslağa dön", run: () => handleStatus(item, "draft") });
        }
        break;
      case "approved":
        if (canApprove) {
          a.push({
            label: "Zamanla",
            run: () => handleStatus(item, "scheduled", item.scheduled_at),
          });
          a.push({ label: "Taslağa dön", run: () => handleStatus(item, "draft") });
        }
        break;
      case "scheduled":
        if (canApprove) {
          a.push({ label: "Hemen yayınla", run: () => handleStatus(item, "published") });
          a.push({ label: "Geri al", run: () => handleStatus(item, "approved") });
        }
        break;
    }
    return a;
  };

  return (
    <Box>
      <Stack direction="row" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h4">İçerik Takvimi & Planlama</Typography>
        {canEdit && (
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => {
              setEditing(null);
              setDialogOpen(true);
            }}
          >
            Yeni İçerik
          </Button>
        )}
      </Stack>

      <TextField
        select
        size="small"
        label="Müşteri filtresi"
        value={filterClient}
        onChange={(e) => setFilterClient(e.target.value === "" ? "" : Number(e.target.value))}
        sx={{ minWidth: 220, mb: 2 }}
      >
        <MenuItem value="">Tümü</MenuItem>
        {clients.map((c) => (
          <MenuItem key={c.id} value={c.id}>
            {c.name}
          </MenuItem>
        ))}
      </TextField>

      {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>{error}</Alert>}

      <Box sx={{ display: "flex", gap: 2, overflowX: "auto", pb: 1 }}>
        {CONTENT_STATUSES.map((col) => {
          const colItems = items.filter((i) => i.status === col.value);
          return (
            <Paper key={col.value} sx={{ p: 1.5, minWidth: 260, flex: "0 0 260px", bgcolor: "grey.50" }}>
              <Typography variant="subtitle2" gutterBottom>
                {col.label} ({colItems.length})
              </Typography>
              <Stack spacing={1}>
                {colItems.map((item) => (
                  <Card key={item.id} variant="outlined">
                    <CardContent sx={{ p: 1.5, "&:last-child": { pb: 1.5 } }}>
                      <Typography variant="body2" fontWeight={600}>
                        {item.title}
                      </Typography>
                      <Typography variant="caption" color="text.secondary" display="block">
                        {item.client?.name ?? "—"}
                      </Typography>
                      {item.scheduled_at && (
                        <Typography variant="caption" color="primary" display="block">
                          📅 {fmtDate(item.scheduled_at)}
                        </Typography>
                      )}
                      <Stack direction="row" spacing={0.5} flexWrap="wrap" useFlexGap mt={0.5}>
                        {item.platforms.map((p) => (
                          <Chip key={p} label={p} size="small" />
                        ))}
                      </Stack>
                      <Stack direction="row" spacing={0.5} flexWrap="wrap" useFlexGap mt={1}>
                        {actionsFor(item).map((act) => (
                          <Button key={act.label} size="small" onClick={act.run}>
                            {act.label}
                          </Button>
                        ))}
                        {canEdit && item.status !== "published" && (
                          <Button
                            size="small"
                            color="inherit"
                            onClick={() => {
                              setEditing(item);
                              setDialogOpen(true);
                            }}
                          >
                            Düzenle
                          </Button>
                        )}
                        {canEdit && (
                          <Button size="small" color="error" onClick={() => handleDelete(item)}>
                            Sil
                          </Button>
                        )}
                      </Stack>
                    </CardContent>
                  </Card>
                ))}
                {colItems.length === 0 && (
                  <Typography variant="caption" color="text.secondary">
                    —
                  </Typography>
                )}
              </Stack>
            </Paper>
          );
        })}
      </Box>

      <ContentFormDialog
        open={dialogOpen}
        editing={editing}
        clients={clients}
        defaultClientId={filterClient}
        onClose={() => {
          setDialogOpen(false);
          setEditing(null);
        }}
        onSubmit={handleSubmit}
      />
    </Box>
  );
}
