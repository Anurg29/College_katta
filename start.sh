#!/bin/bash

# College Katta - Automated Setup Script
# This script will set up and run the College Katta platform

set -e  # Exit on error

echo "🚀 College Katta - Automated Setup"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "ℹ️  $1"
}

# Check if Docker is installed
check_docker() {
    if command -v docker &> /dev/null; then
        print_success "Docker is installed"
        return 0
    else
        print_warning "Docker is not installed"
        return 1
    fi
}

# Check if MySQL is running
check_mysql() {
    if lsof -i :3306 &> /dev/null; then
        print_success "MySQL is running on port 3306"
        return 0
    else
        print_warning "MySQL is not running on port 3306"
        return 1
    fi
}

# Check if MongoDB is running
check_mongodb() {
    if lsof -i :27017 &> /dev/null; then
        print_success "MongoDB is running on port 27017"
        return 0
    else
        print_warning "MongoDB is not running on port 27017"
        return 1
    fi
}

# Check if Redis is running
check_redis() {
    if lsof -i :6379 &> /dev/null; then
        print_success "Redis is running on port 6379"
        return 0
    else
        print_warning "Redis is not running on port 6379"
        return 1
    fi
}

# Start services with Docker
start_docker_services() {
    print_info "Starting services with Docker..."
    docker-compose up -d
    sleep 5  # Wait for services to start
    print_success "Docker services started"
}

# Start MySQL locally
start_mysql_local() {
    print_info "Starting MySQL locally..."
    if command -v brew &> /dev/null; then
        brew services start mysql || mysql.server start
    else
        mysql.server start
    fi
    sleep 3
}

# Setup backend
setup_backend() {
    print_info "Setting up backend..."
    
    cd backend
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        print_info "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    print_info "Installing Python dependencies..."
    pip install -r requirements.txt --quiet
    
    print_success "Backend setup complete"
    cd ..
}

# Setup frontend
setup_frontend() {
    print_info "Setting up frontend..."
    
    cd frontend
    
    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        print_info "Installing Node dependencies..."
        npm install
    else
        print_success "Node dependencies already installed"
    fi
    
    print_success "Frontend setup complete"
    cd ..
}

# Start backend
start_backend() {
    print_info "Starting backend server..."
    
    cd backend
    source venv/bin/activate
    
    # Start backend in background
    nohup uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > ../backend.log 2>&1 &
    BACKEND_PID=$!
    
    echo $BACKEND_PID > ../backend.pid
    
    print_success "Backend started (PID: $BACKEND_PID)"
    print_info "Backend logs: backend.log"
    
    cd ..
}

# Start frontend
start_frontend() {
    print_info "Starting frontend server..."
    
    cd frontend
    
    # Start frontend in background
    nohup npm run dev > ../frontend.log 2>&1 &
    FRONTEND_PID=$!
    
    echo $FRONTEND_PID > ../frontend.pid
    
    print_success "Frontend started (PID: $FRONTEND_PID)"
    print_info "Frontend logs: frontend.log"
    
    cd ..
}

# Check if services are running
check_services() {
    echo ""
    print_info "Checking services status..."
    echo ""
    
    # Check backend
    if lsof -i :8000 &> /dev/null; then
        print_success "Backend is running on http://localhost:8000"
        print_info "API Docs: http://localhost:8000/docs"
    else
        print_error "Backend is not running"
    fi
    
    # Check frontend
    if lsof -i :5173 &> /dev/null; then
        print_success "Frontend is running on http://localhost:5173"
    else
        print_error "Frontend is not running"
    fi
    
    # Check databases
    check_mysql
    check_mongodb
    check_redis
}

# Main setup flow
main() {
    echo ""
    print_info "Starting automated setup..."
    echo ""
    
    # Check if Docker is available
    if check_docker; then
        print_info "Using Docker for database services"
        start_docker_services
    else
        print_warning "Docker not available, checking local services..."
        
        # Check and start local services
        if ! check_mysql; then
            start_mysql_local
        fi
        
        if ! check_mongodb; then
            print_warning "MongoDB not running. Please start it manually or install Docker."
        fi
        
        if ! check_redis; then
            print_warning "Redis not running. Please start it manually or install Docker."
        fi
    fi
    
    echo ""
    
    # Setup backend
    setup_backend
    
    echo ""
    
    # Setup frontend
    setup_frontend
    
    echo ""
    
    # Start backend
    start_backend
    
    # Wait for backend to start
    sleep 5
    
    # Start frontend
    start_frontend
    
    # Wait for frontend to start
    sleep 5
    
    # Check all services
    check_services
    
    echo ""
    echo "=================================="
    print_success "Setup Complete! 🎉"
    echo "=================================="
    echo ""
    print_info "Access your application:"
    echo "  Frontend: http://localhost:5173"
    echo "  Backend API: http://localhost:8000"
    echo "  API Docs: http://localhost:8000/docs"
    echo ""
    print_info "To stop the services, run:"
    echo "  ./stop.sh"
    echo ""
    print_info "To view logs:"
    echo "  tail -f backend.log"
    echo "  tail -f frontend.log"
    echo ""
}

# Run main function
main
