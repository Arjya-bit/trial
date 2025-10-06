import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Chip,
} from '@mui/material';
import { Delete as DeleteIcon } from '@mui/icons-material';
import { taskManagerAPI } from '../services/api';

function TaskManagerPage() {
  const [processes, setProcesses] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchProcesses();
    const interval = setInterval(fetchProcesses, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchProcesses = async () => {
    try {
      const response = await taskManagerAPI.getProcesses();
      setProcesses(response.data.data.slice(0, 20));
    } catch (error) {
      console.error('Error fetching processes:', error);
    }
  };

  const handleKillProcess = async (pid) => {
    if (window.confirm(`Kill process ${pid}?`)) {
      try {
        await taskManagerAPI.killProcess(pid, false);
        fetchProcesses();
      } catch (error) {
        console.error('Error killing process:', error);
      }
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Task Manager
      </Typography>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Running Processes
        </Typography>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>PID</TableCell>
                <TableCell>Name</TableCell>
                <TableCell>Username</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>CPU %</TableCell>
                <TableCell>Memory %</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {processes.map((proc) => (
                <TableRow key={proc.pid}>
                  <TableCell>{proc.pid}</TableCell>
                  <TableCell>{proc.name}</TableCell>
                  <TableCell>{proc.username}</TableCell>
                  <TableCell>
                    <Chip label={proc.status} size="small" />
                  </TableCell>
                  <TableCell>{proc.cpu_percent?.toFixed(1)}%</TableCell>
                  <TableCell>{proc.memory_percent?.toFixed(1)}%</TableCell>
                  <TableCell>
                    <IconButton
                      size="small"
                      onClick={() => handleKillProcess(proc.pid)}
                      color="error"
                    >
                      <DeleteIcon />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </Box>
  );
}

export default TaskManagerPage;
