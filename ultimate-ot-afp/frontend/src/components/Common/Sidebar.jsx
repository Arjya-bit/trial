import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  AppBar,
  Toolbar,
  Typography,
  Box,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Gavel as ForensicsIcon,
  Security as NetworkIcon,
  Widgets as OTIcon,
  Assignment as TaskIcon,
  SmartToy as AIIcon,
  Hub as C2Icon,
  FlashOn as AutoIcon,
  Lock as StealthIcon,
  PowerSettingsNew as PersistenceIcon,
} from '@mui/icons-material';

const drawerWidth = 240;

const menuItems = [
  { text: 'Dashboard', icon: <DashboardIcon />, path: '/' },
  { text: 'Forensics', icon: <ForensicsIcon />, path: '/forensics' },
  { text: 'Network Security', icon: <NetworkIcon />, path: '/network-security' },
  { text: 'OT Security', icon: <OTIcon />, path: '/ot-security' },
  { text: 'Task Manager', icon: <TaskIcon />, path: '/task-manager' },
  { text: 'AI Analysis', icon: <AIIcon />, path: '/ai-analysis' },
  { text: 'C2 Control', icon: <C2Icon />, path: '/c2' },
  { text: 'Autonomous', icon: <AutoIcon />, path: '/autonomous' },
  { text: 'Persistence', icon: <PersistenceIcon />, path: '/persistence' },
  { text: 'Stealth', icon: <StealthIcon />, path: '/stealth' },
];

function Sidebar() {
  const location = useLocation();

  return (
    <>
      <AppBar
        position="fixed"
        sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}
      >
        <Toolbar>
          <Typography variant="h6" noWrap component="div">
            Ultimate OT-AFP Platform
          </Typography>
        </Toolbar>
      </AppBar>
      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
          },
        }}
      >
        <Toolbar />
        <Box sx={{ overflow: 'auto' }}>
          <List>
            {menuItems.map((item) => (
              <ListItem
                button
                key={item.text}
                component={Link}
                to={item.path}
                selected={location.pathname === item.path}
              >
                <ListItemIcon>{item.icon}</ListItemIcon>
                <ListItemText primary={item.text} />
              </ListItem>
            ))}
          </List>
        </Box>
      </Drawer>
    </>
  );
}

export default Sidebar;
