import AddIcon from "@mui/icons-material/Add";
import DeleteIcon from "@mui/icons-material/Delete";
import EditIcon from "@mui/icons-material/Edit";
import {
  Alert,
  Box,
  Button,
  Chip,
  IconButton,
  Paper,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  ClientPayload,
  createClient,
  deleteClient,
  listClients,
  updateClient,
} from "../../api/clients";
import { useAuth } from "../../auth/AuthContext";
import { Client, ClientStatus, clientStatusLabel } from "../../types";
import ClientFormDialog from "./ClientFormDialog";

const statusColor: Record<ClientStatus, "success" | "warning" | "default"> = {
  active: "success",
  paused: "warning",
  archived: "default",
};

export default function ClientsPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const canManage = user?.role === "admin" || user?.role === "manager";

  const [clients, setClients] = useState<Client[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editing, setEditing] = useState<Client | null>(null);

  const load = () => {
    listClients()
      .then(setClients)
      .catch(() => setError("Müşteriler yüklenemedi."));
  };

  useEffect(load, []);

  const handleDelete = async (c: Client) => {
    if (!confirm(`"${c.name}" silinsin mi?`)) return;
    try {
      await deleteClient(c.id);
      load();
    } catch {
      setError("Müşteri silinemedi.");
    }
  };

  const handleSubmit = async (data: ClientPayload) => {
    if (editing) await updateClient(editing.id, data);
    else await createClient(data);
    setDialogOpen(false);
    setEditing(null);
    load();
  };

  return (
    <Box>
      <Stack direction="row" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h4">Müşteriler</Typography>
        {canManage && (
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => {
              setEditing(null);
              setDialogOpen(true);
            }}
          >
            Yeni Müşteri
          </Button>
        )}
      </Stack>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Ad</TableCell>
              <TableCell>Sektör</TableCell>
              <TableCell>Sorumlu</TableCell>
              <TableCell>Hesaplar</TableCell>
              <TableCell>Durum</TableCell>
              {canManage && <TableCell align="right">İşlemler</TableCell>}
            </TableRow>
          </TableHead>
          <TableBody>
            {clients.map((c) => (
              <TableRow
                key={c.id}
                hover
                sx={{ cursor: "pointer" }}
                onClick={() => navigate(`/clients/${c.id}`)}
              >
                <TableCell>{c.name}</TableCell>
                <TableCell>{c.industry ?? "—"}</TableCell>
                <TableCell>{c.manager?.full_name ?? "—"}</TableCell>
                <TableCell>{c.social_accounts.length}</TableCell>
                <TableCell>
                  <Chip
                    size="small"
                    label={clientStatusLabel(c.status)}
                    color={statusColor[c.status]}
                  />
                </TableCell>
                {canManage && (
                  <TableCell align="right" onClick={(e) => e.stopPropagation()}>
                    <IconButton
                      size="small"
                      onClick={() => {
                        setEditing(c);
                        setDialogOpen(true);
                      }}
                    >
                      <EditIcon fontSize="small" />
                    </IconButton>
                    <IconButton size="small" color="error" onClick={() => handleDelete(c)}>
                      <DeleteIcon fontSize="small" />
                    </IconButton>
                  </TableCell>
                )}
              </TableRow>
            ))}
            {clients.length === 0 && (
              <TableRow>
                <TableCell colSpan={canManage ? 6 : 5} align="center">
                  Henüz müşteri yok.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      <ClientFormDialog
        open={dialogOpen}
        editing={editing}
        onClose={() => {
          setDialogOpen(false);
          setEditing(null);
        }}
        onSubmit={handleSubmit}
      />
    </Box>
  );
}
