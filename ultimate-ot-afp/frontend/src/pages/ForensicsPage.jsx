import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Button,
  TextField,
  Grid,
  Card,
  CardContent,
} from '@mui/material';
import { forensicsAPI } from '../services/api';

function ForensicsPage() {
  const [sourcePath, setSourcePath] = useState('');
  const [imageName, setImageName] = useState('');
  const [loading, setLoading] = useState(false);

  const handleCreateImage = async () => {
    setLoading(true);
    try {
      const response = await forensicsAPI.createDiskImage({
        source_path: sourcePath,
        image_name: imageName,
        format: 'raw',
        verify: true,
      });
      console.log('Disk image created:', response.data);
      alert('Disk image created successfully!');
    } catch (error) {
      console.error('Error creating disk image:', error);
      alert('Error creating disk image');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Digital Forensics
      </Typography>

      <Grid container spacing={3}>
        {/* Disk Imaging */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Disk Imaging
            </Typography>
            <TextField
              fullWidth
              label="Source Path"
              value={sourcePath}
              onChange={(e) => setSourcePath(e.target.value)}
              margin="normal"
            />
            <TextField
              fullWidth
              label="Image Name"
              value={imageName}
              onChange={(e) => setImageName(e.target.value)}
              margin="normal"
            />
            <Button
              variant="contained"
              onClick={handleCreateImage}
              disabled={loading}
              sx={{ mt: 2 }}
            >
              Create Disk Image
            </Button>
          </Paper>
        </Grid>

        {/* File Carving */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              File Carving
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Recover deleted files from disk images
            </Typography>
            <Button variant="contained" sx={{ mt: 2 }}>
              Start File Carving
            </Button>
          </Paper>
        </Grid>

        {/* Forensic Cases */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Forensic Cases
            </Typography>
            <Typography variant="body2" color="textSecondary">
              No active cases
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default ForensicsPage;
