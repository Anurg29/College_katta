from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth, users, resources, jobs, projects, events, mentorship
)

api_router = APIRouter()

# Core Authentication & Users
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])

# Enhanced Features
api_router.include_router(resources.router, prefix="/resources", tags=["Resources"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["Jobs & Internships"])
api_router.include_router(projects.router, prefix="/projects", tags=["Project Showcase"])
api_router.include_router(events.router, prefix="/events", tags=["Events"])
api_router.include_router(mentorship.router, prefix="/mentorship", tags=["Mentorship"])

# TODO: Add more routers
# api_router.include_router(communities.router, prefix="/communities", tags=["Communities"])
# api_router.include_router(posts.router, prefix="/posts", tags=["Posts"])
# api_router.include_router(hackathons.router, prefix="/hackathons", tags=["Hackathons"])
# api_router.include_router(teams.router, prefix="/teams", tags=["Teams"])
# api_router.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])
# api_router.include_router(gamification.router, prefix="/gamification", tags=["Gamification"])
