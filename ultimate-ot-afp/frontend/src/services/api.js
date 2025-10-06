import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Forensics API
export const forensicsAPI = {
  createDiskImage: (data) => api.post('/forensics/disk-image', data),
  carveFiles: (data) => api.post('/forensics/file-carving', data),
  getCases: () => api.get('/forensics/cases'),
  createCase: (name, description) => api.post('/forensics/cases', { case_name: name, description }),
};

// AI Analysis API
export const aiAPI = {
  predict: (features) => api.post('/ai/predict', { features }),
  analyzeNetwork: (packetData) => api.post('/ai/analyze-network', { packet_data: packetData }),
  analyzeMalware: (features) => api.post('/ai/analyze-malware', features),
  getAvailableModels: () => api.get('/ai/models/available'),
  downloadModel: (modelKey) => api.post('/ai/models/download', { model_key: modelKey }),
  loadModel: (modelFile) => api.post('/ai/models/load', { model_file: modelFile }),
};

// C2 API
export const c2API = {
  getImplants: (status) => api.get('/c2/implants', { params: { status } }),
  getImplantDetails: (implantId) => api.get(`/c2/implants/${implantId}`),
  sendTask: (implantId, task) => api.post(`/c2/implants/${implantId}/tasks`, task),
  removeImplant: (implantId) => api.delete(`/c2/implants/${implantId}`),
};

// Task Manager API
export const taskManagerAPI = {
  getProcesses: () => api.get('/task-manager/processes'),
  getProcessDetails: (pid) => api.get(`/task-manager/processes/${pid}`),
  killProcess: (pid, force) => api.delete(`/task-manager/processes/${pid}`, { params: { force } }),
  getSuspiciousProcesses: () => api.get('/task-manager/processes/analyze/suspicious'),
  getSystemStats: () => api.get('/task-manager/system/stats'),
};

// Network Security API
export const networkAPI = {
  analyzePacket: (packet) => api.post('/network/analyze-packet', packet),
  getIDSAlerts: (severity, limit) => api.get('/network/ids/alerts', { params: { severity, limit } }),
  getIDSStatistics: () => api.get('/network/ids/statistics'),
  addCustomRule: (rule) => api.post('/network/ids/rules', rule),
};

// OT Security API
export const otSecurityAPI = {
  analyzeModbusPacket: (packet) => api.post('/ot-security/modbus/analyze', packet),
  getOTDevices: () => api.get('/ot-security/devices'),
  getSupportedProtocols: () => api.get('/ot-security/protocols/supported'),
};

// Autonomous API
export const autonomousAPI = {
  start: () => api.post('/autonomous/start'),
  stop: () => api.post('/autonomous/stop'),
  getTaskStatus: (taskId) => api.get(`/autonomous/tasks/${taskId}`),
  enableTask: (taskId) => api.post(`/autonomous/tasks/${taskId}/enable`),
  disableTask: (taskId) => api.post(`/autonomous/tasks/${taskId}/disable`),
  getExecutionLog: (limit) => api.get('/autonomous/logs', { params: { limit } }),
};

// Persistence API
export const persistenceAPI = {
  install: (data) => api.post('/persistence/install', data),
  getMechanisms: () => api.get('/persistence/mechanisms'),
  remove: (mechanismId) => api.delete(`/persistence/mechanisms/${mechanismId}`),
};

// Stealth API
export const stealthAPI = {
  enable: (config) => api.post('/stealth/enable', config),
  disable: () => api.post('/stealth/disable'),
  getStatus: () => api.get('/stealth/status'),
};

export default api;
