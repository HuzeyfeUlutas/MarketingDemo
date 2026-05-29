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

import {
  createUser,
  deleteUser,
  listUsers,
  updateUser,
} from "../../api/users";
import { useAuth } from "../../auth/AuthContext";
import { roleLabel, User } from "../../types";
import UserFormDialog from "./UserFormDialog";

export default function UsersPage() {
  const { user: currentUser } = useAuth();
  const [users, setUsers] = useState<User[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editing, setEditing] = useState<User | null>(null);

  const load = () => {
    listUsers()
      .then(setUsers)
      .catch(() => setError("Kullanıcılar yüklenemedi."));
  };

  useEffect(load, []);

  const handleDelete = async (u: User) => {
    if (!confirm(`${u.full_name} silinsin mi?`)) return;
    try {
      await deleteUser(u.id);
      load();
    } catch {
      setError("Kullanıcı silinemedi.");
    }
  };

  const handleSubmit = async (data: {
    email: string;
    full_name: string;
    role: User["role"];
    password?: string;
    is_active: boolean;
  }) => {
    if (editing) {
      await updateUser(editing.id, {
        full_name: data.full_name,
        role: data.role,
        is_active: data.is_active,
        ...(data.password ? { password: data.password } : {}),
      });
    } else {
      await createUser({
        email: data.email,
        full_name: data.full_name,
        role: data.role,
        password: data.password!,
        is_active: data.is_active,
      });
    }
    setDialogOpen(false);
    setEditing(null);
    load();
  };

  return (
    <Box>
      <Stack direction="row" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h4">Ekip / Kullanıcılar</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => {
            setEditing(null);
            setDialogOpen(true);
          }}
        >
          Yeni Kullanıcı
        </Button>
      </Stack>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Ad Soyad</TableCell>
              <TableCell>E-posta</TableCell>
              <TableCell>Rol</TableCell>
              <TableCell>Durum</TableCell>
              <TableCell align="right">İşlemler</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {users.map((u) => (
              <TableRow key={u.id} hover>
                <TableCell>{u.full_name}</TableCell>
                <TableCell>{u.email}</TableCell>
                <TableCell>{roleLabel(u.role)}</TableCell>
                <TableCell>
                  <Chip
                    size="small"
                    label={u.is_active ? "Aktif" : "Pasif"}
                    color={u.is_active ? "success" : "default"}
                  />
                </TableCell>
                <TableCell align="right">
                  <IconButton
                    size="small"
                    onClick={() => {
                      setEditing(u);
                      setDialogOpen(true);
                    }}
                  >
                    <EditIcon fontSize="small" />
                  </IconButton>
                  <IconButton
                    size="small"
                    color="error"
                    disabled={u.id === currentUser?.id}
                    onClick={() => handleDelete(u)}
                  >
                    <DeleteIcon fontSize="small" />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
            {users.length === 0 && (
              <TableRow>
                <TableCell colSpan={5} align="center">
                  Kayıt yok.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      <UserFormDialog
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
