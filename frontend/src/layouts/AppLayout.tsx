import CampaignIcon from "@mui/icons-material/Campaign";
import CalendarMonthIcon from "@mui/icons-material/CalendarMonth";
import DashboardIcon from "@mui/icons-material/Dashboard";
import InsightsIcon from "@mui/icons-material/Insights";
import PeopleIcon from "@mui/icons-material/People";
import SearchIcon from "@mui/icons-material/Search";
import {
  AppBar,
  Box,
  Drawer,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
} from "@mui/material";
import { ReactNode } from "react";
import { Link, useLocation } from "react-router-dom";

const drawerWidth = 240;

// Sol menü öğeleri — her MVP modülü için bir giriş (sayfalar sonraki fazlarda).
const navItems = [
  { label: "Dashboard", path: "/", icon: <DashboardIcon /> },
  { label: "Müşteriler", path: "/clients", icon: <PeopleIcon /> },
  { label: "İçerik Takvimi", path: "/content", icon: <CalendarMonthIcon /> },
  { label: "Analytics", path: "/analytics", icon: <InsightsIcon /> },
  { label: "SEO", path: "/seo", icon: <SearchIcon /> },
];

export default function AppLayout({ children }: { children: ReactNode }) {
  const location = useLocation();

  return (
    <Box sx={{ display: "flex" }}>
      <AppBar position="fixed" sx={{ zIndex: (t) => t.zIndex.drawer + 1 }}>
        <Toolbar>
          <CampaignIcon sx={{ mr: 1 }} />
          <Typography variant="h6" noWrap>
            Social Media Agency Tool
          </Typography>
        </Toolbar>
      </AppBar>

      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: "border-box" },
        }}
      >
        <Toolbar />
        <List>
          {navItems.map((item) => (
            <ListItemButton
              key={item.path}
              component={Link}
              to={item.path}
              selected={location.pathname === item.path}
            >
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.label} />
            </ListItemButton>
          ))}
        </List>
      </Drawer>

      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <Toolbar />
        {children}
      </Box>
    </Box>
  );
}
