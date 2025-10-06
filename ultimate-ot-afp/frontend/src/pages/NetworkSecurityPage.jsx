import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
} from '@mui/material';
import { networkAPI } from '../services/api';

function NetworkSecurityPage() {
  const [alerts, setAlerts] = useState([]);
  const [statistics, setStatistics] = useState(null);

  useEffect(() => {
    fetchAlerts();
    fetchStatistics();
  }, []);

  const fetchAlerts = async () => {
    try {
      const response = await networkAPI.getIDSAlerts(null, 50);
      setAlerts(response.data.data);
    } catch (error) {
      console.error('Error fetching alerts:', error);
    }
  };

  const fetchStatistics = async () => {
    try {
      const response = await networkAPI.getIDSStatistics();
      setStatistics(response.data.data);
    } catch (error) {
      console.error('Error fetching statistics:', error);
    }
  };

  const getSeverityColor = (severity) => {
    const colors = {
      critical: 'error',
      high: 'warning',
      medium: 'info',
      low: 'default',
    };
    return colors[severity] || 'default';
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Network Security
      </Typography>

      <Grid container spacing={3}>
        {/* IDS Statistics */}
        {statistics && (
          <>
            <Grid item xs={12} md={3}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6">{statistics.total_alerts}</Typography>
                <Typography variant="body2" color="textSecondary">
                  Total Alerts
                </Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} md={3}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6">{statistics.active_rules}</Typography>
                <Typography variant="body2" color="textSecondary">
                  Active Rules
                </Typography>
              </Paper>
            </Grid>
          </>
        )}

        {/* IDS Alerts Table */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Recent IDS Alerts
            </Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Rule Name</TableCell>
                    <TableCell>Severity</TableCell>
                    <TableCell>Source IP</TableCell>
                    <TableCell>Destination IP</TableCell>
                    <TableCell>Timestamp</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {alerts.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={5} align="center">
                        No alerts
                      </TableCell>
                    </TableRow>
                  ) : (
                    alerts.map((alert, index) => (
                      <TableRow key={index}>
                        <TableCell>{alert.rule_name}</TableCell>
                        <TableCell>
                          <Chip
                            label={alert.severity}
                            color={getSeverityColor(alert.severity)}
                            size="small"
                          />
                        </TableCell>
                        <TableCell>{alert.source_ip}</TableCell>
                        <TableCell>{alert.destination_ip}</TableCell>
                        <TableCell>{new Date(alert.timestamp).toLocaleString()}</TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default NetworkSecurityPage;
