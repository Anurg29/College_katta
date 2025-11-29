from sqlalchemy import Column, String, Boolean, Integer, Text, Enum, TIMESTAMP, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid
import enum


def generate_uuid():
    return str(uuid.uuid4())


# ==================== RESOURCE SHARING ====================

class ResourceCategory(str, enum.Enum):
    NOTES = "notes"
    ASSIGNMENTS = "assignments"
    PROJECTS = "projects"
    BOOKS = "books"
    PAPERS = "papers"
    CODE = "code"
    OTHER = "other"


class Resource(Base):
    __tablename__ = "resources"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    file_url = Column(String(500), nullable=False)
    file_type = Column(String(50))
    file_size = Column(Integer)  # in bytes
    category = Column(Enum(ResourceCategory), nullable=False, index=True)
    subject = Column(String(100), index=True)
    semester = Column(Integer, index=True)
    university = Column(String(200), index=True)
    tags = Column(JSON)  # Array of tags
    upvotes = Column(Integer, default=0)
    downvotes = Column(Integer, default=0)
    downloads = Column(Integer, default=0)
    views = Column(Integer, default=0)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), index=True)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    votes = relationship("ResourceVote", back_populates="resource", cascade="all, delete-orphan")


class ResourceVote(Base):
    __tablename__ = "resource_votes"
    
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    resource_id = Column(String(36), ForeignKey("resources.id", ondelete="CASCADE"), primary_key=True)
    vote_type = Column(Enum("upvote", "downvote", name="vote_type"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    resource = relationship("Resource", back_populates="votes")


# ==================== JOB BOARD ====================

class JobType(str, enum.Enum):
    INTERNSHIP = "internship"
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    FREELANCE = "freelance"


class JobLocation(str, enum.Enum):
    REMOTE = "remote"
    ONSITE = "onsite"
    HYBRID = "hybrid"


class ApplicationStatus(str, enum.Enum):
    PENDING = "pending"
    REVIEWING = "reviewing"
    SHORTLISTED = "shortlisted"
    REJECTED = "rejected"
    ACCEPTED = "accepted"


class JobPosting(Base):
    __tablename__ = "job_postings"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(200), nullable=False, index=True)
    company = Column(String(200), nullable=False, index=True)
    company_logo = Column(String(500))
    description = Column(Text, nullable=False)
    requirements = Column(Text)
    responsibilities = Column(Text)
    job_type = Column(Enum(JobType), nullable=False, index=True)
    location_type = Column(Enum(JobLocation), nullable=False, index=True)
    location = Column(String(200))
    salary_min = Column(Integer)
    salary_max = Column(Integer)
    salary_currency = Column(String(10), default="USD")
    skills_required = Column(JSON)  # Array of skills
    experience_min = Column(Integer, default=0)  # in years
    experience_max = Column(Integer)
    application_url = Column(String(500))
    posted_by = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    views = Column(Integer, default=0)
    applications_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True, index=True)
    expires_at = Column(TIMESTAMP, index=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), index=True)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    applications = relationship("JobApplication", back_populates="job", cascade="all, delete-orphan")


class JobApplication(Base):
    __tablename__ = "job_applications"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    job_id = Column(String(36), ForeignKey("job_postings.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    resume_url = Column(String(500), nullable=False)
    cover_letter = Column(Text)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.PENDING, index=True)
    notes = Column(Text)  # Recruiter notes
    applied_at = Column(TIMESTAMP, server_default=func.now(), index=True)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    job = relationship("JobPosting", back_populates="applications")


class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    file_url = Column(String(500), nullable=False)
    is_primary = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


# ==================== PROJECT SHOWCASE ====================

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=False)
    detailed_description = Column(Text)
    tech_stack = Column(JSON)  # Array of technologies
    github_url = Column(String(500))
    demo_url = Column(String(500))
    video_url = Column(String(500))
    images = Column(JSON)  # Array of image URLs
    category = Column(String(100), index=True)
    tags = Column(JSON)  # Array of tags
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    likes = Column(Integer, default=0)
    views = Column(Integer, default=0)
    github_stars = Column(Integer, default=0)
    github_forks = Column(Integer, default=0)
    is_featured = Column(Boolean, default=False, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), index=True)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    collaborators = relationship("ProjectCollaborator", back_populates="project", cascade="all, delete-orphan")
    comments = relationship("ProjectComment", back_populates="project", cascade="all, delete-orphan")
    likes_rel = relationship("ProjectLike", back_populates="project", cascade="all, delete-orphan")


class ProjectCollaborator(Base):
    __tablename__ = "project_collaborators"
    
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role = Column(String(100))
    joined_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="collaborators")


class ProjectComment(Base):
    __tablename__ = "project_comments"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    content = Column(Text, nullable=False)
    parent_id = Column(String(36), ForeignKey("project_comments.id", ondelete="CASCADE"))  # For nested comments
    created_at = Column(TIMESTAMP, server_default=func.now(), index=True)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="comments")


class ProjectLike(Base):
    __tablename__ = "project_likes"
    
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="likes_rel")


# ==================== MENTORSHIP ====================

class MentorshipStatus(str, enum.Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class SessionStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


class MentorProfile(Base):
    __tablename__ = "mentor_profiles"
    
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    expertise = Column(JSON)  # Array of expertise areas
    availability = Column(JSON)  # Schedule availability
    max_mentees = Column(Integer, default=5)
    current_mentees = Column(Integer, default=0)
    bio = Column(Text)
    years_experience = Column(Integer)
    hourly_rate = Column(Float, default=0.0)  # 0 for free mentorship
    rating = Column(Float, default=0.0)
    total_sessions = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    mentorships = relationship("Mentorship", foreign_keys="Mentorship.mentor_id", back_populates="mentor")


class Mentorship(Base):
    __tablename__ = "mentorships"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    mentee_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    mentor_id = Column(String(36), ForeignKey("mentor_profiles.user_id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(Enum(MentorshipStatus), default=MentorshipStatus.PENDING, index=True)
    message = Column(Text)
    goals = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    mentor = relationship("MentorProfile", foreign_keys=[mentor_id], back_populates="mentorships")
    sessions = relationship("MentorshipSession", back_populates="mentorship", cascade="all, delete-orphan")


class MentorshipSession(Base):
    __tablename__ = "mentorship_sessions"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    mentorship_id = Column(String(36), ForeignKey("mentorships.id", ondelete="CASCADE"), nullable=False, index=True)
    scheduled_at = Column(TIMESTAMP, nullable=False, index=True)
    duration = Column(Integer, default=60)  # in minutes
    meeting_url = Column(String(500))
    notes = Column(Text)
    feedback = Column(Text)
    rating = Column(Integer)  # 1-5
    status = Column(Enum(SessionStatus), default=SessionStatus.SCHEDULED, index=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    mentorship = relationship("Mentorship", back_populates="sessions")


# ==================== EVENTS ====================

class EventType(str, enum.Enum):
    WORKSHOP = "workshop"
    HACKATHON = "hackathon"
    WEBINAR = "webinar"
    MEETUP = "meetup"
    CONFERENCE = "conference"
    SEMINAR = "seminar"


class RSVPStatus(str, enum.Enum):
    GOING = "going"
    MAYBE = "maybe"
    NOT_GOING = "not_going"


class Event(Base):
    __tablename__ = "events"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=False)
    event_type = Column(Enum(EventType), nullable=False, index=True)
    start_time = Column(TIMESTAMP, nullable=False, index=True)
    end_time = Column(TIMESTAMP, nullable=False)
    location = Column(String(200))
    is_virtual = Column(Boolean, default=False)
    meeting_url = Column(String(500))
    banner_url = Column(String(500))
    organizer_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    max_attendees = Column(Integer)
    current_attendees = Column(Integer, default=0)
    tags = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    attendees = relationship("EventAttendee", back_populates="event", cascade="all, delete-orphan")


class EventAttendee(Base):
    __tablename__ = "event_attendees"
    
    event_id = Column(String(36), ForeignKey("events.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    rsvp_status = Column(Enum(RSVPStatus), default=RSVPStatus.GOING)
    attended = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    event = relationship("Event", back_populates="attendees")


# ==================== GAMIFICATION ====================

class BadgeRarity(str, enum.Enum):
    COMMON = "common"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


class Badge(Base):
    __tablename__ = "badges"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    icon_url = Column(String(500))
    criteria = Column(JSON)  # Criteria to earn the badge
    rarity = Column(Enum(BadgeRarity), default=BadgeRarity.COMMON)
    points = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    user_badges = relationship("UserBadge", back_populates="badge")


class UserBadge(Base):
    __tablename__ = "user_badges"
    
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    badge_id = Column(String(36), ForeignKey("badges.id", ondelete="CASCADE"), primary_key=True)
    earned_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    badge = relationship("Badge", back_populates="user_badges")


class Achievement(Base):
    __tablename__ = "achievements"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    icon_url = Column(String(500))
    points = Column(Integer, default=0)
    category = Column(String(50), index=True)
    max_progress = Column(Integer, default=1)  # For progressive achievements
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    user_achievements = relationship("UserAchievement", back_populates="achievement")


class UserAchievement(Base):
    __tablename__ = "user_achievements"
    
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    achievement_id = Column(String(36), ForeignKey("achievements.id", ondelete="CASCADE"), primary_key=True)
    progress = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    completed_at = Column(TIMESTAMP)
    
    # Relationships
    achievement = relationship("Achievement", back_populates="user_achievements")


class Leaderboard(Base):
    __tablename__ = "leaderboards"
    
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    total_points = Column(Integer, default=0, index=True)
    rank = Column(Integer, index=True)
    category = Column(String(50), default="overall")
    weekly_points = Column(Integer, default=0)
    monthly_points = Column(Integer, default=0)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
