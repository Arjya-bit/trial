import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Button,
  Card,
  CardContent,
  CardActions,
} from '@mui/material';
import { aiAPI } from '../services/api';

function AIAnalysisPage() {
  const [models, setModels] = useState({});
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchAvailableModels();
  }, []);

  const fetchAvailableModels = async () => {
    try {
      const response = await aiAPI.getAvailableModels();
      setModels(response.data.models);
    } catch (error) {
      console.error('Error fetching models:', error);
    }
  };

  const handleDownloadModel = async (modelKey) => {
    setLoading(true);
    try {
      await aiAPI.downloadModel(modelKey);
      alert(`Downloading model: ${modelKey}`);
    } catch (error) {
      console.error('Error downloading model:', error);
      alert('Error downloading model');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        AI Analysis
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Available AI Models
            </Typography>
            <Grid container spacing={2}>
              {Object.entries(models).map(([key, model]) => (
                <Grid item xs={12} md={4} key={key}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6">{key}</Typography>
                      <Typography variant="body2" color="textSecondary">
                        {model.description}
                      </Typography>
                      <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                        Type: {model.type}
                      </Typography>
                      <Typography variant="caption" display="block">
                        Dataset: {model.dataset}
                      </Typography>
                    </CardContent>
                    <CardActions>
                      <Button
                        size="small"
                        onClick={() => handleDownloadModel(key)}
                        disabled={loading}
                      >
                        Download
                      </Button>
                    </CardActions>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              AI-Powered Analysis
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Use machine learning models to analyze network traffic, detect malware, and identify threats.
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default AIAnalysisPage;
