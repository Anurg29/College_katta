# TechKatta - Social Platform for Engineering Students

<div align="center">
  <h3>Connect. Collaborate. Create.</h3>
  <p>The ultimate platform for engineering students to network, find hackathon teammates, and build amazing projects together.</p>
</div>

## 🚀 Features

### ✅ Fully Implemented Features

#### Core Platform
- **👥 User Management**: Registration, authentication, profile management with skills and interests
- **🏘️ Tech Communities**: Join and create communities based on technology interests
- **🏆 Hackathon Listings**: Browse and register for hackathons
- **🤝 Team Formation**: Find teammates with complementary skills for hackathons
- **⭐ Reputation System**: Earn reputation through contributions and engagement

#### 📚 Resource Sharing Hub (NEW!)
- **Upload & Share**: Study materials, notes, assignments, projects, books, research papers, code
- **Smart Organization**: Subject-wise, semester-based, university-specific categorization
- **Community Engagement**: Upvote/downvote system, download tracking, view analytics
- **Quality Control**: Verified resources, community moderation
- **Advanced Search**: Filter by subject, semester, university, category, tags

#### 💼 Job & Internship Board (NEW!)
- **Job Postings**: Internships, full-time, part-time, contract, freelance positions
- **Smart Filtering**: By type, location (remote/onsite/hybrid), salary, experience, skills
- **Application System**: One-click apply, resume management, application tracking
- **Status Updates**: Pending, reviewing, shortlisted, rejected, accepted
- **Recruiter Dashboard**: Manage applications, update statuses, add notes

#### 📊 Project Showcase (NEW!)
- **Display Projects**: With images, videos, live demos, GitHub integration
- **Tech Stack Tagging**: Categorize by technologies used
- **Community Interaction**: Like, comment, share projects
- **Collaboration**: Add collaborators, define roles, team projects
- **GitHub Integration**: Auto-fetch stars, forks, README

#### 📅 Event Calendar (NEW!)
- **Event Types**: Workshops, hackathons, webinars, meetups, conferences, seminars
- **RSVP System**: Going/Maybe/Not Going with capacity management
- **Virtual & In-Person**: Support for both with meeting links
- **Event Discovery**: Filter by type, date, location
- **Personal Dashboard**: Track attending and organizing events

#### 🎓 Mentorship Program (NEW!)
- **Mentor Registration**: Expertise areas, availability, experience, ratings
- **Mentor Discovery**: Browse and filter mentors by expertise, rating, availability
- **Mentorship Requests**: Request mentorship with goals and messages
- **Session Management**: Schedule, track, rate sessions
- **Feedback System**: Rate mentors and sessions (1-5 stars)

### 🚧 Coming Soon
- **💬 Real-time Chat**: WebSocket-powered chat rooms
- **📝 Discussion Forums**: Post questions, share articles
- **🤖 ML Recommendations**: Personalized content and team suggestions
- **🔔 Notifications**: Real-time notifications
- **🏅 Gamification**: Badges, achievements, leaderboards
- **📱 Mobile App**: Progressive Web App (PWA)


## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Databases**: 
  - MySQL 8.0+ (relational data)
  - MongoDB 6.0+ (posts, chat, notifications)
  - Redis 7.0+ (caching, sessions)
- **Authentication**: JWT with refresh tokens
- **ML/AI**: scikit-learn, pandas, numpy
- **WebSockets**: FastAPI WebSockets
- **Task Queue**: Celery + Redis

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **State Management**: Zustand
- **Styling**: TailwindCSS
- **Animations**: Framer Motion
- **Forms**: React Hook Form + Zod
- **HTTP Client**: Axios
- **Real-time**: Socket.io Client

### DevOps
- **Containerization**: Docker + Docker Compose
- **Database Migrations**: Alembic

## 📋 Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.11+
- MySQL 8.0+
- MongoDB 6.0+
- Redis 7.0+
- Docker & Docker Compose (recommended)

## 🚀 Quick Start

### Option 1: Using Docker (Recommended)

1. **Clone the repository**
```bash
cd /Users/anuragdineshrokade/Documents/College_katta
```

2. **Create environment file**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Start all services**
```bash
docker-compose up -d
```

4. **Access the application**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Option 2: Manual Setup

#### Backend Setup

1. **Create virtual environment**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up databases**
- Start MySQL and create database `techkatta`
- Start MongoDB
- Start Redis

4. **Configure environment**
```bash
cp ../.env.example .env
# Edit .env with your database credentials
```

5. **Run database migrations**
```bash
# The tables will be created automatically on first run
```

6. **Start the backend server**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

1. **Install dependencies**
```bash
cd frontend
npm install
```

2. **Start development server**
```bash
npm run dev
```

3. **Access the application**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000

## 📁 Project Structure

```
techkatta/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/    # API endpoints
│   │   ├── core/                # Config, security, database
│   │   ├── models/              # SQLAlchemy & Pydantic models
│   │   ├── schemas/             # Request/response schemas
│   │   ├── services/            # Business logic
│   │   ├── ml/                  # ML recommendation system
│   │   └── main.py              # FastAPI app
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/          # Reusable components
│   │   ├── pages/               # Page components
│   │   ├── services/            # API services
│   │   ├── store/               # Zustand stores
│   │   ├── types/               # TypeScript types
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
├── docker-compose.yml
├── .env.example
└── README.md
```

## 🔑 Environment Variables

Key environment variables (see `.env.example` for complete list):

```env
# Database
DATABASE_URL=mysql+pymysql://user:pass@localhost:3306/techkatta
MONGODB_URL=mongodb://admin:pass@localhost:27017
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-min-32-characters
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=["http://localhost:5173"]
```

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key API Endpoints

#### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/refresh` - Refresh access token

#### Users
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update current user
- `GET /api/v1/users/{user_id}/profile` - Get user profile

#### Communities (TODO)
- `GET /api/v1/communities` - List communities
- `POST /api/v1/communities` - Create community
- `POST /api/v1/communities/{id}/join` - Join community

#### Hackathons (TODO)
- `GET /api/v1/hackathons` - List hackathons
- `POST /api/v1/hackathons` - Create hackathon

#### Teams (TODO)
- `GET /api/v1/teams` - List teams
- `POST /api/v1/teams` - Create team
- `POST /api/v1/teams/{id}/request` - Request to join team

## 🤖 ML Recommendation System

The platform uses a hybrid recommendation system:

1. **Collaborative Filtering**: Analyzes user interaction patterns
2. **Content-Based Filtering**: Matches based on skills, interests, and profile data
3. **Team Matching**: Suggests teammates with complementary skills

### Training the Model

```python
from app.ml.inference import recommender

# Train collaborative filter with user interactions
interactions = [
    {'user_id': 'user1', 'target_id': 'post1', 'interaction_type': 'like'},
    # ... more interactions
]
recommender.train_collaborative(interactions)

# Add user profiles
recommender.add_user_profile('user1', skills=['Python', 'React'], interests=['AI', 'Web'])

# Get recommendations
recommendations = recommender.recommend('user1', n=10)
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## 🚢 Deployment

### Production Checklist

1. **Environment Variables**
   - Set strong `SECRET_KEY`
   - Configure production database URLs
   - Set `DEBUG=False`
   - Configure CORS for production domain

2. **Database**
   - Set up managed MySQL (AWS RDS, Google Cloud SQL)
   - Set up managed MongoDB (MongoDB Atlas)
   - Set up Redis (AWS ElastiCache, Redis Cloud)

3. **Backend**
   - Deploy to Railway, Render, or AWS
   - Set up SSL/TLS certificates
   - Configure CDN for static files

4. **Frontend**
   - Build production bundle: `npm run build`
   - Deploy to Vercel, Netlify, or AWS S3 + CloudFront

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📝 Development Roadmap

### Phase 1: MVP ✅
- [x] User authentication & profiles
- [x] Basic project structure
- [x] Database models
- [x] Landing page & auth UI

### Phase 2: Core Features (In Progress)
- [ ] Communities CRUD
- [ ] Post creation & commenting
- [ ] Real-time chat
- [ ] Hackathon listings
- [ ] Team formation

### Phase 3: ML Integration
- [ ] Content recommendations
- [ ] Team member matching
- [ ] Learning path suggestions

### Phase 4: Polish & Scale
- [ ] Performance optimization
- [ ] Advanced search
- [ ] Analytics dashboard
- [ ] Mobile app (React Native)

## 📄 License

This project is licensed under the MIT License.

## 👥 Team

Built with ❤️ by engineering students, for engineering students.

## 📞 Support

For support, email support@techkatta.com or join our Discord community.

---

<div align="center">
  <strong>Happy Coding! 🚀</strong>
</div>
