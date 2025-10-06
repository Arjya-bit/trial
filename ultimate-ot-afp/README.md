# Ultimate OT-AFP Platform

**Ultimate Operational Technology - Advanced Forensics Platform**

A comprehensive cybersecurity platform combining digital forensics, network security, OT/ICS security, AI-powered threat analysis, command & control capabilities, and autonomous security operations.

## 🚀 Features

### 🔍 Digital Forensics
- **FTK Emulator**: Disk imaging, file carving, registry analysis
- **Belkasoft Emulator**: Memory forensics, browser analysis, mobile forensics
- **Oxygen Emulator**: Mobile data extraction, social media forensics
- **Autopsy Emulator**: Hash analysis, keyword search, timeline generation
- **Advanced Forensics**: AI-powered analysis, blockchain forensics, malware analysis

### 🌐 Network Security
- **Snort IDS Emulator**: Real-time intrusion detection with custom rules
- **Wireshark Emulator**: Deep packet inspection and protocol analysis
- **BurpSuite Emulator**: Web vulnerability scanning and API testing
- **Wireless Security**: WiFi analysis and security assessment

### 🏭 OT/ICS Security
- **Protocol Analyzers**: Modbus, S7comm, OPC UA, DNP3, BACnet
- **Device Monitoring**: PLC, SCADA, IED monitoring
- **Industrial IDS**: Specialized detection for OT environments

### 🧠 AI-Powered Analysis
- **Kaggle Model Integration**: Download and use pre-trained cybersecurity models
- **Network Traffic Analysis**: ML-based threat detection
- **Malware Classification**: AI-powered malware analysis
- **Anomaly Detection**: Behavioral analysis and threat hunting

### 🎮 Command & Control (C2)
- **Implant Management**: Track and control deployed implants
- **Task Distribution**: Queue and execute remote tasks
- **Secure Communications**: Encrypted C2 channels
- **Heartbeat Monitoring**: Real-time implant health checks

### ⚡ Autonomous Operations
- **Auto-Executor**: Scheduled and trigger-based task execution
- **Continuous Monitoring**: 24/7 automated security scanning
- **Threat Response**: Automated incident response actions
- **Adaptive Learning**: Self-improving security posture

### 📊 Task Manager
- **Process Monitoring**: Real-time process tracking and analysis
- **Performance Metrics**: CPU, memory, disk, and network monitoring
- **Suspicious Process Detection**: AI-powered anomaly detection
- **Resource Management**: System optimization and control

### 🔐 Persistence & Stealth
- **Service Installation**: Windows/Linux service persistence
- **WMI Persistence**: Windows Management Instrumentation hooks
- **Process Hiding**: Advanced evasion techniques
- **AV Evasion**: Anti-detection mechanisms

## 📁 Project Structure

```
ultimate-ot-afp/
├── backend/                    # FastAPI Backend
│   ├── main.py                # Application entry point
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile            # Container configuration
│   └── src/
│       ├── core/             # Core application logic
│       ├── api/              # REST API endpoints
│       ├── modules/          # Feature modules
│       ├── database/         # Database models and clients
│       └── utils/            # Utility functions
├── frontend/                  # React Frontend
│   ├── public/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API services
│   │   └── store/           # Redux store
│   └── package.json
├── Auto_Launcher/            # Automated deployment
├── Command_Control/          # C2 infrastructure
├── Persistence_Engine/       # Persistence mechanisms
├── Stealth_Engine/          # Evasion techniques
├── database/                # Database files
├── docs/                    # Documentation
├── scripts/                 # Utility scripts
└── config/                  # Configuration files
```

## 🛠️ Installation

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis 7+
- Elasticsearch 8+

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run database migrations
alembic upgrade head

# Start backend
python main.py
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
echo "REACT_APP_API_URL=http://localhost:8000/api/v1" > .env
echo "REACT_APP_WS_URL=ws://localhost:8000" >> .env

# Start frontend
npm start
```

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🔧 Configuration

### Kaggle API Setup (for AI Models)

1. Create Kaggle account at https://www.kaggle.com
2. Go to Account → API → Create New API Token
3. Add credentials to `.env`:

```env
KAGGLE_USERNAME=your_username
KAGGLE_KEY=your_api_key
```

### Database Configuration

```env
POSTGRES_USER=otafp_user
POSTGRES_PASSWORD=your_secure_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=otafp_db
```

## 🚦 Usage

### Starting the Platform

```bash
# Backend
cd backend && python main.py

# Frontend
cd frontend && npm start
```

Access the platform at: `http://localhost:3000`

### Downloading AI Models

```python
# Using the API
POST /api/v1/ai/models/download
{
    "model_key": "intrusion_detection"
}
```

### Creating a Forensic Case

```python
POST /api/v1/forensics/cases
{
    "case_name": "Investigation 2025-001",
    "description": "Network intrusion investigation"
}
```

### Deploying C2 Implant

```python
POST /api/v1/c2/register
{
    "hostname": "target-host",
    "ip_address": "192.168.1.100",
    "os": "Windows 10",
    "username": "user",
    "privileges": "user"
}
```

## 📖 API Documentation

Once the backend is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd frontend
npm test
```

## 🔒 Security Notes

⚠️ **IMPORTANT**: This platform includes powerful security tools and should only be used:
- In authorized environments
- For legitimate security testing
- With proper permissions
- For educational purposes

Misuse of these tools may be illegal. Always ensure you have proper authorization.

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines before submitting PRs.

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- Inspired by industry-leading forensic and security tools
- Built with FastAPI, React, and modern cybersecurity frameworks
- Utilizes machine learning models from Kaggle's cybersecurity datasets

## 📞 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check the documentation in `/docs`
- Review API documentation at `/api/docs`

## 🗺️ Roadmap

- [ ] Additional forensic tool emulators
- [ ] Enhanced AI model training capabilities
- [ ] Mobile app for remote monitoring
- [ ] Integration with SIEM platforms
- [ ] Advanced threat intelligence feeds
- [ ] Automated penetration testing
- [ ] Blockchain forensics expansion
- [ ] IoT device security analysis

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    React Frontend                        │
│  Dashboard │ Forensics │ Network │ OT │ AI │ C2 │ Auto  │
└─────────────────┬───────────────────────────────────────┘
                  │ REST API + WebSocket
┌─────────────────┴───────────────────────────────────────┐
│                   FastAPI Backend                        │
│  ┌─────────┬─────────┬─────────┬─────────┬─────────┐   │
│  │Forensics│ Network │   OT    │   AI    │   C2    │   │
│  │ Module  │ Security│ Security│ Analysis│ Server  │   │
│  └─────────┴─────────┴─────────┴─────────┴─────────┘   │
└─────────────────┬───────────────────────────────────────┘
                  │
┌─────────────────┴───────────────────────────────────────┐
│              Data Layer                                  │
│  PostgreSQL  │  Redis  │  Elasticsearch  │  AI Models   │
└─────────────────────────────────────────────────────────┘
```

---

**Built with ❤️ for the cybersecurity community**
