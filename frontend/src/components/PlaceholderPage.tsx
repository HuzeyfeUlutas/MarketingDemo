import { Box, Paper, Typography } from "@mui/material";

// Henüz uygulanmamış modüller için geçici sayfa (Faz 1+ ile doldurulacak).
export default function PlaceholderPage({ title }: { title: string }) {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        {title}
      </Typography>
      <Paper sx={{ p: 3 }}>
        <Typography color="text.secondary">
          Bu modül sonraki fazlarda geliştirilecek. (Yol haritası:
          docs/ROADMAP.md)
        </Typography>
      </Paper>
    </Box>
  );
}
