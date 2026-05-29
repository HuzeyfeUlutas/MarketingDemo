import {
  Alert,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControlLabel,
  MenuItem,
  Stack,
  Switch,
  TextField,
} from "@mui/material";
import { FormEvent, useEffect, useState } from "react";

import { User, UserRole, USER_ROLES } from "../../types";

interface FormData {
  email: string;
  full_name: string;
  role: UserRole;
  password?: string;
  is_active: boolean;
}

interface Props {
  open: boolean;
  editing: User | null;
  onClose: () => void;
  onSubmit: (data: FormData) => Promise<void>;
}

const empty: FormData = {
  email: "",
  full_name: "",
  role: "content_creator",
  password: "",
  is_active: true,
};

export default function UserFormDialog({ open, editing, onClose, onSubmit }: Props) {
  const [form, setForm] = useState<FormData>(empty);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (editing) {
      setForm({
        email: editing.email,
        full_name: editing.full_name,
        role: editing.role,
        password: "",
        is_active: editing.is_active,
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
      const detail =
        (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail ??
        "Kaydedilemedi.";
      setError(typeof detail === "string" ? detail : "Kaydedilemedi.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <form onSubmit={handleSubmit}>
        <DialogTitle>{editing ? "Kullanıcı Düzenle" : "Yeni Kullanıcı"}</DialogTitle>
        <DialogContent>
          <Stack spacing={2} mt={1}>
            {error && <Alert severity="error">{error}</Alert>}
            <TextField
              label="E-posta"
              type="email"
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              required
              disabled={!!editing}
              fullWidth
            />
            <TextField
              label="Ad Soyad"
              value={form.full_name}
              onChange={(e) => setForm({ ...form, full_name: e.target.value })}
              required
              fullWidth
            />
            <TextField
              select
              label="Rol"
              value={form.role}
              onChange={(e) => setForm({ ...form, role: e.target.value as UserRole })}
              fullWidth
            >
              {USER_ROLES.map((r) => (
                <MenuItem key={r.value} value={r.value}>
                  {r.label}
                </MenuItem>
              ))}
            </TextField>
            <TextField
              label={editing ? "Yeni Parola (opsiyonel)" : "Parola"}
              type="password"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              required={!editing}
              helperText="En az 8 karakter"
              fullWidth
            />
            <FormControlLabel
              control={
                <Switch
                  checked={form.is_active}
                  onChange={(e) => setForm({ ...form, is_active: e.target.checked })}
                />
              }
              label="Aktif"
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
