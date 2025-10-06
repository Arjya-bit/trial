#!/bin/bash

# Ultimate OT-AFP Platform Setup Verification Script

echo "🔍 Verifying Ultimate OT-AFP Platform Setup..."
echo "================================================"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
passed=0
failed=0

# Check function
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
        ((passed++))
        return 0
    else
        echo -e "${RED}✗${NC} $1"
        ((failed++))
        return 1
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1/"
        ((passed++))
        return 0
    else
        echo -e "${RED}✗${NC} $1/"
        ((failed++))
        return 1
    fi
}

echo "📁 Checking Project Structure..."
echo "--------------------------------"

# Backend Core
check_file "backend/main.py"
check_file "backend/requirements.txt"
check_file "backend/Dockerfile"
check_file "backend/.env.example"

# Backend Source
check_dir "backend/src/core"
check_dir "backend/src/api"
check_dir "backend/src/modules"
check_dir "backend/src/database"

# Key Backend Files
check_file "backend/src/core/app.py"
check_file "backend/src/core/config.py"
check_file "backend/src/core/database.py"
check_file "backend/src/core/security.py"

# API Endpoints
check_file "backend/src/api/v1/routers.py"
check_file "backend/src/api/v1/endpoints/forensics.py"
check_file "backend/src/api/v1/endpoints/ai_analysis.py"
check_file "backend/src/api/v1/endpoints/c2.py"
check_file "backend/src/api/v1/endpoints/task_manager.py"

# Modules
check_dir "backend/src/modules/ai_model"
check_dir "backend/src/modules/forensics"
check_dir "backend/src/modules/network_security"
check_dir "backend/src/modules/c2"
check_dir "backend/src/modules/autonomous"

# AI Model Files
check_file "backend/src/modules/ai_model/model_downloader.py"
check_file "backend/src/modules/ai_model/model_inference.py"
check_file "backend/src/modules/ai_model/config.json"

# Frontend
echo ""
echo "🎨 Checking Frontend..."
echo "----------------------"
check_file "frontend/package.json"
check_file "frontend/Dockerfile"
check_file "frontend/src/index.js"
check_file "frontend/src/App.jsx"

# Frontend Pages
check_file "frontend/src/pages/Dashboard.jsx"
check_file "frontend/src/pages/ForensicsPage.jsx"
check_file "frontend/src/pages/NetworkSecurityPage.jsx"
check_file "frontend/src/pages/AIAnalysisPage.jsx"
check_file "frontend/src/pages/C2Page.jsx"

# Frontend Services
check_file "frontend/src/services/api.js"
check_file "frontend/src/services/websocket.js"

# Components
check_file "frontend/src/components/Common/Sidebar.jsx"

# Additional Directories
echo ""
echo "🚀 Checking Additional Components..."
echo "------------------------------------"
check_dir "Auto_Launcher"
check_dir "Command_Control"
check_dir "Persistence_Engine"
check_dir "Stealth_Engine"

# Key Scripts
check_file "Auto_Launcher/admin_escalator.py"
check_file "Auto_Launcher/silent_installer.bat"
check_file "Auto_Launcher/stealth_loader.sh"
check_file "Command_Control/implant_comms.py"
check_file "Persistence_Engine/service_installer.py"
check_file "Stealth_Engine/process_hider.py"

# Documentation
echo ""
echo "📚 Checking Documentation..."
echo "---------------------------"
check_file "README.md"
check_file "QUICKSTART.md"
check_file "STRUCTURE.md"
check_file "PROJECT_SUMMARY.md"

# Configuration
echo ""
echo "⚙️  Checking Configuration..."
echo "----------------------------"
check_file "docker-compose.yml"
check_file ".gitignore"

echo ""
echo "================================================"
echo "📊 Verification Summary"
echo "================================================"
echo -e "Passed: ${GREEN}$passed${NC}"
echo -e "Failed: ${RED}$failed${NC}"
echo ""

if [ $failed -eq 0 ]; then
    echo -e "${GREEN}✅ All checks passed! Platform is ready.${NC}"
    echo ""
    echo "🚀 Quick Start:"
    echo "   docker-compose up -d"
    echo ""
    echo "📖 Access:"
    echo "   Frontend: http://localhost:3000"
    echo "   Backend:  http://localhost:8000"
    echo "   API Docs: http://localhost:8000/api/docs"
    exit 0
else
    echo -e "${RED}❌ Some checks failed. Please review the missing files.${NC}"
    exit 1
fi
