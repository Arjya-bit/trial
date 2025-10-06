import React, { useState, useEffect } from 'react';
import { Box, Typography, Paper, Grid, Chip } from '@mui/material';
import { otSecurityAPI } from '../services/api';

function OTSecurityPage() {
  const [devices, setDevices] = useState([]);
  const [protocols, setProtocols] = useState([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [devicesRes, protocolsRes] = await Promise.all([
        otSecurityAPI.getOTDevices(),
        otSecurityAPI.getSupportedProtocols(),
      ]);
      setDevices(devicesRes.data.data);
      setProtocols(protocolsRes.data.protocols);
    } catch (error) {
      console.error('Error fetching OT security data:', error);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        OT Security
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              OT Devices
            </Typography>
            <Grid container spacing={2}>
              {devices.map((device) => (
                <Grid item xs={12} md={4} key={device.id}>
                  <Paper sx={{ p: 2 }}>
                    <Typography variant="h6">{device.id}</Typography>
                    <Typography variant="body2">Type: {device.type}</Typography>
                    <Chip label={device.status} color="success" size="small" sx={{ mt: 1 }} />
                  </Paper>
                </Grid>
              ))}
            </Grid>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Supported Protocols
            </Typography>
            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
              {protocols.map((protocol) => (
                <Chip key={protocol} label={protocol.toUpperCase()} />
              ))}
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default OTSecurityPage;
