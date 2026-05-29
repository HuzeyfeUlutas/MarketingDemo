import {
  Alert,
  Box,
  Button,
  Chip,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  MenuItem,
  Stack,
  TextField,
} from "@mui/material";
import { FormEvent, useEffect, useState } from "react";

import { ContentPayload } from "../../api/content";
import { Client, ContentItem, SOCIAL_PLATFORMS, SocialPlatform } from "../../types";

interface Props {
  open: boolean;
  editing: ContentItem | null;
  clients: Client[];
  defaultClientId?: number | "";
  onClose: () => void;
  onSubmit: (data: ContentPayload) => Promise<void>;
}

// ISO (UTC) ↔ datetime-local input dönüşümü.
function toLocalInput(iso: string | null): string {
  if (!iso) return "";
  const d = new Date(iso);
  const off = d.getTimezoneOffset();
  return new Date(d.getTime() - off * 60000).toISOString().slice(0, 16);
}

export default function ContentFormDialog({
  open,
  editing,
  clients,
  defaultClientId = "",
  onClose,
  onSubmit,
}: Props) {
  const [clientId, setClientId] = useState<number | "">("");
  const [title, setTitle] = useState("");
  const [body, setBody] = useState("");
  const [platforms, setPlatforms] = useState<SocialPlatform[]>([]);
  const [scheduledLocal, setScheduledLocal] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (!open) return;
    if (editing) {
      setClientId(editing.client_id);
      setTitle(editing.title);
      setBody(editing.body);
      setPlatforms(editing.platforms);
      setScheduledLocal(toLocalInput(editing.scheduled_at));
    } else {
      setClientId(defaultClientId);
      setTitle("");
      setBody("");
      setPlatforms([]);
      setScheduledLocal("");
    }
    setError(null);
  }, [open, editing, defaultClientId]);

  const togglePlatform = (p: SocialPlatform) =>
    setPlatforms((prev) => (prev.includes(p) ? prev.filter((x) => x !== p) : [...prev, p]));

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (clientId === "") {
      setError("Müşteri seçiniz.");
      return;
    }
    setSaving(true);
    setError(null);
    try {
      await onSubmit({
        client_id: clientId,
        title,
        body,
        platforms,
        scheduled_at: scheduledLocal ? new Date(scheduledLocal).toISOString() : null,
      });
    } catch {
      setError("Kaydedilemedi.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <form onSubmit={handleSubmit}>
        <DialogTitle>{editing ? "İçerik Düzenle" : "Yeni İçerik"}</DialogTitle>
        <DialogContent>
          <Stack spacing={2} mt={1}>
            {error && <Alert severity="error">{error}</Alert>}
            <TextField
              select
              label="Müşteri"
              value={clientId}
              onChange={(e) => setClientId(Number(e.target.value))}
              required
              disabled={!!editing}
              fullWidth
            >
              {clients.map((c) => (
                <MenuItem key={c.id} value={c.id}>
                  {c.name}
                </MenuItem>
              ))}
            </TextField>
            <TextField
              label="Başlık"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
              fullWidth
            />
            <TextField
              label="Metin / Caption"
              value={body}
              onChange={(e) => setBody(e.target.value)}
              multiline
              minRows={3}
              fullWidth
            />
            <Box>
              <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
                {SOCIAL_PLATFORMS.map((p) => (
                  <Chip
                    key={p.value}
                    label={p.label}
                    color={platforms.includes(p.value) ? "primary" : "default"}
                    onClick={() => togglePlatform(p.value)}
                    variant={platforms.includes(p.value) ? "filled" : "outlined"}
                  />
                ))}
              </Stack>
            </Box>
            <TextField
              label="Planlanan Tarih/Saat"
              type="datetime-local"
              value={scheduledLocal}
              onChange={(e) => setScheduledLocal(e.target.value)}
              InputLabelProps={{ shrink: true }}
              fullWidth
            />
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={onClose}>İptal</Button>
          <Button type="submit" variant="contained" disabled={saving}>
            {saving ? "Kaydediliyor..." : "Kaydet"}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
}
