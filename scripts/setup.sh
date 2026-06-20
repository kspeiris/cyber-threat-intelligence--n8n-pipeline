#!/bin/bash

echo "🚀 Cyber Threat Intelligence Pipeline Setup"
echo "==========================================="

# Check Docker installation
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Create necessary directories
echo "📁 Creating directories..."

# Create .env file if it doesn't exist
if [ ! -f backend/.env ]; then
    echo "🔑 Creating .env file..."
    cp backend/.env.example backend/.env
    echo "⚠️ Please update backend/.env with your API keys"
fi

# Build and start Docker containers
echo "🏗️ Building Docker containers..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "📊 Access your services:"
echo "   - FastAPI Backend: http://localhost:8000"
echo "   - FastAPI Docs: http://localhost:8000/docs"
echo "   - Streamlit Dashboard: http://localhost:8501"
echo "   - n8n Workflow: http://localhost:5678"
echo ""
echo "📝 Default credentials:"
echo "   - PostgreSQL: user/password"
echo "   - n8n: No authentication by default"
echo ""
echo "⚠️ Important:"
echo "   1. Update backend/.env with your API keys"
echo "   2. Configure n8n workflow with your Telegram credentials"
echo "   3. Access n8n and import the workflow from n8n-workflows/"
echo ""
echo "To stop services: docker-compose down"
echo "To view logs: docker-compose logs -f"