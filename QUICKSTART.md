# 🚀 College Katta - Quick Start Guide

## ✅ Project Successfully Running & Deployed!

### 🌐 GitHub Repository
**URL**: [https://github.com/Anurg29/College_katta](https://github.com/Anurg29/College_katta)

---

## 🎉 Current Status

### ✅ Backend Server
- **Status**: Running Successfully
- **URL**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database**: SQLite (auto-created at `backend/techkatta.db`)
- **All Tables Created**: ✅

### ✅ Frontend Application
- **Status**: Running Successfully  
- **URL**: http://localhost:5173
- **Framework**: React + TypeScript + Vite

### ✅ GitHub Deployment
- **Repository**: Anurg29/College_katta
- **Branch**: main
- **Latest Commit**: "feat: Add SQLite support for easier local development"
- **Status**: All changes pushed successfully

---

## 🏃 Running the Project

### Backend (Already Running)
```bash
cd backend
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (Already Running)
```bash
cd frontend
npm run dev
```

---

## 🔧 What Was Fixed

### 1. Database Configuration
- ✅ Added SQLite support for easy local development
- ✅ Made DATABASE_URL optional (defaults to SQLite)
- ✅ Made MONGODB_URL optional (defaults to localhost)
- ✅ Auto-fallback to SQLite if MySQL not configured
- ✅ No complex database setup required!

### 2. Configuration Updates
**File**: `backend/app/core/config.py`
- DATABASE_URL now defaults to `sqlite:///./techkatta.db`
- MONGODB_URL now defaults to `mongodb://localhost:27017`

**File**: `backend/app/core/database.py`
- Added multi-database support (MySQL, SQLite, others)
- Automatic fallback mechanism
- SQLite-specific configuration for local dev

### 3. Project Cleanup
- ✅ Removed unnecessary folders (venv, node_modules, __pycache__, dist)
- ✅ Cleaned up all Python cache files
- ✅ Optimized .gitignore

---

## 📦 Features Available

### Core Features
- ✅ User Authentication (JWT)
- ✅ User Profiles & Management
- ✅ Resource Sharing Hub
- ✅ Job & Internship Board
- ✅ Project Showcase
- ✅ Event Calendar
- ✅ Mentorship Program
- ✅ ML Recommendation System

### API Endpoints
All endpoints are documented at: http://localhost:8000/docs

**Authentication**
- POST `/api/v1/auth/register` - Register new user
- POST `/api/v1/auth/login` - Login user
- POST `/api/v1/auth/refresh` - Refresh token

**Resources**
- GET `/api/v1/resources` - List resources
- POST `/api/v1/resources` - Upload resource
- POST `/api/v1/resources/{id}/vote` - Vote on resource

**Jobs**
- GET `/api/v1/jobs` - List job postings
- POST `/api/v1/jobs` - Create job posting
- POST `/api/v1/jobs/{id}/apply` - Apply to job

**Projects**
- GET `/api/v1/projects` - List projects
- POST `/api/v1/projects` - Create project
- POST `/api/v1/projects/{id}/like` - Like project

**Events**
- GET `/api/v1/events` - List events
- POST `/api/v1/events` - Create event
- POST `/api/v1/events/{id}/rsvp` - RSVP to event

**Mentorship**
- GET `/api/v1/mentorship/mentors` - List mentors
- POST `/api/v1/mentorship/become-mentor` - Register as mentor
- POST `/api/v1/mentorship/request` - Request mentorship
- POST `/api/v1/mentorship/sessions` - Schedule session

---

## 🌐 Access Your Application

### Local Development
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

### Test the API
```bash
# Health check
curl http://localhost:8000/health

# Root endpoint
curl http://localhost:8000/

# API documentation
open http://localhost:8000/docs
```

---

## 📁 Project Structure

```
College_katta/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/    # All API routes
│   │   ├── core/                # Config & database
│   │   ├── models/              # Database models
│   │   ├── schemas/             # Pydantic schemas
│   │   └── main.py              # FastAPI app
│   ├── techkatta.db             # SQLite database (auto-created)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.tsx
│   └── package.json
├── DEPLOYMENT.md                # Deployment guide
└── README.md                    # Main documentation
```

---

## 🔄 Git Commands Reference

### Clone the Repository
```bash
git clone https://github.com/Anurg29/College_katta.git
cd College_katta
```

### Pull Latest Changes
```bash
git pull origin main
```

### Make Changes and Push
```bash
git add .
git commit -m "Your commit message"
git push origin main
```

---

## 🐳 Optional: Docker Deployment

If you want to use Docker instead:

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## 🎯 Next Steps

### For Development
1. ✅ Backend is running on port 8000
2. ✅ Frontend is running on port 5173
3. ✅ SQLite database is auto-created
4. ✅ All changes are pushed to GitHub

### To Add Features
1. Create a new branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Test locally
4. Commit and push: `git push origin feature/your-feature`
5. Create a Pull Request on GitHub

### To Deploy to Production
See `DEPLOYMENT.md` for:
- Railway deployment (Backend)
- Firebase Hosting (Frontend)
- Vercel/Netlify alternatives

---

## 🐛 Troubleshooting

### Backend won't start?
```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill the process if needed
kill -9 <PID>

# Restart backend
cd backend
python3 -m uvicorn app.main:app --reload
```

### Frontend won't start?
```bash
# Reinstall dependencies
cd frontend
rm -rf node_modules
npm install
npm run dev
```

### Database issues?
The project now uses SQLite by default - no setup needed!
The database file is automatically created at `backend/techkatta.db`

---

## 📞 Support

- **GitHub Issues**: [https://github.com/Anurg29/College_katta/issues](https://github.com/Anurg29/College_katta/issues)
- **Repository**: [https://github.com/Anurg29/College_katta](https://github.com/Anurg29/College_katta)

---

**🎉 Congratulations! Your project is running and deployed to GitHub!**

**Last Updated**: November 30, 2025, 6:07 PM IST
