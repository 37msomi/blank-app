#!/bin/bash
# LMS Setup Script - Automates frontend and backend installation

set -e

echo "🚀 Leave Management System - Setup Script"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

echo -e "${BLUE}✓ Node.js version:${NC} $(node --version)"
echo -e "${BLUE}✓ npm version:${NC} $(npm --version)"
echo ""

# Navigate to project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

# Backend Setup
echo -e "${BLUE}📦 Setting up Backend...${NC}"
cd backend

if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
fi

echo "Installing backend dependencies..."
npm install

echo -e "${GREEN}✓ Backend setup complete!${NC}"
echo ""

# Frontend Setup
echo -e "${BLUE}📦 Setting up Frontend...${NC}"
cd ../frontend

if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
fi

echo "Installing frontend dependencies..."
npm install

echo -e "${GREEN}✓ Frontend setup complete!${NC}"
echo ""

# Summary
echo -e "${GREEN}=========================================="
echo "✅ Setup Complete!"
echo "==========================================${NC}"
echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Start PostgreSQL (Docker):"
echo -e "${BLUE}   docker-compose up -d${NC}"
echo ""
echo "2. Start Backend (from backend/ directory):"
echo -e "${BLUE}   npm run dev${NC}"
echo ""
echo "3. Start Frontend (from frontend/ directory):"
echo -e "${BLUE}   npm start${NC}"
echo ""
echo "4. Open browser and navigate to:"
echo -e "${BLUE}   http://localhost:3000${NC}"
echo ""
echo "Demo Credentials:"
echo "  Employee: emp@test.com"
echo "  Manager:  mgr@test.com"
echo "  Admin:    admin@test.com"
echo "  Password: password (all accounts)"
echo ""
