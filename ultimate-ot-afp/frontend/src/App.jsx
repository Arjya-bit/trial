import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline, Box } from '@mui/material';
import { QueryClient, QueryClientProvider } from 'react-query';
import { SnackbarProvider } from 'notistack';

// Components
import Sidebar from './components/Common/Sidebar';
import TopBar from './components/Common/TopBar';

// Pages
import Dashboard from './pages/Dashboard';
import ForensicsPage from './pages/ForensicsPage';
import NetworkSecurityPage from './pages/NetworkSecurityPage';
import OTSecurityPage from './pages/OTSecurityPage';
import TaskManagerPage from './pages/TaskManagerPage';
import AIAnalysisPage from './pages/AIAnalysisPage';
import AutonomousPage from './pages/AutonomousPage';
import C2Page from './pages/C2Page';
import StealthPage from './pages/StealthPage';
import PersistencePage from './pages/PersistencePage';

// Services
import { initializeWebSocket } from './services/websocket';

// Create React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      staleTime: 1000 * 60 * 5, // 5 minutes
    },
  },
});

// Create dark theme
const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#00d4aa',
      dark: '#00b894',
      light: '#26e6cc',
    },
    secondary: {
      main: '#6c5ce7',
      dark: '#5a4fcf',
      light: '#8b7eeb',
    },
    background: {
      default: '#0f1419',
      paper: '#1a2332',
    },
    text: {
      primary: '#e1e5e9',
      secondary: '#8b949e',
    },
    error: {
      main: '#f85149',
    },
    warning: {
      main: '#f0883e',
    },
    success: {
      main: '#2ea043',
    },
    info: {
      main: '#58a6ff',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 600,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 500,
    },
    h4: {
      fontSize: '1.5rem',
      fontWeight: 500,
    },
    h5: {
      fontSize: '1.25rem',
      fontWeight: 500,
    },
    h6: {
      fontSize: '1rem',
      fontWeight: 500,
    },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          background: 'linear-gradient(145deg, #1e2a3a 0%, #252f3f 100%)',
          border: '1px solid #30363d',
          borderRadius: '12px',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: '8px',
          textTransform: 'none',
          fontWeight: 500,
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: '6px',
        },
      },
    },
  },
});

const App = () => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [wsConnected, setWsConnected] = useState(false);

  useEffect(() => {
    // Initialize WebSocket connection
    const websocket = initializeWebSocket();
    
    websocket.on('connect', () => {
      setWsConnected(true);
      console.log('🔌 WebSocket connected');
    });

    websocket.on('disconnect', () => {
      setWsConnected(false);
      console.log('🔌 WebSocket disconnected');
    });

    return () => {
      websocket.disconnect();
    };
  }, []);

  const handleSidebarToggle = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={darkTheme}>
        <CssBaseline />
        <SnackbarProvider 
          maxSnack={3}
          anchorOrigin={{
            vertical: 'top',
            horizontal: 'right',
          }}
        >
          <Router>
            <Box sx={{ display: 'flex', minHeight: '100vh' }}>
              <Sidebar open={sidebarOpen} onToggle={handleSidebarToggle} />
              
              <Box 
                component="main" 
                sx={{ 
                  flexGrow: 1,
                  transition: 'margin-left 0.3s',
                  marginLeft: sidebarOpen ? '280px' : '80px',
                  background: 'linear-gradient(135deg, #0f1419 0%, #1a2332 100%)',
                  minHeight: '100vh',
                }}
              >
                <TopBar 
                  onSidebarToggle={handleSidebarToggle}
                  wsConnected={wsConnected}
                />
                
                <Box sx={{ p: 3, mt: 8 }}>
                  <Routes>
                    <Route path="/" element={<Navigate to="/dashboard" replace />} />
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/forensics" element={<ForensicsPage />} />
                    <Route path="/network-security" element={<NetworkSecurityPage />} />
                    <Route path="/ot-security" element={<OTSecurityPage />} />
                    <Route path="/task-manager" element={<TaskManagerPage />} />
                    <Route path="/ai-analysis" element={<AIAnalysisPage />} />
                    <Route path="/autonomous" element={<AutonomousPage />} />
                    <Route path="/c2" element={<C2Page />} />
                    <Route path="/stealth" element={<StealthPage />} />
                    <Route path="/persistence" element={<PersistencePage />} />
                  </Routes>
                </Box>
              </Box>
            </Box>
          </Router>
        </SnackbarProvider>
      </ThemeProvider>
    </QueryClientProvider>
  );
};

export default App;