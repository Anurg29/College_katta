#!/bin/bash

# College Katta - Stop Script
# This script will stop all running services

echo "🛑 Stopping College Katta services..."
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Stop backend
if [ -f "backend.pid" ]; then
    BACKEND_PID=$(cat backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        kill $BACKEND_PID
        print_success "Backend stopped (PID: $BACKEND_PID)"
    else
        print_error "Backend process not found"
    fi
    rm backend.pid
else
    # Try to find and kill by port
    BACKEND_PID=$(lsof -ti :8000)
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID
        print_success "Backend stopped (PID: $BACKEND_PID)"
    fi
fi

# Stop frontend
if [ -f "frontend.pid" ]; then
    FRONTEND_PID=$(cat frontend.pid)
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        kill $FRONTEND_PID
        print_success "Frontend stopped (PID: $FRONTEND_PID)"
    else
        print_error "Frontend process not found"
    fi
    rm frontend.pid
else
    # Try to find and kill by port
    FRONTEND_PID=$(lsof -ti :5173)
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID
        print_success "Frontend stopped (PID: $FRONTEND_PID)"
    fi
fi

# Ask about Docker services
if command -v docker &> /dev/null; then
    echo ""
    read -p "Do you want to stop Docker services? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker-compose down
        print_success "Docker services stopped"
    fi
fi

echo ""
print_success "All services stopped!"
