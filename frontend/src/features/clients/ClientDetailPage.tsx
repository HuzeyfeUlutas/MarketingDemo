import AddIcon from "@mui/icons-material/Add";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import DeleteIcon from "@mui/icons-material/Delete";
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Divider,
  Grid,
  IconButton,
  Link as MuiLink,
  List,
  ListItem,
  ListItemText,
  Stack,
  Typography,
} from "@mui/material";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import {
  SocialAccountPayload,
  addSocialAccount,
  deleteSocialAccount,
  getClient,
} from "../../api/clients";
import { useAuth } from "../../auth/AuthContext";
import { Client, clientStatusLabel, platformLabel } from "../../types";
import SocialAccountDialog from "./SocialAccountDialog";

export default function ClientDetailPage() {
  const { id } = useParams();
  const clientId = Number(id);
  const navigate = useNavigate();
  const { user } = useAuth();
  const canManage = user?.role === "admin" || user?.role === "manager";

  const [client, setClient] = useState<Client | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);

  const load = () => {
    getClient(clientId)
      .then(setClient)
      .catch(() => setError("Müşteri yüklenemedi."));
  };

  useEffect(load, [clientId]);

  const handleAdd = async (data: SocialAccountPayload) => {
    await addSocialAccount(clientId, data);
    setDialogOpen(false);
    load();
  };

  const handleDeleteAccount = async (accountId: number) => {
    if (!confirm("Hesap silinsin mi?")) return;
    await deleteSocialAccount(clientId, accountId);
    load();
  };

  if (error) return <Alert severity="error">{error}</Alert>;
  if (!client) return null;

  return (
    <Box>
      <Button startIcon={<ArrowBackIcon />} onClick={() => navigate("/clients")} sx={{ mb: 2 }}>
        Müşteriler
      </Button>

      <Stack direction="row" alignItems="center" spacing={2} mb={2}>
        <Typography variant="h4">{client.name}</Typography>
        <Chip label={clientStatusLabel(client.status)} />
      </Stack>

      <Grid container spacing={2}>
        <Grid item xs={12} md={5}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Bilgiler
              </Typography>
              <Stack spacing={1}>
                <Typography variant="body2">
                  <strong>Sektör:</strong> {client.industry ?? "—"}
                </Typography>
                <Typography variant="body2">
                  <strong>Web:</strong>{" "}
                  {client.website ? (
                    <MuiLink href={client.website} target="_blank" rel="noopener">
                      {client.website}
                    </MuiLink>
                  ) : (
                    "—"
                  )}
                </Typography>
                <Typography variant="body2">
                  <strong>Sorumlu Yönetici:</strong> {client.manager?.full_name ?? "—"}
                </Typography>
                {client.notes && (
                  <Typography variant="body2">
                    <strong>Notlar:</strong> {client.notes}
                  </Typography>
                )}
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={7}>
          <Card>
            <CardContent>
              <Stack direction="row" justifyContent="space-between" alignItems="center">
                <Typography variant="h6">Sosyal Hesaplar (mock)</Typography>
                {canManage && (
                  <Button
                    size="small"
                    startIcon={<AddIcon />}
                    onClick={() => setDialogOpen(true)}
                  >
                    Ekle
                  </Button>
                )}
              </Stack>
              <Divider sx={{ my: 1 }} />
              <List dense>
                {client.social_accounts.map((acc) => (
                  <ListItem
                    key={acc.id}
                    secondaryAction={
                      canManage && (
                        <IconButton
                          edge="end"
                          size="small"
                          color="error"
                          onClick={() => handleDeleteAccount(acc.id)}
                        >
                          <DeleteIcon fontSize="small" />
                        </IconButton>
                      )
                    }
                  >
                    <ListItemText
                      primary={`${platformLabel(acc.platform)} — ${acc.handle}`}
                      secondary={`${acc.follower_count.toLocaleString("tr-TR")} takipçi`}
                    />
                  </ListItem>
                ))}
                {client.social_accounts.length === 0 && (
                  <Typography variant="body2" color="text.secondary">
                    Henüz sosyal hesap eklenmemiş.
                  </Typography>
                )}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <SocialAccountDialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        onSubmit={handleAdd}
      />
    </Box>
  );
}
