import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  LinearProgress,
  Alert,
  Tabs,
  Tab
} from '@mui/material';
import {
  CloudDownload,
  Storage,
  Psychology,
  Refresh,
  Delete,
  PlayArrow,
  Stop,
  Info
} from '@mui/icons-material';

const AIAnalysisPage = () => {
  const [tabValue, setTabValue] = useState(0);
  const [models, setModels] = useState([]);
  const [loading, setLoading] = useState(false);
  const [downloadDialogOpen, setDownloadDialogOpen] = useState(false);

  // Mock data for demonstration
  const mockModels = [
    {
      name: 'malware-detection-model',
      type: 'classification',
      description: 'Advanced malware detection using PE file analysis',
      downloaded: true,
      loaded: false,
      size: '245 MB',
      accuracy: 0.94
    },
    {
      name: 'network-intrusion-detection',
      type: 'anomaly_detection',
      description: 'Network traffic anomaly detection system',
      downloaded: true,
      loaded: true,
      size: '180 MB',
      accuracy: 0.91
    },
    {
      name: 'log-anomaly-detection',
      type: 'nlp_anomaly',
      description: 'System log anomaly detection using NLP',
      downloaded: false,
      loaded: false,
      size: '320 MB',
      accuracy: 0.87
    }
  ];

  useEffect(() => {
    setModels(mockModels);
  }, []);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleDownloadModel = (modelName) => {
    setLoading(true);
    // Simulate download
    setTimeout(() => {
      setModels(prev => prev.map(model => 
        model.name === modelName 
          ? { ...model, downloaded: true }
          : model
      ));
      setLoading(false);
    }, 3000);
  };

  const handleLoadModel = (modelName) => {
    setModels(prev => prev.map(model => 
      model.name === modelName 
        ? { ...model, loaded: !model.loaded }
        : model
    ));
  };

  const getModelTypeColor = (type) => {
    switch (type) {
      case 'classification':
        return 'primary';
      case 'anomaly_detection':
        return 'secondary';
      case 'nlp_anomaly':
        return 'warning';
      default:
        return 'default';
    }
  };

  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="h3" sx={{ fontWeight: 600, mb: 1 }}>
          AI Analysis
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          Manage AI models and perform intelligent analysis
        </Typography>
      </Box>

      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange}>
          <Tab label="Model Management" />
          <Tab label="Malware Analysis" />
          <Tab label="Network Analysis" />
          <Tab label="Log Analysis" />
        </Tabs>
      </Box>

      {/* Model Management Tab */}
      {tabValue === 0 && (
        <Grid container spacing={3}>
          {/* Model Statistics */}
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2 }}>
                  Model Statistics
                </Typography>
                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" color="text.secondary">
                    Downloaded Models
                  </Typography>
                  <Typography variant="h4" sx={{ fontWeight: 600 }}>
                    {models.filter(m => m.downloaded).length} / {models.length}
                  </Typography>
                </Box>
                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" color="text.secondary">
                    Active Models
                  </Typography>
                  <Typography variant="h4" sx={{ fontWeight: 600 }}>
                    {models.filter(m => m.loaded).length}
                  </Typography>
                </Box>
                <LinearProgress 
                  variant="determinate" 
                  value={(models.filter(m => m.downloaded).length / models.length) * 100}
                  sx={{ height: 8, borderRadius: 4 }}
                />
              </CardContent>
            </Card>
          </Grid>

          {/* Quick Actions */}
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2 }}>
                  Quick Actions
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={6} md={3}>
                    <Button
                      fullWidth
                      variant="outlined"
                      startIcon={<CloudDownload />}
                      onClick={() => setDownloadDialogOpen(true)}
                    >
                      Download All
                    </Button>
                  </Grid>
                  <Grid item xs={6} md={3}>
                    <Button
                      fullWidth
                      variant="outlined"
                      startIcon={<Refresh />}
                    >
                      Refresh
                    </Button>
                  </Grid>
                  <Grid item xs={6} md={3}>
                    <Button
                      fullWidth
                      variant="outlined"
                      startIcon={<PlayArrow />}
                    >
                      Load All
                    </Button>
                  </Grid>
                  <Grid item xs={6} md={3}>
                    <Button
                      fullWidth
                      variant="outlined"
                      startIcon={<Stop />}
                    >
                      Unload All
                    </Button>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Grid>

          {/* Models Table */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2 }}>
                  Available Models
                </Typography>
                
                {loading && (
                  <Alert severity="info" sx={{ mb: 2 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                      <Typography>Downloading model...</Typography>
                      <LinearProgress sx={{ flexGrow: 1 }} />
                    </Box>
                  </Alert>
                )}

                <TableContainer component={Paper} sx={{ backgroundColor: 'background.paper' }}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Model Name</TableCell>
                        <TableCell>Type</TableCell>
                        <TableCell>Description</TableCell>
                        <TableCell>Size</TableCell>
                        <TableCell>Accuracy</TableCell>
                        <TableCell>Status</TableCell>
                        <TableCell>Actions</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {models.map((model) => (
                        <TableRow key={model.name}>
                          <TableCell>
                            <Typography variant="body2" sx={{ fontWeight: 500 }}>
                              {model.name}
                            </Typography>
                          </TableCell>
                          <TableCell>
                            <Chip 
                              label={model.type}
                              color={getModelTypeColor(model.type)}
                              size="small"
                            />
                          </TableCell>
                          <TableCell>
                            <Typography variant="body2" color="text.secondary">
                              {model.description}
                            </Typography>
                          </TableCell>
                          <TableCell>{model.size}</TableCell>
                          <TableCell>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              <Typography variant="body2">
                                {(model.accuracy * 100).toFixed(1)}%
                              </Typography>
                              <LinearProgress 
                                variant="determinate" 
                                value={model.accuracy * 100}
                                sx={{ width: 60, height: 4 }}
                              />
                            </Box>
                          </TableCell>
                          <TableCell>
                            <Box sx={{ display: 'flex', gap: 1 }}>
                              {!model.downloaded && (
                                <Chip label="Not Downloaded" color="error" size="small" />
                              )}
                              {model.downloaded && !model.loaded && (
                                <Chip label="Downloaded" color="warning" size="small" />
                              )}
                              {model.loaded && (
                                <Chip label="Active" color="success" size="small" />
                              )}
                            </Box>
                          </TableCell>
                          <TableCell>
                            <Box sx={{ display: 'flex', gap: 1 }}>
                              {!model.downloaded ? (
                                <IconButton
                                  size="small"
                                  onClick={() => handleDownloadModel(model.name)}
                                  disabled={loading}
                                >
                                  <CloudDownload />
                                </IconButton>
                              ) : (
                                <>
                                  <IconButton
                                    size="small"
                                    onClick={() => handleLoadModel(model.name)}
                                    color={model.loaded ? "error" : "primary"}
                                  >
                                    {model.loaded ? <Stop /> : <PlayArrow />}
                                  </IconButton>
                                  <IconButton size="small" color="error">
                                    <Delete />
                                  </IconButton>
                                </>
                              )}
                              <IconButton size="small">
                                <Info />
                              </IconButton>
                            </Box>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Other tabs would be implemented similarly */}
      {tabValue === 1 && (
        <Card>
          <CardContent>
            <Typography variant="h6">Malware Analysis</Typography>
            <Typography color="text.secondary">
              Upload files for AI-powered malware detection and analysis.
            </Typography>
          </CardContent>
        </Card>
      )}

      {tabValue === 2 && (
        <Card>
          <CardContent>
            <Typography variant="h6">Network Analysis</Typography>
            <Typography color="text.secondary">
              Analyze network traffic for intrusions and anomalies.
            </Typography>
          </CardContent>
        </Card>
      )}

      {tabValue === 3 && (
        <Card>
          <CardContent>
            <Typography variant="h6">Log Analysis</Typography>
            <Typography color="text.secondary">
              Intelligent analysis of system and application logs.
            </Typography>
          </CardContent>
        </Card>
      )}

      {/* Download Dialog */}
      <Dialog open={downloadDialogOpen} onClose={() => setDownloadDialogOpen(false)}>
        <DialogTitle>Download All Models</DialogTitle>
        <DialogContent>
          <Typography>
            This will download all available AI models from Kaggle. This may take several minutes
            and require significant disk space.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDownloadDialogOpen(false)}>Cancel</Button>
          <Button 
            variant="contained" 
            onClick={() => {
              setDownloadDialogOpen(false);
              // Implement download all logic
            }}
          >
            Download All
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default AIAnalysisPage;