import React from 'react';
import { Box, Typography, Paper } from '@mui/material';

function StealthPage() {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Stealth Operations
      </Typography>
      <Paper sx={{ p: 3 }}>
        <Typography variant="body1">
          Configure stealth and evasion techniques
        </Typography>
      </Paper>
    </Box>
  );
}

export default StealthPage;
