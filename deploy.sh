#!/bin/bash

# College Katta - Production Deployment Helper Script
# This script helps you set up and deploy the College Katta project to production

set -e  # Exit on error

echo "🚀 College Katta - Production Deployment Helper"
echo "================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "Step 1: Checking Prerequisites"
echo "================================"

# Check Node.js
if command_exists node; then
    NODE_VERSION=$(node --version)
    print_success "Node.js installed: $NODE_VERSION"
else
    print_error "Node.js not found. Please install Node.js 18+"
    exit 1
fi

# Check npm
if command_exists npm; then
    NPM_VERSION=$(npm --version)
    print_success "npm installed: $NPM_VERSION"
else
    print_error "npm not found"
    exit 1
fi

# Check Python
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python installed: $PYTHON_VERSION"
else
    print_error "Python3 not found. Please install Python 3.11+"
    exit 1
fi

# Check Firebase CLI
if command_exists firebase; then
    print_success "Firebase CLI installed"
else
    print_warning "Firebase CLI not found"
    read -p "Install Firebase CLI? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        npm install -g firebase-tools
        print_success "Firebase CLI installed"
    fi
fi

echo ""
echo "Step 2: Environment Configuration"
echo "=================================="

# Check if .env files exist
if [ -f "backend/.env" ]; then
    print_success "Backend .env file exists"
else
    print_warning "Backend .env file not found"
    print_info "Creating from .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example backend/.env
        print_success "Created backend/.env from .env.example"
        print_warning "Please update backend/.env with your actual values"
    fi
fi

echo ""
echo "Step 3: Build Frontend"
echo "======================"

cd frontend

print_info "Installing frontend dependencies..."
npm install

print_info "Building frontend..."
npm run build

if [ -d "dist" ]; then
    print_success "Frontend built successfully"
else
    print_error "Frontend build failed"
    exit 1
fi

cd ..

echo ""
echo "Step 4: Firebase Setup"
echo "======================"

read -p "Do you want to deploy to Firebase? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    cd frontend
    
    print_info "Logging into Firebase..."
    firebase login
    
    print_info "Listing Firebase projects..."
    firebase projects:list
    
    echo ""
    read -p "Enter your Firebase Project ID: " PROJECT_ID
    
    if [ ! -f ".firebaserc" ]; then
        print_info "Creating .firebaserc..."
        cat > .firebaserc <<EOF
{
  "projects": {
    "default": "$PROJECT_ID"
  }
}
EOF
        print_success "Created .firebaserc"
    fi
    
    print_info "Deploying to Firebase..."
    firebase deploy --only hosting
    
    print_success "Firebase deployment complete!"
    print_info "Your app is live at: https://$PROJECT_ID.web.app"
    
    cd ..
fi

echo ""
echo "Step 5: Backend Deployment Info"
echo "================================"

print_info "To deploy backend to Railway:"
echo "1. Go to https://railway.app"
echo "2. Sign up/Login with GitHub"
echo "3. Create new project"
echo "4. Deploy from GitHub repo: Anurg29/College_katta"
echo "5. Select 'backend' directory"
echo "6. Add environment variables (see PRODUCTION_DEPLOYMENT.md)"
echo ""

print_info "Required Environment Variables:"
echo "- DATABASE_URL (from Railway MySQL)"
echo "- MONGODB_URL (from MongoDB Atlas)"
echo "- REDIS_URL (from Railway Redis)"
echo "- SECRET_KEY (generate with: python3 -c 'import secrets; print(secrets.token_urlsafe(32))')"
echo "- CORS_ORIGINS (add your Firebase URL)"
echo ""

echo "Step 6: Database Setup Info"
echo "============================"

print_info "MongoDB Atlas Setup:"
echo "1. Go to https://www.mongodb.com/cloud/atlas/register"
echo "2. Create free M0 cluster"
echo "3. Create database user"
echo "4. Whitelist IP: 0.0.0.0/0"
echo "5. Get connection string"
echo ""

print_info "Railway MySQL Setup:"
echo "1. In Railway dashboard, click 'New' → 'Database' → 'MySQL'"
echo "2. Copy connection details from Variables tab"
echo "3. Construct DATABASE_URL"
echo ""

echo "Step 7: Generate SECRET_KEY"
echo "==========================="

print_info "Generating SECRET_KEY..."
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
print_success "Generated SECRET_KEY:"
echo "$SECRET_KEY"
print_warning "Save this key securely and add it to Railway environment variables!"
echo ""

echo "Step 8: Summary"
echo "==============="

print_success "Local setup complete!"
echo ""
print_info "Next steps:"
echo "1. ✅ Frontend built and ready"
echo "2. ⚠️  Deploy frontend to Firebase (if not done above)"
echo "3. ⚠️  Set up MongoDB Atlas database"
echo "4. ⚠️  Set up Railway MySQL database"
echo "5. ⚠️  Deploy backend to Railway"
echo "6. ⚠️  Update CORS_ORIGINS in Railway"
echo "7. ⚠️  Test end-to-end"
echo ""

print_info "For detailed instructions, see:"
echo "- PRODUCTION_DEPLOYMENT.md"
echo "- DEPLOYMENT_ERRORS.md"
echo "- QUICKSTART.md"
echo ""

print_success "Deployment helper complete! 🎉"
