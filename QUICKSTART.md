# TechKatta - Quick Start Guide

## 🎯 Getting Started in 5 Minutes

This guide will help you get TechKatta running on your local machine quickly.

## Prerequisites Check

Before starting, ensure you have:
- ✅ Docker Desktop installed and running
- ✅ Git installed
- ✅ A code editor (VS Code recommended)

## Step 1: Clone and Setup

```bash
# Navigate to the project directory
cd /Users/anuragdineshrokade/Documents/College_katta

# Create environment file
cp .env.example .env
```

## Step 2: Start with Docker (Easiest Method)

```bash
# Start all services (MySQL, MongoDB, Redis, Backend)
docker-compose up -d

# Check if services are running
docker-compose ps
```

Expected output:
```
NAME                    STATUS
techkatta_mysql         Up
techkatta_mongo         Up
techkatta_redis         Up
techkatta_backend       Up
```

## Step 3: Setup Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## Step 4: Access the Application

Open your browser and visit:
- **Frontend**: http://localhost:5173
- **Backend API Docs**: http://localhost:8000/docs
- **Backend Health**: http://localhost:8000/health

## Step 5: Create Your First Account

1. Go to http://localhost:5173
2. Click "Get Started" or "Register"
3. Fill in the registration form:
   - Email: your-email@example.com
   - Username: yourusername
   - Password: (min 8 characters)
4. Click "Create Account"
5. Login with your credentials

## 🎉 You're All Set!

You should now see the dashboard. Start exploring!

## Common Issues & Solutions

### Issue: Docker containers won't start

**Solution:**
```bash
# Stop all containers
docker-compose down

# Remove volumes and start fresh
docker-compose down -v
docker-compose up -d
```

### Issue: Port already in use

**Solution:**
```bash
# Check what's using the port
lsof -i :8000  # For backend
lsof -i :5173  # For frontend
lsof -i :3306  # For MySQL

# Kill the process or change ports in docker-compose.yml
```

### Issue: Frontend can't connect to backend

**Solution:**
- Check if backend is running: http://localhost:8000/health
- Verify CORS settings in `.env`
- Check browser console for errors

### Issue: Database connection errors

**Solution:**
```bash
# Wait for MySQL to be fully ready (takes ~30 seconds on first start)
docker-compose logs mysql

# Restart backend after MySQL is ready
docker-compose restart backend
```

## Manual Setup (Without Docker)

If you prefer not to use Docker:

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Make sure MySQL, MongoDB, and Redis are running locally
# Update .env with your local database credentials

# Start backend
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

## Next Steps

1. **Explore the API**: Visit http://localhost:8000/docs
2. **Complete your profile**: Add skills, interests, university info
3. **Join communities**: Browse and join tech communities
4. **Find hackathons**: Check out upcoming hackathons
5. **Form teams**: Create or join teams for hackathons

## Development Tips

### Hot Reload
- Frontend: Automatically reloads on file changes
- Backend: Automatically reloads with `--reload` flag

### Database Access

**MySQL:**
```bash
docker exec -it techkatta_mysql mysql -u techkatta_user -p
# Password: techkatta_pass
```

**MongoDB:**
```bash
docker exec -it techkatta_mongo mongosh -u admin -p adminpass
```

**Redis:**
```bash
docker exec -it techkatta_redis redis-cli
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f mysql
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (fresh start)
docker-compose down -v
```

## Testing the API

### Using Swagger UI
1. Go to http://localhost:8000/docs
2. Click "Authorize" button
3. Login to get access token
4. Use the token to test protected endpoints

### Using curl

```bash
# Register a user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "testpass123"
  }'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'

# Get current user (replace TOKEN with your access token)
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer TOKEN"
```

## Project Structure Overview

```
techkatta/
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── api/      # API endpoints
│   │   ├── core/     # Configuration
│   │   ├── models/   # Database models
│   │   ├── ml/       # ML recommendation system
│   │   └── main.py   # Entry point
│   └── requirements.txt
├── frontend/          # React frontend
│   ├── src/
│   │   ├── pages/    # Page components
│   │   ├── services/ # API services
│   │   ├── store/    # State management
│   │   └── App.tsx
│   └── package.json
└── docker-compose.yml
```

## Need Help?

- 📖 Check the full [README.md](./README.md)
- 🔍 Search existing issues on GitHub
- 💬 Ask in the community Discord
- 📧 Email: support@techkatta.com

---

**Happy Coding! 🚀**
