# 🚀 Production Deployment Guide - College Katta

## 📊 Deployment Status

### Current Issues Identified:
1. ❌ **Firebase Deployment**: Failed - Missing service account secret
2. ⚠️ **Production Databases**: Not configured
3. ⚠️ **Backend Deployment**: Not deployed to cloud
4. ⚠️ **End-to-End Testing**: Pending

---

## 🔥 Step 1: Firebase Frontend Deployment

### Issue Found:
**Error**: `The process '/opt/hostedtoolcache/node/18.20.8/x64/bin/npx' failed with exit code 1`

**Root Cause**: Missing or incorrect `FIREBASE_SERVICE_ACCOUNT` secret in GitHub

### Solution:

#### A. Install Firebase CLI
```bash
npm install -g firebase-tools
```

#### B. Login to Firebase
```bash
firebase login
```

#### C. Initialize Firebase Project
```bash
cd frontend

# Initialize Firebase (if not already done)
firebase init hosting

# Select options:
# - Use an existing project or create new
# - Public directory: dist
# - Configure as single-page app: Yes
# - Set up automatic builds with GitHub: No (we'll use GitHub Actions)
```

#### D. Get Your Firebase Project ID
```bash
# List your Firebase projects
firebase projects:list

# Note the Project ID (e.g., college-katta-xxxxx)
```

#### E. Create Firebase Service Account
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project
3. Click the gear icon ⚙️ → **Project Settings**
4. Go to **Service Accounts** tab
5. Click **Generate New Private Key**
6. Download the JSON file (keep it secure!)

#### F. Add Secret to GitHub
1. Go to your GitHub repository: https://github.com/Anurg29/College_katta
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `FIREBASE_SERVICE_ACCOUNT`
5. Value: Paste the entire content of the JSON file you downloaded
6. Click **Add secret**

#### G. Update Workflow File
Update `.github/workflows/frontend-deploy.yml` with correct project ID:

```yaml
- name: Deploy to Firebase
  uses: FirebaseExtended/action-hosting-deploy@v0
  with:
    repoToken: '${{ secrets.GITHUB_TOKEN }}'
    firebaseServiceAccount: '${{ secrets.FIREBASE_SERVICE_ACCOUNT }}'
    channelId: live
    projectId: YOUR_ACTUAL_PROJECT_ID  # Update this!
```

#### H. Test Deployment Locally
```bash
cd frontend

# Build the project
npm run build

# Test Firebase deployment
firebase deploy --only hosting

# If successful, you'll get a hosting URL like:
# https://your-project.web.app
```

---

## 🗄️ Step 2: Set Up Production Databases

### A. MongoDB Atlas (Free Tier)

#### 1. Create MongoDB Atlas Account
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
2. Sign up for free account
3. Create a new cluster (M0 Free tier)

#### 2. Configure Database
```bash
# In MongoDB Atlas Dashboard:
# 1. Click "Database" → "Browse Collections" → "Create Database"
# 2. Database name: techkatta
# 3. Collection name: users (we'll create more later)
```

#### 3. Set Up Database User
```bash
# In Atlas Dashboard:
# 1. Click "Database Access"
# 2. Click "Add New Database User"
# 3. Username: techkatta_user
# 4. Password: [Generate strong password]
# 5. Database User Privileges: Read and write to any database
# 6. Click "Add User"
```

#### 4. Configure Network Access
```bash
# In Atlas Dashboard:
# 1. Click "Network Access"
# 2. Click "Add IP Address"
# 3. Click "Allow Access from Anywhere" (0.0.0.0/0)
#    OR add specific Railway/Render IP addresses
# 4. Click "Confirm"
```

#### 5. Get Connection String
```bash
# In Atlas Dashboard:
# 1. Click "Database" → "Connect"
# 2. Choose "Connect your application"
# 3. Driver: Python, Version: 3.12 or later
# 4. Copy connection string:

mongodb+srv://techkatta_user:<password>@cluster0.xxxxx.mongodb.net/techkatta?retryWrites=true&w=majority

# Replace <password> with your actual password
```

### B. Railway MySQL Database

#### 1. Create Railway Account
1. Go to [Railway.app](https://railway.app)
2. Sign up with GitHub
3. Create new project

#### 2. Add MySQL Database
```bash
# In Railway Dashboard:
# 1. Click "New" → "Database" → "Add MySQL"
# 2. Wait for provisioning (1-2 minutes)
# 3. Click on MySQL service
# 4. Go to "Variables" tab
# 5. Copy these values:
#    - MYSQLHOST
#    - MYSQLPORT
#    - MYSQLDATABASE
#    - MYSQLUSER
#    - MYSQLPASSWORD
```

#### 3. Construct DATABASE_URL
```bash
# Format:
mysql+pymysql://MYSQLUSER:MYSQLPASSWORD@MYSQLHOST:MYSQLPORT/MYSQLDATABASE

# Example:
mysql+pymysql://root:password123@containers-us-west-1.railway.app:6543/railway
```

### C. Railway Redis (Optional but Recommended)

#### 1. Add Redis to Railway
```bash
# In Railway Dashboard:
# 1. Click "New" → "Database" → "Add Redis"
# 2. Wait for provisioning
# 3. Go to "Variables" tab
# 4. Copy REDIS_URL
```

---

## 🚂 Step 3: Deploy Backend to Railway

### A. Prepare for Deployment

#### 1. Update requirements.txt (if needed)
```bash
cd backend

# Ensure all dependencies are listed
cat requirements.txt

# Add any missing packages
```

#### 2. Verify Procfile
```bash
# File: backend/Procfile
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

#### 3. Create runtime.txt
```bash
# File: backend/runtime.txt
python-3.11.0
```

### B. Deploy to Railway

#### 1. Connect GitHub Repository
```bash
# In Railway Dashboard:
# 1. Click "New Project"
# 2. Select "Deploy from GitHub repo"
# 3. Choose "Anurg29/College_katta"
# 4. Select "backend" directory as root
```

#### 2. Configure Environment Variables
```bash
# In Railway → Your Service → Variables tab, add:

# Database URLs (from Step 2)
DATABASE_URL=mysql+pymysql://user:pass@host:port/database
MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net/techkatta
REDIS_URL=redis://host:port

# Security
SECRET_KEY=<generate-with-command-below>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Application
APP_NAME=TechKatta
APP_ENV=production
DEBUG=False
API_V1_PREFIX=/api/v1

# CORS - Add your Firebase hosting URL
CORS_ORIGINS=["https://your-project.web.app","https://your-project.firebaseapp.com"]
```

#### 3. Generate SECRET_KEY
```bash
# Run this command to generate a secure secret key:
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Copy the output and use it as SECRET_KEY
```

#### 4. Deploy
```bash
# Railway will automatically:
# 1. Detect Procfile
# 2. Install dependencies from requirements.txt
# 3. Run the web command
# 4. Assign a public URL

# Monitor deployment in Railway dashboard
# Check logs for any errors
```

#### 5. Get Your Backend URL
```bash
# In Railway Dashboard:
# 1. Click on your service
# 2. Go to "Settings" tab
# 3. Under "Domains", you'll see your Railway URL
# Example: https://college-katta-production.up.railway.app
```

---

## 🔄 Step 4: Update Frontend to Use Production Backend

### A. Create Environment File for Production

Create `frontend/.env.production`:
```env
VITE_API_URL=https://your-backend.up.railway.app/api/v1
```

### B. Update API Configuration

File: `frontend/src/services/api.ts` (or similar):
```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});
```

### C. Update CORS in Backend

Update Railway environment variable:
```env
CORS_ORIGINS=["https://your-project.web.app","https://your-project.firebaseapp.com","http://localhost:5173"]
```

### D. Rebuild and Redeploy Frontend
```bash
cd frontend
npm run build
firebase deploy --only hosting
```

---

## 🧪 Step 5: End-to-End Testing

### A. Test Backend API

#### 1. Health Check
```bash
# Replace with your Railway URL
curl https://your-backend.up.railway.app/health

# Expected response:
# {"status":"healthy"}
```

#### 2. Root Endpoint
```bash
curl https://your-backend.up.railway.app/

# Expected response:
# {
#   "message": "Welcome to TechKatta API",
#   "version": "1.0.0",
#   "docs": "/docs",
#   "status": "running"
# }
```

#### 3. API Documentation
```bash
# Open in browser:
https://your-backend.up.railway.app/docs
```

### B. Test Database Connections

#### 1. Create Test User (via API)
```bash
curl -X POST https://your-backend.up.railway.app/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!@#",
    "full_name": "Test User",
    "university": "Test University"
  }'

# Expected: User created successfully
```

#### 2. Login
```bash
curl -X POST https://your-backend.up.railway.app/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!@#"
  }'

# Expected: Returns access_token and refresh_token
```

### C. Test Frontend

#### 1. Open Firebase Hosting URL
```bash
# Open in browser:
https://your-project.web.app
```

#### 2. Test User Registration
1. Click "Sign Up"
2. Fill in registration form
3. Submit
4. Check if user is created

#### 3. Test User Login
1. Click "Login"
2. Enter credentials
3. Submit
4. Check if redirected to dashboard

#### 4. Test API Integration
1. Try creating a resource
2. Try viewing resources
3. Check if data persists

### D. Monitor Logs

#### Backend Logs (Railway)
```bash
# In Railway Dashboard:
# 1. Click on your service
# 2. Go to "Deployments" tab
# 3. Click on latest deployment
# 4. View logs in real-time
```

#### Frontend Logs (Firebase)
```bash
# In Firebase Console:
# 1. Go to your project
# 2. Click "Hosting"
# 3. View deployment history
```

---

## 📋 Deployment Checklist

### Pre-Deployment
- [ ] All code committed to GitHub
- [ ] Environment variables documented
- [ ] Database schemas finalized
- [ ] API endpoints tested locally
- [ ] Frontend builds successfully

### Firebase Setup
- [ ] Firebase project created
- [ ] Firebase CLI installed
- [ ] Service account key generated
- [ ] GitHub secret `FIREBASE_SERVICE_ACCOUNT` added
- [ ] Project ID updated in workflow
- [ ] Local deployment tested

### Database Setup
- [ ] MongoDB Atlas cluster created
- [ ] MongoDB user created
- [ ] MongoDB network access configured
- [ ] Connection string obtained
- [ ] Railway MySQL database created
- [ ] MySQL connection string obtained
- [ ] Railway Redis created (optional)

### Backend Deployment
- [ ] Railway account created
- [ ] GitHub repository connected
- [ ] Environment variables configured
- [ ] SECRET_KEY generated
- [ ] CORS origins updated
- [ ] Deployment successful
- [ ] Backend URL obtained

### Integration
- [ ] Frontend updated with backend URL
- [ ] CORS configured correctly
- [ ] Frontend redeployed

### Testing
- [ ] Backend health check passes
- [ ] API documentation accessible
- [ ] User registration works
- [ ] User login works
- [ ] Database operations work
- [ ] Frontend loads correctly
- [ ] Frontend-backend communication works

---

## 🐛 Troubleshooting

### Firebase Deployment Fails
**Error**: `exit code 1`
**Solution**: 
1. Check `FIREBASE_SERVICE_ACCOUNT` secret exists
2. Verify project ID is correct
3. Ensure service account has proper permissions

### Backend Won't Start on Railway
**Error**: `Application failed to respond`
**Solution**:
1. Check logs for errors
2. Verify all environment variables are set
3. Ensure DATABASE_URL is correct
4. Check if port binding is correct (`$PORT`)

### Database Connection Errors
**Error**: `Connection refused` or `Authentication failed`
**Solution**:
1. Verify connection strings are correct
2. Check database user credentials
3. Ensure network access is configured (MongoDB Atlas)
4. Test connection locally first

### CORS Errors in Frontend
**Error**: `Access to fetch blocked by CORS policy`
**Solution**:
1. Add frontend URL to `CORS_ORIGINS` in backend
2. Ensure format is correct: `["https://domain.com"]`
3. Redeploy backend after updating

---

## 📊 Expected Results

### After Successful Deployment:

**Frontend**: https://your-project.web.app
- ✅ Loads without errors
- ✅ Can register new users
- ✅ Can login
- ✅ Can perform CRUD operations

**Backend**: https://your-backend.up.railway.app
- ✅ Health check returns 200
- ✅ API docs accessible at `/docs`
- ✅ All endpoints functional
- ✅ Database connections working

**Databases**:
- ✅ MongoDB Atlas storing user data
- ✅ MySQL storing relational data
- ✅ Redis caching (if configured)

---

## 🔐 Security Checklist

- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` generated
- [ ] Database passwords are strong
- [ ] GitHub secrets properly configured
- [ ] API rate limiting enabled (if applicable)
- [ ] HTTPS enforced on all endpoints
- [ ] Environment variables never committed to Git

---

## 📞 Quick Commands Reference

### Firebase
```bash
# Login
firebase login

# List projects
firebase projects:list

# Deploy
firebase deploy --only hosting

# View logs
firebase hosting:channel:list
```

### Railway
```bash
# Install Railway CLI (optional)
npm install -g @railway/cli

# Login
railway login

# Link project
railway link

# View logs
railway logs

# Open dashboard
railway open
```

### Testing
```bash
# Test backend health
curl https://your-backend.up.railway.app/health

# Test frontend
curl https://your-project.web.app

# Check API docs
open https://your-backend.up.railway.app/docs
```

---

## 🎯 Next Steps After Deployment

1. **Set up monitoring**: Add error tracking (Sentry, LogRocket)
2. **Configure analytics**: Google Analytics, Mixpanel
3. **Set up CI/CD**: Automated testing before deployment
4. **Add custom domain**: Configure custom domain for frontend
5. **Enable caching**: Configure Redis for better performance
6. **Set up backups**: Automated database backups
7. **Load testing**: Test with expected user load
8. **Security audit**: Review security best practices

---

**Last Updated**: November 30, 2025, 6:30 PM IST  
**Status**: Ready for production deployment

**Need Help?** Check the logs first, then refer to this guide's troubleshooting section.
