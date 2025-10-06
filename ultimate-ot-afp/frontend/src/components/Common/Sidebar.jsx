import React, { useState } from 'react';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Typography,
  Box,
  Divider,
  Avatar,
  Collapse,
  IconButton,
} from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Dashboard,
  Security,
  NetworkCheck,
  Biotech,
  TaskAlt,
  Psychology,
  SmartToy,
  Hub,
  Visibility,
  Sync,
  ExpandLess,
  ExpandMore,
  ChevronLeft,
  ChevronRight,
} from '@mui/icons-material';

const drawerWidth = 280;
const collapsedWidth = 80;

const menuItems = [
  {
    title: 'Dashboard',
    icon: <Dashboard />,
    path: '/dashboard',
  },
  {
    title: 'Digital Forensics',
    icon: <Security />,
    path: '/forensics',
    submenu: [
      { title: 'Autopsy Emulator', path: '/forensics/autopsy' },
      { title: 'Belkasoft Analysis', path: '/forensics/belkasoft' },
      { title: 'FTK Imager', path: '/forensics/ftk' },
      { title: 'Oxygen Suite', path: '/forensics/oxygen' },
    ],
  },
  {
    title: 'Network Security',
    icon: <NetworkCheck />,
    path: '/network-security',
    submenu: [
      { title: 'Packet Capture', path: '/network-security/capture' },
      { title: 'Intrusion Detection', path: '/network-security/ids' },
      { title: 'Protocol Analysis', path: '/network-security/protocol' },
      { title: 'Wireless Security', path: '/network-security/wireless' },
    ],
  },
  {
    title: 'OT Security',
    icon: <Biotech />,
    path: '/ot-security',
    submenu: [
      { title: 'SCADA Monitor', path: '/ot-security/scada' },
      { title: 'Modbus Analysis', path: '/ot-security/modbus' },
      { title: 'Protocol Analyzers', path: '/ot-security/protocols' },
      { title: 'Device Monitoring', path: '/ot-security/devices' },
    ],
  },
  {
    title: 'Task Manager',
    icon: <TaskAlt />,
    path: '/task-manager',
  },
  {
    title: 'AI Analysis',
    icon: <Psychology />,
    path: '/ai-analysis',
    submenu: [
      { title: 'Model Management', path: '/ai-analysis/models' },
      { title: 'Malware Detection', path: '/ai-analysis/malware' },
      { title: 'Anomaly Detection', path: '/ai-analysis/anomaly' },
      { title: 'Log Analysis', path: '/ai-analysis/logs' },
    ],
  },
  {
    title: 'Autonomous Ops',
    icon: <SmartToy />,
    path: '/autonomous',
    submenu: [
      { title: 'Auto Executor', path: '/autonomous/executor' },
      { title: 'Task Scheduler', path: '/autonomous/scheduler' },
      { title: 'Continuous Monitoring', path: '/autonomous/monitoring' },
    ],
  },
  {
    title: 'Command & Control',
    icon: <Hub />,
    path: '/c2',
    submenu: [
      { title: 'Implant Manager', path: '/c2/implants' },
      { title: 'Task Distribution', path: '/c2/tasks' },
      { title: 'Communications', path: '/c2/comms' },
    ],
  },
  {
    title: 'Stealth Operations',
    icon: <Visibility />,
    path: '/stealth',
  },
  {
    title: 'Persistence Engine',
    icon: <Sync />,
    path: '/persistence',
  },
];

const Sidebar = ({ open, onToggle }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const [expandedItems, setExpandedItems] = useState({});

  const handleItemClick = (item) => {
    if (item.submenu) {
      setExpandedItems(prev => ({
        ...prev,
        [item.title]: !prev[item.title]
      }));
    } else {
      navigate(item.path);
    }
  };

  const handleSubmenuClick = (path) => {
    navigate(path);
  };

  const isActive = (path) => {
    return location.pathname === path || location.pathname.startsWith(path + '/');
  };

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: open ? drawerWidth : collapsedWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: open ? drawerWidth : collapsedWidth,
          boxSizing: 'border-box',
          background: 'linear-gradient(180deg, #1a2332 0%, #0f1419 100%)',
          border: 'none',
          borderRight: '1px solid #30363d',
          transition: 'width 0.3s ease',
          overflowX: 'hidden',
        },
      }}
    >
      {/* Header */}
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: open ? 'space-between' : 'center',
          p: 2,
          minHeight: 64,
          borderBottom: '1px solid #30363d',
        }}
      >
        {open && (
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Avatar
              sx={{
                width: 40,
                height: 40,
                background: 'linear-gradient(45deg, #00d4aa, #6c5ce7)',
              }}
            >
              🛡️
            </Avatar>
            <Box>
              <Typography variant="h6" sx={{ fontWeight: 600, fontSize: '1.1rem' }}>
                Ultimate OT-AFP
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Advanced Forensics Platform
              </Typography>
            </Box>
          </Box>
        )}
        
        <IconButton
          onClick={onToggle}
          sx={{
            color: 'text.secondary',
            '&:hover': {
              background: 'rgba(0, 212, 170, 0.1)',
              color: 'primary.main',
            },
          }}
        >
          {open ? <ChevronLeft /> : <ChevronRight />}
        </IconButton>
      </Box>

      {/* Navigation */}
      <List sx={{ flexGrow: 1, px: 1, py: 2 }}>
        {menuItems.map((item, index) => (
          <React.Fragment key={item.title}>
            <ListItem disablePadding sx={{ mb: 0.5 }}>
              <ListItemButton
                onClick={() => handleItemClick(item)}
                sx={{
                  borderRadius: 2,
                  mb: 0.5,
                  backgroundColor: isActive(item.path) 
                    ? 'rgba(0, 212, 170, 0.15)' 
                    : 'transparent',
                  color: isActive(item.path) ? 'primary.main' : 'text.primary',
                  '&:hover': {
                    backgroundColor: 'rgba(0, 212, 170, 0.1)',
                    color: 'primary.main',
                  },
                }}
              >
                <ListItemIcon
                  sx={{
                    color: isActive(item.path) ? 'primary.main' : 'text.secondary',
                    minWidth: open ? 40 : 'auto',
                    mr: open ? 2 : 0,
                  }}
                >
                  {item.icon}
                </ListItemIcon>
                
                {open && (
                  <>
                    <ListItemText 
                      primary={item.title}
                      sx={{
                        '& .MuiListItemText-primary': {
                          fontSize: '0.9rem',
                          fontWeight: isActive(item.path) ? 600 : 400,
                        },
                      }}
                    />
                    {item.submenu && (
                      expandedItems[item.title] ? <ExpandLess /> : <ExpandMore />
                    )}
                  </>
                )}
              </ListItemButton>
            </ListItem>

            {/* Submenu */}
            {open && item.submenu && (
              <Collapse in={expandedItems[item.title]} timeout="auto" unmountOnExit>
                <List component="div" disablePadding>
                  {item.submenu.map((subItem) => (
                    <ListItem key={subItem.path} disablePadding>
                      <ListItemButton
                        onClick={() => handleSubmenuClick(subItem.path)}
                        sx={{
                          pl: 6,
                          borderRadius: 2,
                          backgroundColor: isActive(subItem.path) 
                            ? 'rgba(108, 92, 231, 0.15)' 
                            : 'transparent',
                          color: isActive(subItem.path) ? 'secondary.main' : 'text.secondary',
                          '&:hover': {
                            backgroundColor: 'rgba(108, 92, 231, 0.1)',
                            color: 'secondary.main',
                          },
                        }}
                      >
                        <ListItemText 
                          primary={subItem.title}
                          sx={{
                            '& .MuiListItemText-primary': {
                              fontSize: '0.8rem',
                              fontWeight: isActive(subItem.path) ? 500 : 400,
                            },
                          }}
                        />
                      </ListItemButton>
                    </ListItem>
                  ))}
                </List>
              </Collapse>
            )}
          </React.Fragment>
        ))}
      </List>

      {/* Footer */}
      {open && (
        <Box sx={{ p: 2, borderTop: '1px solid #30363d' }}>
          <Typography variant="caption" color="text.secondary" align="center" display="block">
            Version 1.0.0
          </Typography>
          <Typography variant="caption" color="text.secondary" align="center" display="block">
            Ultimate Security Platform
          </Typography>
        </Box>
      )}
    </Drawer>
  );
};

export default Sidebar;