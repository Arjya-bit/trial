import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  Chip,
  Button,
} from '@mui/material';
import { c2API } from '../services/api';

function C2Page() {
  const [implants, setImplants] = useState([]);

  useEffect(() => {
    fetchImplants();
    const interval = setInterval(fetchImplants, 10000);
    return () => clearInterval(interval);
  }, []);

  const fetchImplants = async () => {
    try {
      const response = await c2API.getImplants();
      setImplants(response.data.data);
    } catch (error) {
      console.error('Error fetching implants:', error);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        C2 Command & Control
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Active Implants
            </Typography>
            {implants.length === 0 ? (
              <Typography color="textSecondary">No active implants</Typography>
            ) : (
              <Grid container spacing={2}>
                {implants.map((implant) => (
                  <Grid item xs={12} md={4} key={implant.id}>
                    <Card>
                      <CardContent>
                        <Typography variant="h6">{implant.hostname}</Typography>
                        <Typography variant="body2" color="textSecondary">
                          IP: {implant.ip_address}
                        </Typography>
                        <Typography variant="body2" color="textSecondary">
                          OS: {implant.os}
                        </Typography>
                        <Typography variant="body2" color="textSecondary">
                          User: {implant.username}
                        </Typography>
                        <Chip
                          label={implant.status}
                          color={implant.status === 'active' ? 'success' : 'default'}
                          size="small"
                          sx={{ mt: 1 }}
                        />
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default C2Page;
