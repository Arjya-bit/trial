# Quick Start Guide

Get the Ultimate OT-AFP Platform up and running in minutes!

## 🚀 Quick Start with Docker

The fastest way to get started:

```bash
# 1. Clone or navigate to the project
cd ultimate-ot-afp

# 2. Start all services with Docker Compose
docker-compose up -d

# 3. Wait for services to be healthy (about 30 seconds)
docker-compose ps

# 4. Access the platform
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
```

That's it! The platform is now running.

## 💻 Manual Installation

### Backend Setup (5 minutes)

```bash
# 1. Navigate to backend directory
cd backend

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure environment
cp .env.example .env
# Edit .env with your database credentials

# 6. Start the backend
python main.py
```

Backend will be available at: http://localhost:8000

### Frontend Setup (3 minutes)

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Configure environment
echo "REACT_APP_API_URL=http://localhost:8000/api/v1" > .env
echo "REACT_APP_WS_URL=ws://localhost:8000" >> .env

# 4. Start the frontend
npm start
```

Frontend will be available at: http://localhost:3000

## 🗄️ Database Setup

### Using Docker (Recommended)

Databases are automatically configured when using docker-compose.

### Manual Setup

**PostgreSQL:**
```bash
# Install PostgreSQL
sudo apt-get install postgresql  # Ubuntu/Debian
brew install postgresql  # Mac

# Create database
createdb otafp_db
```

**Redis:**
```bash
# Install Redis
sudo apt-get install redis-server  # Ubuntu/Debian
brew install redis  # Mac

# Start Redis
redis-server
```

**Elasticsearch:**
```bash
# Docker method (easiest)
docker run -d -p 9200:9200 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:8.11.0
```

## 🧠 AI Model Setup

### Download Cybersecurity Models from Kaggle

1. **Get Kaggle API credentials:**
   - Go to https://www.kaggle.com
   - Account → API → Create New API Token
   - Download `kaggle.json`

2. **Configure credentials:**
   ```bash
   # Linux/Mac
   mkdir -p ~/.kaggle
   mv kaggle.json ~/.kaggle/
   chmod 600 ~/.kaggle/kaggle.json
   
   # Or add to .env
   KAGGLE_USERNAME=your_username
   KAGGLE_KEY=your_api_key
   ```

3. **Download models via API:**
   ```bash
   # Using curl
   curl -X POST http://localhost:8000/api/v1/ai/models/download \
     -H "Content-Type: application/json" \
     -d '{"model_key": "intrusion_detection"}'
   ```

## 🎯 First Steps

### 1. Access the Dashboard
Open http://localhost:3000 and explore the main dashboard.

### 2. Try Forensics Tools
- Navigate to Forensics section
- Create a disk image
- Try file carving

### 3. Monitor Processes
- Go to Task Manager
- View running processes
- Monitor system resources

### 4. Network Security
- Check Network Security section
- View IDS alerts
- Analyze network traffic

### 5. AI Analysis
- Go to AI Analysis page
- Download a cybersecurity model
- Run predictions on sample data

## 📖 Key Endpoints

### Backend API
- **API Documentation:** http://localhost:8000/api/docs
- **Health Check:** http://localhost:8000/health
- **Forensics:** http://localhost:8000/api/v1/forensics
- **Network Security:** http://localhost:8000/api/v1/network
- **AI Analysis:** http://localhost:8000/api/v1/ai
- **C2 Control:** http://localhost:8000/api/v1/c2
- **Task Manager:** http://localhost:8000/api/v1/task-manager

### WebSocket
- **Real-time Updates:** ws://localhost:8000/ws
- **Alerts:** ws://localhost:8000/ws/alerts
- **Metrics:** ws://localhost:8000/ws/metrics

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Frontend build fails
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Check Node version
node --version  # Should be 18+
```

### Database connection errors
```bash
# Check if databases are running
docker-compose ps  # If using Docker

# Test PostgreSQL connection
psql -U otafp_user -d otafp_db -h localhost

# Test Redis connection
redis-cli ping
```

### Can't download AI models
```bash
# Verify Kaggle credentials
cat ~/.kaggle/kaggle.json

# Test Kaggle API
kaggle datasets list

# Check API permissions
# Make sure your Kaggle account has accepted competition rules
```

## 🔐 Security Considerations

⚠️ **Important:** Default configuration is for development only!

For production:
1. Change all default passwords
2. Use strong SECRET_KEY in .env
3. Enable HTTPS/TLS
4. Configure firewall rules
5. Use environment-specific credentials
6. Enable authentication and authorization
7. Regular security audits

## 📚 Next Steps

1. **Read the full README.md** for comprehensive documentation
2. **Explore API docs** at /api/docs
3. **Configure Kaggle API** for AI models
4. **Set up persistent storage** for forensics data
5. **Configure alerting** for security events
6. **Customize dashboards** for your needs

## 🆘 Getting Help

- Check logs: `docker-compose logs -f`
- Review API docs: http://localhost:8000/api/docs
- Check GitHub issues
- Read full documentation in `/docs`

## ✅ Verification Checklist

- [ ] Backend running on port 8000
- [ ] Frontend accessible at port 3000
- [ ] PostgreSQL connected
- [ ] Redis connected
- [ ] Elasticsearch connected
- [ ] API docs accessible
- [ ] WebSocket connection working
- [ ] Can view Dashboard
- [ ] Can access all modules

---

**You're all set! Happy hacking! 🎉**
