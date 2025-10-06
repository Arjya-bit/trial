import React, { useState } from 'react';
import { Box, Typography, Paper, Button, Grid } from '@mui/material';
import { autonomousAPI } from '../services/api';

function AutonomousPage() {
  const [running, setRunning] = useState(false);

  const handleStart = async () => {
    try {
      await autonomousAPI.start();
      setRunning(true);
      alert('Autonomous engine started');
    } catch (error) {
      console.error('Error starting autonomous engine:', error);
    }
  };

  const handleStop = async () => {
    try {
      await autonomousAPI.stop();
      setRunning(false);
      alert('Autonomous engine stopped');
    } catch (error) {
      console.error('Error stopping autonomous engine:', error);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Autonomous Operations
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Autonomous Engine Control
            </Typography>
            <Typography variant="body2" color="textSecondary" paragraph>
              The autonomous engine automatically executes security tasks based on triggers.
            </Typography>
            <Button
              variant="contained"
              color={running ? 'error' : 'primary'}
              onClick={running ? handleStop : handleStart}
            >
              {running ? 'Stop Engine' : 'Start Engine'}
            </Button>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default AutonomousPage;
