# 🚀 College Katta - Deployment Guide

## GitHub Repository
**Repository URL**: [https://github.com/Anurg29/College_katta](https://github.com/Anurg29/College_katta)

---

## ✅ Project Status

### Successfully Deployed to GitHub
- ✅ Repository: `Anurg29/College_katta`
- ✅ Branch: `main`
- ✅ All source code committed and pushed
- ✅ `.gitignore` properly configured
- ✅ Unnecessary files excluded (node_modules, venv, __pycache__, dist)

---

## 📦 What's Included

### Backend (`/backend`)
- FastAPI application with Python 3.11+
- MySQL + MongoDB database models
- JWT authentication system
- RESTful API endpoints for:
  - Authentication & User Management
  - Resource Sharing Hub
  - Job & Internship Board
  - Project Showcase
  - Event Calendar
  - Mentorship Program
- ML recommendation system
- Docker configuration

### Frontend (`/frontend`)
- React 18 + TypeScript application
- Vite build tool
- TailwindCSS styling
- Responsive UI components
- Firebase deployment configuration

### Configuration Files
- `.env.example` - Environment variable template
- `docker-compose.yml` - Docker orchestration
- `requirements.txt` - Python dependencies
- `package.json` - Node.js dependencies
- `.gitignore` - Git ignore rules

---

## 🔧 Setup Instructions for New Users

### 1. Clone the Repository
```bash
git clone https://github.com/Anurg29/College_katta.git
cd College_katta
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp ../.env.example .env
# Edit .env with your database credentials

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

### 4. Access the Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 🗄️ Database Setup

### MySQL Setup
```sql
-- Create database
CREATE DATABASE techkatta;

-- Create user
CREATE USER 'techkatta_user'@'localhost' IDENTIFIED BY 'your_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON techkatta.* TO 'techkatta_user'@'localhost';
FLUSH PRIVILEGES;
```

### MongoDB Setup
```bash
# Start MongoDB
mongod --dbpath /path/to/data

# Or use MongoDB Atlas (cloud)
# Update MONGODB_URL in .env with your connection string
```

### Redis Setup
```bash
# Install Redis
brew install redis  # macOS
# or
sudo apt-get install redis  # Linux

# Start Redis
redis-server
```

---

## 🐳 Docker Deployment (Recommended)

### Quick Start with Docker
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

This will start:
- Backend API (port 8000)
- Frontend (port 5173)
- MySQL database
- MongoDB database
- Redis cache

---

## ☁️ Cloud Deployment

### Backend Deployment Options

#### Option 1: Railway
1. Go to [Railway.app](https://railway.app)
2. Connect your GitHub repository
3. Select `backend` directory
4. Add environment variables from `.env.example`
5. Deploy!

#### Option 2: Render
1. Go to [Render.com](https://render.com)
2. Create new Web Service
3. Connect GitHub repository
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Frontend Deployment Options

#### Option 1: Firebase Hosting (Already Configured)
```bash
cd frontend

# Build production bundle
npm run build

# Deploy to Firebase
firebase deploy
```

#### Option 2: Vercel
1. Go to [Vercel.com](https://vercel.com)
2. Import GitHub repository
3. Select `frontend` directory
4. Deploy automatically!

#### Option 3: Netlify
1. Go to [Netlify.com](https://netlify.com)
2. Connect GitHub repository
3. Build command: `npm run build`
4. Publish directory: `dist`

---

## 🔐 Environment Variables

### Required Variables
```env
# Database
DATABASE_URL=mysql+pymysql://user:password@host:port/database
MONGODB_URL=mongodb://user:password@host:port
REDIS_URL=redis://host:port

# Security
SECRET_KEY=your-secret-key-min-32-characters
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=["http://localhost:5173","https://yourdomain.com"]
```

---

## 📊 Current Features

### ✅ Implemented
- User Authentication (JWT)
- User Profiles & Management
- Resource Sharing Hub
- Job & Internship Board
- Project Showcase
- Event Calendar
- Mentorship Program
- ML Recommendation System

### 🚧 In Progress
- Real-time Chat
- Discussion Forums
- Gamification System
- Advanced Search

---

## 🐛 Known Issues

### Database Connection Error
**Error**: `Access denied for user 'techkatta_user'@'localhost'`

**Solution**: 
1. Create MySQL user and database (see Database Setup above)
2. Update `.env` file with correct credentials
3. Ensure MySQL server is running

---

## 📝 Git Workflow

### Making Changes
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "Description of changes"

# Push to GitHub
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

### Syncing with Main Branch
```bash
# Switch to main branch
git checkout main

# Pull latest changes
git pull origin main

# Switch back to feature branch
git checkout feature/your-feature-name

# Merge main into feature branch
git merge main
```

---

## 📞 Support & Contact

- **Repository**: [https://github.com/Anurg29/College_katta](https://github.com/Anurg29/College_katta)
- **Issues**: [https://github.com/Anurg29/College_katta/issues](https://github.com/Anurg29/College_katta/issues)
- **Owner**: @Anurg29

---

## 📄 License

This project is licensed under the MIT License.

---

**Last Updated**: November 30, 2025
**Version**: 1.0.0
**Status**: ✅ Active Development
