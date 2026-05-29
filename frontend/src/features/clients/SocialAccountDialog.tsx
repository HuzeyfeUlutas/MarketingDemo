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

import { SocialAccountPayload } from "../../api/clients";
import { SOCIAL_PLATFORMS, SocialPlatform } from "../../types";

interface Props {
  open: boolean;
  onClose: () => void;
  onSubmit: (data: SocialAccountPayload) => Promise<void>;
}

const empty: SocialAccountPayload = { platform: "instagram", handle: "", follower_count: 0 };

export default function SocialAccountDialog({ open, onClose, onSubmit }: Props) {
  const [form, setForm] = useState<SocialAccountPayload>(empty);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (open) {
      setForm(empty);
      setError(null);
    }
  }, [open]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      await onSubmit(form);
    } catch {
      setError("Hesap eklenemedi.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="xs">
      <form onSubmit={handleSubmit}>
        <DialogTitle>Sosyal Hesap Ekle</DialogTitle>
        <DialogContent>
          <Stack spacing={2} mt={1}>
            {error && <Alert severity="error">{error}</Alert>}
            <TextField
              select
              label="Platform"
              value={form.platform}
              onChange={(e) =>
                setForm({ ...form, platform: e.target.value as SocialPlatform })
              }
              fullWidth
            >
              {SOCIAL_PLATFORMS.map((p) => (
                <MenuItem key={p.value} value={p.value}>
                  {p.label}
                </MenuItem>
              ))}
            </TextField>
            <TextField
              label="Kullanıcı Adı (handle)"
              value={form.handle}
              onChange={(e) => setForm({ ...form, handle: e.target.value })}
              required
              fullWidth
            />
            <TextField
              label="Takipçi (boş bırakılırsa rastgele üretilir)"
              type="number"
              value={form.follower_count || ""}
              onChange={(e) =>
                setForm({ ...form, follower_count: Number(e.target.value) || 0 })
              }
              fullWidth
            />
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={onClose}>İptal</Button>
          <Button type="submit" variant="contained" disabled={saving}>
            Ekle
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
}
