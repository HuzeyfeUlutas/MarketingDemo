import {
  Alert,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  MenuItem,
  Stack,
  TextField,
} from "@mui/material";
import { FormEvent, useEffect, useState } from "react";

import { ClientPayload, listAssignableManagers } from "../../api/clients";
import { CLIENT_STATUSES, Client, ClientStatus, UserSummary } from "../../types";

interface Props {
  open: boolean;
  editing: Client | null;
  onClose: () => void;
  onSubmit: (data: ClientPayload) => Promise<void>;
}

const empty: ClientPayload = {
  name: "",
  industry: "",
  website: "",
  notes: "",
  status: "active",
  manager_id: null,
};

export default function ClientFormDialog({ open, editing, onClose, onSubmit }: Props) {
  const [form, setForm] = useState<ClientPayload>(empty);
  const [managers, setManagers] = useState<UserSummary[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (!open) return;
    listAssignableManagers().then(setManagers).catch(() => setManagers([]));
    if (editing) {
      setForm({
        name: editing.name,
        industry: editing.industry ?? "",
        website: editing.website ?? "",
        notes: editing.notes ?? "",
        status: editing.status,
        manager_id: editing.manager_id,
      });
    } else {
      setForm(empty);
    }
    setError(null);
  }, [editing, open]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    setSaving(true);
    try {
      await onSubmit(form);
    } catch (err: unknown) {
      const detail = (err as { response?: { data?: { detail?: string } } })?.response?.data
        ?.detail;
      setError(typeof detail === "string" ? detail : "Kaydedilemedi.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <form onSubmit={handleSubmit}>
        <DialogTitle>{editing ? "Müşteri Düzenle" : "Yeni Müşteri"}</DialogTitle>
        <DialogContent>
          <Stack spacing={2} mt={1}>
            {error && <Alert severity="error">{error}</Alert>}
            <TextField
              label="Müşteri Adı"
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              required
              fullWidth
            />
            <TextField
              label="Sektör"
              value={form.industry ?? ""}
              onChange={(e) => setForm({ ...form, industry: e.target.value })}
              fullWidth
            />
            <TextField
              label="Web Sitesi"
              value={form.website ?? ""}
              onChange={(e) => setForm({ ...form, website: e.target.value })}
              fullWidth
            />
            <TextField
              select
              label="Durum"
              value={form.status}
              onChange={(e) => setForm({ ...form, status: e.target.value as ClientStatus })}
              fullWidth
            >
              {CLIENT_STATUSES.map((s) => (
                <MenuItem key={s.value} value={s.value}>
                  {s.label}
                </MenuItem>
              ))}
            </TextField>
            <TextField
              select
              label="Sorumlu Yönetici"
              value={form.manager_id ?? ""}
              onChange={(e) =>
                setForm({
                  ...form,
                  manager_id: e.target.value === "" ? null : Number(e.target.value),
                })
              }
              fullWidth
            >
              <MenuItem value="">— Atanmadı —</MenuItem>
              {managers.map((m) => (
                <MenuItem key={m.id} value={m.id}>
                  {m.full_name}
                </MenuItem>
              ))}
            </TextField>
            <TextField
              label="Notlar"
              value={form.notes ?? ""}
              onChange={(e) => setForm({ ...form, notes: e.target.value })}
              multiline
              minRows={2}
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
