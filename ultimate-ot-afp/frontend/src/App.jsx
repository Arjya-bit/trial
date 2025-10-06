import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Box } from '@mui/material';
import Sidebar from './components/Common/Sidebar';
import Dashboard from './pages/Dashboard';
import ForensicsPage from './pages/ForensicsPage';
import NetworkSecurityPage from './pages/NetworkSecurityPage';
import OTSecurityPage from './pages/OTSecurityPage';
import TaskManagerPage from './pages/TaskManagerPage';
import AutonomousPage from './pages/AutonomousPage';
import AIAnalysisPage from './pages/AIAnalysisPage';
import C2Page from './pages/C2Page';
import PersistencePage from './pages/PersistencePage';
import StealthPage from './pages/StealthPage';

function App() {
  return (
    <Box sx={{ display: 'flex' }}>
      <Sidebar />
      <Box component="main" sx={{ flexGrow: 1, p: 3, mt: 8 }}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/forensics" element={<ForensicsPage />} />
          <Route path="/network-security" element={<NetworkSecurityPage />} />
          <Route path="/ot-security" element={<OTSecurityPage />} />
          <Route path="/task-manager" element={<TaskManagerPage />} />
          <Route path="/autonomous" element={<AutonomousPage />} />
          <Route path="/ai-analysis" element={<AIAnalysisPage />} />
          <Route path="/c2" element={<C2Page />} />
          <Route path="/persistence" element={<PersistencePage />} />
          <Route path="/stealth" element={<StealthPage />} />
        </Routes>
      </Box>
    </Box>
  );
}

export default App;
