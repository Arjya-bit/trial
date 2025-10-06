import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  LinearProgress,
  Chip,
  IconButton,
  Paper,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Avatar,
  Divider,
  Button,
  Alert
} from '@mui/material';
import {
  Security,
  NetworkCheck,
  Biotech,
  Psychology,
  SmartToy,
  Warning,
  CheckCircle,
  Error,
  Info,
  Refresh,
  Timeline,
  Speed,
  Storage,
  Memory
} from '@mui/icons-material';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';

// Sample data for demonstration
const systemMetrics = {
  cpu: 68,
  memory: 72,
  disk: 45,
  network: 23
};

const securityAlerts = [
  {
    id: 1,
    type: 'high',
    title: 'Suspicious Network Activity',
    description: 'Multiple failed login attempts detected from external IP',
    timestamp: '2024-01-15 10:30:22',
    source: 'Network Security'
  },
  {
    id: 2,
    type: 'medium',
    title: 'Anomalous Process Detected',
    description: 'Unknown process consuming high CPU resources',
    timestamp: '2024-01-15 10:25:15',
    source: 'AI Analysis'
  },
  {
    id: 3,
    type: 'low',
    title: 'OT Device Offline',
    description: 'Modbus device 192.168.1.50 not responding',
    timestamp: '2024-01-15 10:20:08',
    source: 'OT Security'
  }
];

const activityData = [
  { time: '00:00', forensics: 12, network: 8, ot: 4, ai: 15 },
  { time: '04:00', forensics: 19, network: 12, ot: 7, ai: 22 },
  { time: '08:00', forensics: 35, network: 28, ot: 18, ai: 45 },
  { time: '12:00', forensics: 42, network: 35, ot: 25, ai: 52 },
  { time: '16:00', forensics: 38, network: 32, ot: 22, ai: 48 },
  { time: '20:00', forensics: 25, network: 18, ot: 12, ai: 30 }
];

const moduleStats = [
  { name: 'Digital Forensics', value: 35, color: '#00d4aa' },
  { name: 'Network Security', value: 28, color: '#6c5ce7' },
  { name: 'OT Security', value: 22, color: '#fd79a8' },
  { name: 'AI Analysis', value: 15, color: '#fdcb6e' }
];

const Dashboard = () => {
  const [refreshing, setRefreshing] = useState(false);
  const [systemStatus, setSystemStatus] = useState('operational');

  const handleRefresh = async () => {
    setRefreshing(true);
    // Simulate data refresh
    setTimeout(() => {
      setRefreshing(false);
    }, 2000);
  };

  const getAlertIcon = (type) => {
    switch (type) {
      case 'high':
        return <Error color="error" />;
      case 'medium':
        return <Warning color="warning" />;
      case 'low':
        return <Info color="info" />;
      default:
        return <Info />;
    }
  };

  const getAlertColor = (type) => {
    switch (type) {
      case 'high':
        return 'error';
      case 'medium':
        return 'warning';
      case 'low':
        return 'info';
      default:
        return 'default';
    }
  };

  return (
    <Box className="fade-in">
      {/* Header */}
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box>
          <Typography variant="h3" sx={{ fontWeight: 600, mb: 1 }}>
            Dashboard
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            Ultimate OT-AFP Platform Overview
          </Typography>
        </Box>
        
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Chip 
            label={systemStatus === 'operational' ? 'All Systems Operational' : 'System Alert'}
            color={systemStatus === 'operational' ? 'success' : 'error'}
            icon={systemStatus === 'operational' ? <CheckCircle /> : <Error />}
            sx={{ px: 2 }}
          />
          <IconButton 
            onClick={handleRefresh}
            disabled={refreshing}
            sx={{ 
              background: 'rgba(0, 212, 170, 0.1)',
              '&:hover': { background: 'rgba(0, 212, 170, 0.2)' }
            }}
          >
            <Refresh sx={{ color: 'primary.main' }} />
          </IconButton>
        </Box>
      </Box>

      <Grid container spacing={3}>
        {/* System Metrics Cards */}
        <Grid item xs={12} md={3}>
          <Card className="hover-lift">
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>
                  <Speed />
                </Avatar>
                <Box>
                  <Typography variant="h6">CPU Usage</Typography>
                  <Typography variant="body2" color="text.secondary">
                    Current Load
                  </Typography>
                </Box>
              </Box>
              <Box sx={{ mb: 1 }}>
                <Typography variant="h4" sx={{ fontWeight: 600 }}>
                  {systemMetrics.cpu}%
                </Typography>
              </Box>
              <LinearProgress 
                variant="determinate" 
                value={systemMetrics.cpu} 
                sx={{ 
                  height: 8, 
                  borderRadius: 4,
                  backgroundColor: 'rgba(0, 212, 170, 0.1)',
                  '& .MuiLinearProgress-bar': {
                    backgroundColor: systemMetrics.cpu > 80 ? '#f85149' : '#00d4aa'
                  }
                }}
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card className="hover-lift">
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Avatar sx={{ bgcolor: 'secondary.main', mr: 2 }}>
                  <Memory />
                </Avatar>
                <Box>
                  <Typography variant="h6">Memory</Typography>
                  <Typography variant="body2" color="text.secondary">
                    RAM Usage
                  </Typography>
                </Box>
              </Box>
              <Box sx={{ mb: 1 }}>
                <Typography variant="h4" sx={{ fontWeight: 600 }}>
                  {systemMetrics.memory}%
                </Typography>
              </Box>
              <LinearProgress 
                variant="determinate" 
                value={systemMetrics.memory} 
                sx={{ 
                  height: 8, 
                  borderRadius: 4,
                  backgroundColor: 'rgba(108, 92, 231, 0.1)',
                  '& .MuiLinearProgress-bar': {
                    backgroundColor: systemMetrics.memory > 80 ? '#f85149' : '#6c5ce7'
                  }
                }}
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card className="hover-lift">
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Avatar sx={{ bgcolor: 'warning.main', mr: 2 }}>
                  <Storage />
                </Avatar>
                <Box>
                  <Typography variant="h6">Disk Space</Typography>
                  <Typography variant="body2" color="text.secondary">
                    Storage Used
                  </Typography>
                </Box>
              </Box>
              <Box sx={{ mb: 1 }}>
                <Typography variant="h4" sx={{ fontWeight: 600 }}>
                  {systemMetrics.disk}%
                </Typography>
              </Box>
              <LinearProgress 
                variant="determinate" 
                value={systemMetrics.disk} 
                sx={{ 
                  height: 8, 
                  borderRadius: 4,
                  backgroundColor: 'rgba(240, 136, 62, 0.1)',
                  '& .MuiLinearProgress-bar': {
                    backgroundColor: '#f0883e'
                  }
                }}
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card className="hover-lift">
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Avatar sx={{ bgcolor: 'info.main', mr: 2 }}>
                  <NetworkCheck />
                </Avatar>
                <Box>
                  <Typography variant="h6">Network</Typography>
                  <Typography variant="body2" color="text.secondary">
                    Traffic Load
                  </Typography>
                </Box>
              </Box>
              <Box sx={{ mb: 1 }}>
                <Typography variant="h4" sx={{ fontWeight: 600 }}>
                  {systemMetrics.network}%
                </Typography>
              </Box>
              <LinearProgress 
                variant="determinate" 
                value={systemMetrics.network} 
                sx={{ 
                  height: 8, 
                  borderRadius: 4,
                  backgroundColor: 'rgba(88, 166, 255, 0.1)',
                  '& .MuiLinearProgress-bar': {
                    backgroundColor: '#58a6ff'
                  }
                }}
              />
            </CardContent>
          </Card>
        </Grid>

        {/* Activity Chart */}
        <Grid item xs={12} lg={8}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'between', alignItems: 'center', mb: 3 }}>
                <Typography variant="h6">Activity Timeline</Typography>
                <Chip label="Last 24 Hours" size="small" />
              </Box>
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={activityData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                  <XAxis dataKey="time" stroke="#8b949e" />
                  <YAxis stroke="#8b949e" />
                  <Tooltip 
                    contentStyle={{
                      backgroundColor: '#1a2332',
                      border: '1px solid #30363d',
                      borderRadius: '8px'
                    }}
                  />
                  <Area 
                    type="monotone" 
                    dataKey="forensics" 
                    stackId="1"
                    stroke="#00d4aa" 
                    fill="rgba(0, 212, 170, 0.3)" 
                  />
                  <Area 
                    type="monotone" 
                    dataKey="network" 
                    stackId="1"
                    stroke="#6c5ce7" 
                    fill="rgba(108, 92, 231, 0.3)" 
                  />
                  <Area 
                    type="monotone" 
                    dataKey="ot" 
                    stackId="1"
                    stroke="#fd79a8" 
                    fill="rgba(253, 121, 168, 0.3)" 
                  />
                  <Area 
                    type="monotone" 
                    dataKey="ai" 
                    stackId="1"
                    stroke="#fdcb6e" 
                    fill="rgba(253, 203, 110, 0.3)" 
                  />
                </AreaChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Module Distribution */}
        <Grid item xs={12} lg={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 3 }}>Module Activity Distribution</Typography>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={moduleStats}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {moduleStats.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
              <Box sx={{ mt: 2 }}>
                {moduleStats.map((item, index) => (
                  <Box key={index} sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <Box 
                      sx={{ 
                        width: 12, 
                        height: 12, 
                        backgroundColor: item.color, 
                        borderRadius: 1, 
                        mr: 1 
                      }} 
                    />
                    <Typography variant="body2" sx={{ flexGrow: 1 }}>
                      {item.name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {item.value}%
                    </Typography>
                  </Box>
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Security Alerts */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                <Typography variant="h6">Recent Security Alerts</Typography>
                <Button 
                  variant="outlined" 
                  size="small"
                  sx={{ borderColor: 'primary.main', color: 'primary.main' }}
                >
                  View All
                </Button>
              </Box>
              
              <List>
                {securityAlerts.map((alert, index) => (
                  <React.Fragment key={alert.id}>
                    <ListItem 
                      sx={{ 
                        borderRadius: 2,
                        mb: 1,
                        '&:hover': {
                          backgroundColor: 'rgba(255, 255, 255, 0.05)'
                        }
                      }}
                    >
                      <ListItemIcon>
                        {getAlertIcon(alert.type)}
                      </ListItemIcon>
                      <ListItemText
                        primary={
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                            <Typography variant="subtitle2">{alert.title}</Typography>
                            <Chip 
                              label={alert.type.toUpperCase()} 
                              size="small"
                              color={getAlertColor(alert.type)}
                              sx={{ fontSize: '0.75rem' }}
                            />
                          </Box>
                        }
                        secondary={
                          <Box>
                            <Typography variant="body2" color="text.secondary" sx={{ mb: 0.5 }}>
                              {alert.description}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                              {alert.source} • {alert.timestamp}
                            </Typography>
                          </Box>
                        }
                      />
                    </ListItem>
                    {index < securityAlerts.length - 1 && <Divider />}
                  </React.Fragment>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;