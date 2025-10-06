# Ultimate OT-AFP Platform - Complete Project Structure

## 📂 Full Directory Tree

```
ultimate-ot-afp/
│
├── backend/                                    # Backend API Server
│   ├── main.py                                # Application entry point
│   ├── requirements.txt                       # Python dependencies
│   ├── Dockerfile                            # Backend container config
│   ├── .env.example                          # Environment template
│   │
│   ├── src/
│   │   ├── core/                             # Core application
│   │   │   ├── __init__.py
│   │   │   ├── app.py                        # FastAPI app factory
│   │   │   ├── config.py                     # Configuration management
│   │   │   ├── database.py                   # Database setup
│   │   │   └── security.py                   # Authentication & security
│   │   │
│   │   ├── api/                              # API layer
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── routers.py                # API router aggregator
│   │   │   │   └── endpoints/                # API endpoints
│   │   │   │       ├── __init__.py
│   │   │   │       ├── forensics.py          # Forensics endpoints
│   │   │   │       ├── ai_analysis.py        # AI analysis endpoints
│   │   │   │       ├── persistence.py        # Persistence endpoints
│   │   │   │       ├── stealth.py            # Stealth endpoints
│   │   │   │       ├── network_security.py   # Network security endpoints
│   │   │   │       ├── ot_security.py        # OT security endpoints
│   │   │   │       ├── c2.py                 # C2 endpoints
│   │   │   │       ├── task_manager.py       # Task manager endpoints
│   │   │   │       └── autonomous.py         # Autonomous endpoints
│   │   │   │
│   │   │   └── websocket/                    # WebSocket layer
│   │   │       ├── __init__.py
│   │   │       └── realtime.py               # Real-time communications
│   │   │
│   │   ├── database/                         # Database layer
│   │   │   ├── __init__.py
│   │   │   ├── redis_client.py               # Redis client
│   │   │   ├── elasticsearch_client.py       # Elasticsearch client
│   │   │   └── models/                       # SQLAlchemy models
│   │   │       ├── __init__.py
│   │   │       ├── c2.py                     # C2 models
│   │   │       ├── forensics.py              # Forensics models
│   │   │       ├── network_security.py       # Network security models
│   │   │       └── task_manager.py           # Task manager models
│   │   │
│   │   ├── modules/                          # Feature modules
│   │   │   │
│   │   │   ├── admin_escalation/             # 🆕 Admin escalation
│   │   │   │   └── admin_escalator.py
│   │   │   │
│   │   │   ├── ai_model/                     # 🧠 AI model integration
│   │   │   │   ├── __init__.py
│   │   │   │   ├── model_downloader.py       # Kaggle model downloader
│   │   │   │   ├── model_inference.py        # Inference engine
│   │   │   │   ├── model_trainer.py          # Model training
│   │   │   │   └── config.json               # AI config
│   │   │   │
│   │   │   ├── ai/                           # AI analysis
│   │   │   │   └── ai_analysis.py
│   │   │   │
│   │   │   ├── autonomous/                   # ⚡ Autonomous operations
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auto_executor.py          # Task executor
│   │   │   │   ├── persistence_manager.py
│   │   │   │   └── continuous_forensics.py
│   │   │   │
│   │   │   ├── c2/                           # 🎮 Command & Control
│   │   │   │   ├── __init__.py
│   │   │   │   ├── c2_server.py              # C2 server
│   │   │   │   ├── implant_comms.py
│   │   │   │   └── task_distributor.py
│   │   │   │
│   │   │   ├── forensics/                    # 🔍 Digital forensics
│   │   │   │   ├── __init__.py
│   │   │   │   ├── ftk_emulator/             # FTK emulator
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── disk_imaging.py
│   │   │   │   │   ├── file_carving.py
│   │   │   │   │   └── registry_analyzer.py
│   │   │   │   ├── belkasoft_emulator/       # Belkasoft emulator
│   │   │   │   ├── oxygen_emulator/          # Oxygen emulator
│   │   │   │   ├── autopsy_emulator/         # Autopsy emulator
│   │   │   │   ├── advanced_forensics/       # Advanced forensics
│   │   │   │   ├── mobile/                   # Mobile forensics
│   │   │   │   └── social_media/             # Social media forensics
│   │   │   │
│   │   │   ├── network_security/             # 🌐 Network security
│   │   │   │   ├── __init__.py
│   │   │   │   ├── snort_emulator/           # Snort IDS
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── intrusion_detection.py
│   │   │   │   ├── wireshark_emulator/       # Wireshark
│   │   │   │   ├── burpsuite_emulator/       # BurpSuite
│   │   │   │   └── wireless/                 # Wireless security
│   │   │   │
│   │   │   ├── ot_security/                  # 🏭 OT/ICS security
│   │   │   │   ├── protocol_analyzers/       # Protocol analyzers
│   │   │   │   └── device_monitoring/        # Device monitoring
│   │   │   │
│   │   │   ├── persistence/                  # 🔐 Persistence
│   │   │   │   ├── service_installer.py
│   │   │   │   ├── wmi_persistence.py
│   │   │   │   └── cron_persistence.py
│   │   │   │
│   │   │   ├── stealth/                      # 🥷 Stealth operations
│   │   │   │   ├── stealth_operations.py
│   │   │   │   ├── process_hider.py
│   │   │   │   └── av_evasion.py
│   │   │   │
│   │   │   ├── task_manager/                 # 📊 Task manager
│   │   │   │   ├── __init__.py
│   │   │   │   ├── process_monitor.py        # Process monitoring
│   │   │   │   ├── performance_analyzer.py
│   │   │   │   ├── service_manager.py
│   │   │   │   └── system_resources.py
│   │   │   │
│   │   │   └── data_processing/              # Data processing
│   │   │       ├── data_aggregator.py
│   │   │       ├── machine_learning.py
│   │   │       ├── alert_system.py
│   │   │       └── report_generator.py
│   │   │
│   │   └── utils/                            # Utilities
│   │       ├── __init__.py
│   │       ├── ai_analyzer.py
│   │       └── logger.py                     # Logging setup
│   │
│   └── tests/                                # Tests
│       ├── test_ai_model.py
│       ├── test_forensics.py
│       ├── test_network.py
│       └── test_autonomous.py
│
├── frontend/                                  # React Frontend
│   ├── public/
│   │   └── index.html                        # HTML template
│   │
│   ├── src/
│   │   ├── index.js                          # Entry point
│   │   ├── App.jsx                           # Main app component
│   │   │
│   │   ├── modules/                          # Feature modules
│   │   │   ├── Dashboard/                    # 📊 Dashboard
│   │   │   ├── TaskManager/                  # Task manager
│   │   │   ├── Forensics/                    # Forensics
│   │   │   ├── NetworkSecurity/              # Network security
│   │   │   ├── OTSecurity/                   # OT security
│   │   │   ├── Reports/                      # Reports
│   │   │   ├── Autonomous/                   # Autonomous
│   │   │   ├── AIAnalysis/                   # AI analysis
│   │   │   ├── Persistence/                  # Persistence
│   │   │   ├── Stealth/                      # Stealth
│   │   │   ├── C2/                           # C2 control
│   │   │   ├── AdminEscalation/              # Admin escalation
│   │   │   ├── ContinuousForensics/          # Continuous forensics
│   │   │   └── MalwareAnalysis/              # Malware analysis
│   │   │
│   │   ├── components/                       # React components
│   │   │   └── Common/
│   │   │       └── Sidebar.jsx               # Navigation sidebar
│   │   │
│   │   ├── pages/                            # Page components
│   │   │   ├── Dashboard.jsx                 # Dashboard page
│   │   │   ├── ForensicsPage.jsx             # Forensics page
│   │   │   ├── NetworkSecurityPage.jsx       # Network security page
│   │   │   ├── OTSecurityPage.jsx            # OT security page
│   │   │   ├── TaskManagerPage.jsx           # Task manager page
│   │   │   ├── AutonomousPage.jsx            # Autonomous page
│   │   │   ├── AIAnalysisPage.jsx            # AI analysis page
│   │   │   ├── C2Page.jsx                    # C2 page
│   │   │   ├── PersistencePage.jsx           # Persistence page
│   │   │   └── StealthPage.jsx               # Stealth page
│   │   │
│   │   ├── services/                         # API services
│   │   │   ├── api.js                        # REST API client
│   │   │   └── websocket.js                  # WebSocket client
│   │   │
│   │   ├── store/                            # Redux store
│   │   │   └── index.js
│   │   │
│   │   ├── utils/                            # Utilities
│   │   │
│   │   └── styles/                           # Styles
│   │
│   ├── package.json                          # NPM dependencies
│   ├── Dockerfile                            # Frontend container
│   └── nginx.conf                            # Nginx configuration
│
├── Auto_Launcher/                            # 🚀 Auto launcher
│   ├── admin_escalator.py                    # Privilege escalation
│   ├── linux_autorun.desktop                 # Linux autostart
│   ├── silent_installer.bat                  # Windows installer
│   ├── stealth_loader.sh                     # Stealth launcher
│   └── windows_autorun.inf                   # Windows autorun
│
├── Command_Control/                          # C2 infrastructure
│   ├── c2_server.py                          # C2 server
│   ├── implant_comms.py                      # Implant communications
│   └── task_distributor.py                   # Task distribution
│
├── Persistence_Engine/                       # Persistence mechanisms
│   ├── service_installer.py                  # Service installer
│   └── wmi_persistence.py                    # WMI persistence
│
├── Stealth_Engine/                           # Stealth operations
│   ├── av_evasion.py                         # AV evasion
│   └── process_hider.py                      # Process hiding
│
├── database/                                 # Database files (local)
├── docs/                                     # Documentation
├── scripts/                                  # Utility scripts
├── config/                                   # Configuration files
│
├── docker-compose.yml                        # Docker Compose config
├── .gitignore                                # Git ignore rules
├── README.md                                 # Main documentation
├── QUICKSTART.md                             # Quick start guide
└── STRUCTURE.md                              # This file

```

## 📊 Module Overview

### Backend Modules

| Module | Purpose | Key Features |
|--------|---------|--------------|
| **forensics** | Digital forensics | Disk imaging, file carving, registry analysis |
| **network_security** | Network security | IDS, packet analysis, vulnerability scanning |
| **ot_security** | OT/ICS security | Protocol analysis, device monitoring |
| **ai_model** | AI integration | Kaggle models, inference, training |
| **c2** | Command & control | Implant management, task distribution |
| **autonomous** | Autonomous ops | Auto-execution, continuous monitoring |
| **task_manager** | System monitoring | Process tracking, resource monitoring |
| **persistence** | Persistence | Service installation, WMI hooks |
| **stealth** | Stealth ops | Process hiding, AV evasion |

### Frontend Modules

| Module | Component | Description |
|--------|-----------|-------------|
| **Dashboard** | Main dashboard | System overview, metrics, alerts |
| **Forensics** | Forensic tools | Disk imaging, file carving, analysis |
| **NetworkSecurity** | Network tools | IDS alerts, packet capture |
| **OTSecurity** | OT monitoring | Device status, protocol analysis |
| **TaskManager** | Process manager | Process list, system stats |
| **AIAnalysis** | AI tools | Model management, predictions |
| **C2** | C2 control | Implant management, tasks |
| **Autonomous** | Auto operations | Task scheduling, execution logs |

## 🔧 Technology Stack

### Backend
- **Framework:** FastAPI
- **Database:** PostgreSQL + SQLAlchemy
- **Cache:** Redis
- **Search:** Elasticsearch
- **AI/ML:** scikit-learn, pandas, numpy
- **Security:** python-jose, passlib
- **Async:** asyncio, aiohttp

### Frontend
- **Framework:** React 18
- **UI Library:** Material-UI (MUI)
- **State Management:** Redux Toolkit
- **Routing:** React Router
- **Charts:** Recharts
- **Real-time:** Socket.io

### Infrastructure
- **Containerization:** Docker
- **Orchestration:** Docker Compose
- **Web Server:** Nginx (frontend)
- **ASGI Server:** Uvicorn (backend)

## 📈 Data Flow

```
User → Frontend (React)
       ↓ REST API
       Backend (FastAPI)
       ↓
       ├→ PostgreSQL (Structured data)
       ├→ Redis (Cache, sessions)
       └→ Elasticsearch (Logs, search)
```

## 🔐 Security Architecture

```
┌─────────────────────────────────────┐
│         Security Layers             │
├─────────────────────────────────────┤
│ 1. Authentication (JWT)             │
│ 2. Authorization (Role-based)       │
│ 3. Input Validation                 │
│ 4. Rate Limiting                    │
│ 5. SQL Injection Prevention         │
│ 6. XSS Protection                   │
│ 7. CORS Configuration               │
│ 8. Encrypted Communications         │
└─────────────────────────────────────┘
```

---

**This structure represents the complete Ultimate OT-AFP Platform as implemented.**
