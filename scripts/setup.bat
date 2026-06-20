@echo off
echo 🚀 Cyber Threat Intelligence Pipeline Setup
echo ===========================================

REM Check Docker installation
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker first.
    exit /b 1
)

docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    exit /b 1
)

echo ✅ Docker and Docker Compose are installed

REM Create .env file if it doesn't exist
if not exist "backend\.env" (
    echo 🔑 Creating .env file...
    copy backend\.env.example backend\.env
    echo ⚠️ Please update backend\.env with your API keys
)

REM Build and start Docker containers
echo 🏗️ Building Docker containers...
docker-compose build

echo 🚀 Starting services...
docker-compose up -d

echo.
echo ✅ Setup completed successfully!
echo.
echo 📊 Access your services:
echo    - FastAPI Backend: http://localhost:8000
echo    - FastAPI Docs: http://localhost:8000/docs
echo    - Streamlit Dashboard: http://localhost:8501
echo    - n8n Workflow: http://localhost:5678
echo.
echo 📝 Default credentials:
echo    - PostgreSQL: user/password
echo.
echo ⚠️ Important:
echo    1. Update backend\.env with your API keys
echo    2. Configure n8n workflow with your Telegram credentials
echo.
echo To stop services: docker-compose down
echo To view logs: docker-compose logs -f