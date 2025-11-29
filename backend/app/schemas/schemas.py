from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    STUDENT = "student"
    MENTOR = "mentor"
    RECRUITER = "recruiter"
    ADMIN = "admin"


class ProficiencyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    id: str
    role: UserRole
    is_verified: bool
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Profile Schemas
class ProfileBase(BaseModel):
    bio: Optional[str] = None
    university: Optional[str] = None
    graduation_year: Optional[int] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    location: Optional[str] = None


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass


class ProfileResponse(ProfileBase):
    id: str
    user_id: str
    avatar_url: Optional[str] = None
    reputation_score: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Skill Schemas
class SkillBase(BaseModel):
    name: str
    category: Optional[str] = None


class SkillCreate(SkillBase):
    pass


class SkillResponse(SkillBase):
    id: str
    
    class Config:
        from_attributes = True


class UserSkillCreate(BaseModel):
    skill_id: str
    proficiency_level: ProficiencyLevel = ProficiencyLevel.INTERMEDIATE


class UserSkillResponse(BaseModel):
    skill: SkillResponse
    proficiency_level: ProficiencyLevel
    
    class Config:
        from_attributes = True


# Interest Schemas
class InterestBase(BaseModel):
    name: str
    category: Optional[str] = None


class InterestCreate(InterestBase):
    pass


class InterestResponse(InterestBase):
    id: str
    
    class Config:
        from_attributes = True


# Community Schemas
class CommunityBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    category: Optional[str] = None
    is_private: bool = False


class CommunityCreate(CommunityBase):
    slug: str = Field(..., min_length=3, max_length=100)


class CommunityUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    is_private: Optional[bool] = None


class CommunityResponse(CommunityBase):
    id: str
    slug: str
    icon_url: Optional[str] = None
    banner_url: Optional[str] = None
    created_by: Optional[str] = None
    member_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Hackathon Schemas
class HackathonMode(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    HYBRID = "hybrid"


class HackathonStatus(str, Enum):
    UPCOMING = "upcoming"
    ONGOING = "ongoing"
    COMPLETED = "completed"


class HackathonBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    description: Optional[str] = None
    organizer: Optional[str] = None
    start_date: datetime
    end_date: datetime
    registration_deadline: Optional[datetime] = None
    mode: HackathonMode = HackathonMode.ONLINE
    location: Optional[str] = None
    prize_pool: Optional[str] = None
    website_url: Optional[str] = None
    max_team_size: int = 4
    min_team_size: int = 1


class HackathonCreate(HackathonBase):
    pass


class HackathonUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[HackathonStatus] = None


class HackathonResponse(HackathonBase):
    id: str
    banner_url: Optional[str] = None
    status: HackathonStatus
    created_by: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# Team Schemas
class TeamStatus(str, Enum):
    FORMING = "forming"
    COMPLETE = "complete"
    DISBANDED = "disbanded"


class TeamBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    max_members: int = 4


class TeamCreate(TeamBase):
    hackathon_id: str
    required_skills: Optional[List[str]] = []


class TeamUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_open: Optional[bool] = None


class TeamResponse(TeamBase):
    id: str
    hackathon_id: str
    leader_id: Optional[str] = None
    current_members: int
    is_open: bool
    status: TeamStatus
    created_at: datetime
    
    class Config:
        from_attributes = True


# Team Request Schemas
class TeamRequestCreate(BaseModel):
    message: Optional[str] = None


class TeamRequestResponse(BaseModel):
    id: str
    team_id: str
    user_id: str
    message: Optional[str] = None
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# Token Schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None
    type: Optional[str] = None
