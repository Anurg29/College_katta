# 🎯 Quick Deployment Reference Card

## 🔥 Firebase Deployment (Frontend)

### Issue Found:
- ❌ **GitHub Actions failing**: Missing `FIREBASE_SERVICE_ACCOUNT` secret
- ❌ **Project ID may be incorrect**: `college-katta-a1b2c`

### Quick Fix:
```bash
# 1. Install Firebase CLI
npm install -g firebase-tools

# 2. Login
firebase login

# 3. Get your project ID
firebase projects:list

# 4. Generate service account key
# Go to: Firebase Console → Project Settings → Service Accounts → Generate New Private Key

# 5. Add to GitHub
# GitHub → Settings → Secrets → Actions → New secret
# Name: FIREBASE_SERVICE_ACCOUNT
# Value: <paste JSON content>

# 6. Update .github/workflows/frontend-deploy.yml
# Change projectId to your actual project ID

# 7. Test locally
cd frontend
npm run build
firebase deploy --only hosting
```

---

## 🗄️ Database Setup

### MongoDB Atlas (5 minutes)
```bash
# 1. Sign up: https://www.mongodb.com/cloud/atlas/register
# 2. Create M0 Free cluster
# 3. Database Access → Add User → techkatta_user
# 4. Network Access → Add IP → 0.0.0.0/0
# 5. Get connection string:

mongodb+srv://techkatta_user:PASSWORD@cluster0.xxxxx.mongodb.net/techkatta
```

### Railway MySQL (3 minutes)
```bash
# 1. Go to: https://railway.app
# 2. New Project → Database → MySQL
# 3. Copy from Variables tab:
#    - MYSQLHOST
#    - MYSQLPORT
#    - MYSQLDATABASE
#    - MYSQLUSER
#    - MYSQLPASSWORD

# 4. Construct URL:
mysql+pymysql://USER:PASSWORD@HOST:PORT/DATABASE
```

---

## 🚂 Railway Backend Deployment

### Quick Deploy:
```bash
# 1. Go to: https://railway.app
# 2. New Project → Deploy from GitHub
# 3. Select: Anurg29/College_katta
# 4. Root Directory: backend
# 5. Add Environment Variables (see below)
# 6. Deploy!
```

### Required Environment Variables:
```env
DATABASE_URL=mysql+pymysql://user:pass@host:port/db
MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net/techkatta
REDIS_URL=redis://host:port
SECRET_KEY=<generate-below>
DEBUG=False
APP_ENV=production
CORS_ORIGINS=["https://your-project.web.app"]
```

### Generate SECRET_KEY:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 🧪 Testing Checklist

### Backend Health Check:
```bash
curl https://your-backend.up.railway.app/health
# Expected: {"status":"healthy"}
```

### API Documentation:
```bash
open https://your-backend.up.railway.app/docs
```

### Frontend:
```bash
open https://your-project.web.app
```

### Test User Registration:
```bash
curl -X POST https://your-backend.up.railway.app/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!@#",
    "full_name": "Test User"
  }'
```

---

## 📋 Deployment Order

1. ✅ **Set up MongoDB Atlas** (5 min)
2. ✅ **Set up Railway MySQL** (3 min)
3. ✅ **Deploy Backend to Railway** (10 min)
4. ✅ **Fix Firebase Secrets** (5 min)
5. ✅ **Update Frontend with Backend URL** (2 min)
6. ✅ **Deploy Frontend to Firebase** (5 min)
7. ✅ **Test End-to-End** (10 min)

**Total Time**: ~40 minutes

---

## 🆘 Quick Troubleshooting

### Firebase Deploy Fails:
```bash
# Check secret exists
# GitHub → Settings → Secrets → FIREBASE_SERVICE_ACCOUNT

# Test locally first
cd frontend && firebase deploy
```

### Backend Won't Start:
```bash
# Check Railway logs
# Railway Dashboard → Your Service → Deployments → View Logs

# Common issues:
# - Missing environment variables
# - Wrong DATABASE_URL format
# - CORS not configured
```

### Database Connection Error:
```bash
# Test MongoDB connection
mongosh "mongodb+srv://user:pass@cluster.mongodb.net/techkatta"

# Test MySQL connection
mysql -h HOST -P PORT -u USER -p DATABASE
```

### CORS Error:
```bash
# Add frontend URL to CORS_ORIGINS in Railway
CORS_ORIGINS=["https://your-project.web.app","http://localhost:5173"]

# Redeploy backend
```

---

## 🔗 Important Links

- **GitHub Repo**: https://github.com/Anurg29/College_katta
- **GitHub Actions**: https://github.com/Anurg29/College_katta/actions
- **Firebase Console**: https://console.firebase.google.com/
- **Railway Dashboard**: https://railway.app/dashboard
- **MongoDB Atlas**: https://cloud.mongodb.com/

---

## 📞 Commands Cheat Sheet

```bash
# Frontend
cd frontend
npm install
npm run build
firebase deploy

# Backend (local)
cd backend
python3 -m uvicorn app.main:app --reload

# Docker
docker-compose up -d
docker-compose logs -f
docker-compose down

# Git
git add -A
git commit -m "message"
git push origin main

# Generate secrets
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Test API
curl http://localhost:8000/health
curl https://your-backend.up.railway.app/health
```

---

**Last Updated**: November 30, 2025  
**For detailed instructions**: See `PRODUCTION_DEPLOYMENT.md`
