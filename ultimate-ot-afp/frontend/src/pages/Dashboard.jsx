import React, { useEffect, useState } from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
} from '@mui/material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { taskManagerAPI } from '../services/api';
import websocketService from '../services/websocket';

function Dashboard() {
  const [systemStats, setSystemStats] = useState(null);
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    // Fetch initial system stats
    fetchSystemStats();

    // Connect to WebSocket for real-time updates
    websocketService.connect();
    websocketService.subscribe('metrics');
    websocketService.subscribe('alerts');

    websocketService.on('metrics', handleMetricsUpdate);
    websocketService.on('alert', handleAlertUpdate);

    return () => {
      websocketService.off('metrics', handleMetricsUpdate);
      websocketService.off('alert', handleAlertUpdate);
    };
  }, []);

  const fetchSystemStats = async () => {
    try {
      const response = await taskManagerAPI.getSystemStats();
      setSystemStats(response.data.data);
    } catch (error) {
      console.error('Error fetching system stats:', error);
    }
  };

  const handleMetricsUpdate = (data) => {
    console.log('Metrics update:', data);
  };

  const handleAlertUpdate = (data) => {
    setAlerts((prev) => [data.data, ...prev].slice(0, 10));
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>

      <Grid container spacing={3}>
        {/* System Stats Cards */}
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                CPU Usage
              </Typography>
              <Typography variant="h3">
                {systemStats?.cpu_percent?.toFixed(1) || 0}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Memory Usage
              </Typography>
              <Typography variant="h3">
                {systemStats?.memory?.percent?.toFixed(1) || 0}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Disk Usage
              </Typography>
              <Typography variant="h3">
                {systemStats?.disk?.percent?.toFixed(1) || 0}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Active Processes
              </Typography>
              <Typography variant="h3">
                {systemStats?.process_count || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Performance Chart */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              System Performance
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={[]}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="cpu" stroke="#8884d8" />
                <Line type="monotone" dataKey="memory" stroke="#82ca9d" />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Recent Alerts */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Recent Alerts
            </Typography>
            {alerts.length === 0 ? (
              <Typography color="textSecondary">No recent alerts</Typography>
            ) : (
              alerts.map((alert, index) => (
                <Box key={index} sx={{ mb: 2 }}>
                  <Typography variant="body1">{alert.title}</Typography>
                  <Typography variant="body2" color="textSecondary">
                    {alert.description}
                  </Typography>
                </Box>
              ))
            )}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default Dashboard;
