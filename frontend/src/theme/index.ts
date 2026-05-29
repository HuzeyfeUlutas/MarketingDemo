import { createTheme } from "@mui/material/styles";

// Ajans aracı için temel MUI teması. Renkler/markalama sonra özelleştirilebilir.
export const theme = createTheme({
  palette: {
    mode: "light",
    primary: { main: "#4f46e5" },
    secondary: { main: "#0ea5e9" },
    background: { default: "#f5f6fa" },
  },
  shape: { borderRadius: 10 },
  typography: {
    fontFamily: "Inter, Roboto, system-ui, sans-serif",
  },
});
