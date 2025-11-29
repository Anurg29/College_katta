from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum


# ==================== RESOURCE SCHEMAS ====================

class ResourceCategoryEnum(str, Enum):
    NOTES = "notes"
    ASSIGNMENTS = "assignments"
    PROJECTS = "projects"
    BOOKS = "books"
    PAPERS = "papers"
    CODE = "code"
    OTHER = "other"


class ResourceBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    description: Optional[str] = None
    category: ResourceCategoryEnum
    subject: Optional[str] = Field(None, max_length=100)
    semester: Optional[int] = Field(None, ge=1, le=10)
    university: Optional[str] = Field(None, max_length=200)
    tags: Optional[List[str]] = []


class ResourceCreate(ResourceBase):
    file_url: str
    file_type: Optional[str] = None
    file_size: Optional[int] = None


class ResourceUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = None
    subject: Optional[str] = None
    semester: Optional[int] = Field(None, ge=1, le=10)
    tags: Optional[List[str]] = None


class ResourceResponse(ResourceBase):
    id: str
    file_url: str
    file_type: Optional[str]
    file_size: Optional[int]
    upvotes: int
    downvotes: int
    downloads: int
    views: int
    user_id: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ResourceVoteCreate(BaseModel):
    vote_type: str = Field(..., pattern="^(upvote|downvote)$")


# ==================== JOB BOARD SCHEMAS ====================

class JobTypeEnum(str, Enum):
    INTERNSHIP = "internship"
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    FREELANCE = "freelance"


class JobLocationEnum(str, Enum):
    REMOTE = "remote"
    ONSITE = "onsite"
    HYBRID = "hybrid"


class ApplicationStatusEnum(str, Enum):
    PENDING = "pending"
    REVIEWING = "reviewing"
    SHORTLISTED = "shortlisted"
    REJECTED = "rejected"
    ACCEPTED = "accepted"


class JobPostingBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    company: str = Field(..., min_length=2, max_length=200)
    company_logo: Optional[str] = None
    description: str = Field(..., min_length=50)
    requirements: Optional[str] = None
    responsibilities: Optional[str] = None
    job_type: JobTypeEnum
    location_type: JobLocationEnum
    location: Optional[str] = None
    salary_min: Optional[int] = Field(None, ge=0)
    salary_max: Optional[int] = Field(None, ge=0)
    salary_currency: str = "USD"
    skills_required: Optional[List[str]] = []
    experience_min: int = Field(0, ge=0)
    experience_max: Optional[int] = Field(None, ge=0)
    application_url: Optional[str] = None
    expires_at: Optional[datetime] = None


class JobPostingCreate(JobPostingBase):
    pass


class JobPostingUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    description: Optional[str] = None
    requirements: Optional[str] = None
    responsibilities: Optional[str] = None
    location: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    skills_required: Optional[List[str]] = None
    is_active: Optional[bool] = None
    expires_at: Optional[datetime] = None


class JobPostingResponse(JobPostingBase):
    id: str
    posted_by: str
    views: int
    applications_count: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class JobApplicationCreate(BaseModel):
    resume_url: str
    cover_letter: Optional[str] = None


class JobApplicationResponse(BaseModel):
    id: str
    job_id: str
    user_id: str
    resume_url: str
    cover_letter: Optional[str]
    status: ApplicationStatusEnum
    applied_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ResumeCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    file_url: str
    is_primary: bool = False


class ResumeResponse(BaseModel):
    id: str
    user_id: str
    title: str
    file_url: str
    is_primary: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== PROJECT SCHEMAS ====================

class ProjectBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    description: str = Field(..., min_length=10)
    detailed_description: Optional[str] = None
    tech_stack: Optional[List[str]] = []
    github_url: Optional[str] = None
    demo_url: Optional[str] = None
    video_url: Optional[str] = None
    images: Optional[List[str]] = []
    category: Optional[str] = None
    tags: Optional[List[str]] = []


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = None
    detailed_description: Optional[str] = None
    tech_stack: Optional[List[str]] = None
    github_url: Optional[str] = None
    demo_url: Optional[str] = None
    video_url: Optional[str] = None
    images: Optional[List[str]] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None


class ProjectResponse(ProjectBase):
    id: str
    user_id: str
    likes: int
    views: int
    github_stars: int
    github_forks: int
    is_featured: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectCommentCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)
    parent_id: Optional[str] = None


class ProjectCommentResponse(BaseModel):
    id: str
    project_id: str
    user_id: str
    content: str
    parent_id: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== MENTORSHIP SCHEMAS ====================

class MentorshipStatusEnum(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class SessionStatusEnum(str, Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


class MentorProfileCreate(BaseModel):
    expertise: List[str] = Field(..., min_items=1)
    availability: dict = {}
    max_mentees: int = Field(5, ge=1, le=20)
    bio: Optional[str] = None
    years_experience: Optional[int] = Field(None, ge=0)
    hourly_rate: float = Field(0.0, ge=0.0)


class MentorProfileUpdate(BaseModel):
    expertise: Optional[List[str]] = None
    availability: Optional[dict] = None
    max_mentees: Optional[int] = Field(None, ge=1, le=20)
    bio: Optional[str] = None
    years_experience: Optional[int] = None
    hourly_rate: Optional[float] = None
    is_active: Optional[bool] = None


class MentorProfileResponse(BaseModel):
    user_id: str
    expertise: List[str]
    availability: dict
    max_mentees: int
    current_mentees: int
    bio: Optional[str]
    years_experience: Optional[int]
    hourly_rate: float
    rating: float
    total_sessions: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class MentorshipRequestCreate(BaseModel):
    mentor_id: str
    message: Optional[str] = None
    goals: Optional[str] = None


class MentorshipResponse(BaseModel):
    id: str
    mentee_id: str
    mentor_id: str
    status: MentorshipStatusEnum
    message: Optional[str]
    goals: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class SessionCreate(BaseModel):
    mentorship_id: str
    scheduled_at: datetime
    duration: int = Field(60, ge=15, le=180)
    meeting_url: Optional[str] = None
    notes: Optional[str] = None


class SessionUpdate(BaseModel):
    scheduled_at: Optional[datetime] = None
    duration: Optional[int] = Field(None, ge=15, le=180)
    meeting_url: Optional[str] = None
    notes: Optional[str] = None
    feedback: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    status: Optional[SessionStatusEnum] = None


class SessionResponse(BaseModel):
    id: str
    mentorship_id: str
    scheduled_at: datetime
    duration: int
    meeting_url: Optional[str]
    notes: Optional[str]
    feedback: Optional[str]
    rating: Optional[int]
    status: SessionStatusEnum
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== EVENT SCHEMAS ====================

class EventTypeEnum(str, Enum):
    WORKSHOP = "workshop"
    HACKATHON = "hackathon"
    WEBINAR = "webinar"
    MEETUP = "meetup"
    CONFERENCE = "conference"
    SEMINAR = "seminar"


class RSVPStatusEnum(str, Enum):
    GOING = "going"
    MAYBE = "maybe"
    NOT_GOING = "not_going"


class EventBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=20)
    event_type: EventTypeEnum
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    is_virtual: bool = False
    meeting_url: Optional[str] = None
    banner_url: Optional[str] = None
    max_attendees: Optional[int] = Field(None, ge=1)
    tags: Optional[List[str]] = []


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    is_virtual: Optional[bool] = None
    meeting_url: Optional[str] = None
    banner_url: Optional[str] = None
    max_attendees: Optional[int] = None
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None


class EventResponse(EventBase):
    id: str
    organizer_id: str
    current_attendees: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EventRSVPCreate(BaseModel):
    rsvp_status: RSVPStatusEnum


# ==================== GAMIFICATION SCHEMAS ====================

class BadgeRarityEnum(str, Enum):
    COMMON = "common"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


class BadgeResponse(BaseModel):
    id: str
    name: str
    description: str
    icon_url: Optional[str]
    rarity: BadgeRarityEnum
    points: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserBadgeResponse(BaseModel):
    badge_id: str
    earned_at: datetime
    badge: BadgeResponse

    class Config:
        from_attributes = True


class AchievementResponse(BaseModel):
    id: str
    name: str
    description: str
    icon_url: Optional[str]
    points: int
    category: str
    max_progress: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserAchievementResponse(BaseModel):
    achievement_id: str
    progress: int
    completed: bool
    completed_at: Optional[datetime]
    achievement: AchievementResponse

    class Config:
        from_attributes = True


class LeaderboardResponse(BaseModel):
    user_id: str
    total_points: int
    rank: int
    category: str
    weekly_points: int
    monthly_points: int

    class Config:
        from_attributes = True
