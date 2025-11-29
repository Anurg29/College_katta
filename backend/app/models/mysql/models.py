from sqlalchemy import Column, String, Boolean, Integer, Text, Enum, TIMESTAMP, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid
import enum


def generate_uuid():
    return str(uuid.uuid4())


class UserRole(str, enum.Enum):
    STUDENT = "student"
    MENTOR = "mentor"
    RECRUITER = "recruiter"
    ADMIN = "admin"


class ProficiencyLevel(str, enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))
    role = Column(Enum(UserRole), default=UserRole.STUDENT)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    skills = relationship("UserSkill", back_populates="user", cascade="all, delete-orphan")
    interests = relationship("UserInterest", back_populates="user", cascade="all, delete-orphan")
    communities = relationship("CommunityMember", back_populates="user", cascade="all, delete-orphan")
    teams = relationship("TeamMember", back_populates="user", cascade="all, delete-orphan")
    interactions = relationship("UserInteraction", back_populates="user", cascade="all, delete-orphan")


class Profile(Base):
    __tablename__ = "profiles"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    bio = Column(Text)
    university = Column(String(200))
    graduation_year = Column(Integer)
    github_url = Column(String(255))
    linkedin_url = Column(String(255))
    portfolio_url = Column(String(255))
    avatar_url = Column(String(255))
    location = Column(String(100))
    reputation_score = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="profile")


class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(50), unique=True, nullable=False, index=True)
    category = Column(String(50), index=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    user_skills = relationship("UserSkill", back_populates="skill")


class UserSkill(Base):
    __tablename__ = "user_skills"
    
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    skill_id = Column(String(36), ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True)
    proficiency_level = Column(Enum(ProficiencyLevel), default=ProficiencyLevel.INTERMEDIATE)
    
    # Relationships
    user = relationship("User", back_populates="skills")
    skill = relationship("Skill", back_populates="user_skills")


class Interest(Base):
    __tablename__ = "interests"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(50), unique=True, nullable=False)
    category = Column(String(50), index=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    user_interests = relationship("UserInterest", back_populates="interest")


class UserInterest(Base):
    __tablename__ = "user_interests"
    
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    interest_id = Column(String(36), ForeignKey("interests.id", ondelete="CASCADE"), primary_key=True)
    
    # Relationships
    user = relationship("User", back_populates="interests")
    interest = relationship("Interest", back_populates="user_interests")


class Community(Base):
    __tablename__ = "communities"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    category = Column(String(50), index=True)
    icon_url = Column(String(255))
    banner_url = Column(String(255))
    created_by = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"))
    member_count = Column(Integer, default=0)
    is_private = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    members = relationship("CommunityMember", back_populates="community", cascade="all, delete-orphan")


class CommunityMember(Base):
    __tablename__ = "community_members"
    
    community_id = Column(String(36), ForeignKey("communities.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role = Column(Enum("admin", "moderator", "member", name="community_role"), default="member")
    joined_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    community = relationship("Community", back_populates="members")
    user = relationship("User", back_populates="communities")


class Hackathon(Base):
    __tablename__ = "hackathons"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    organizer = Column(String(200))
    start_date = Column(TIMESTAMP, nullable=False)
    end_date = Column(TIMESTAMP, nullable=False)
    registration_deadline = Column(TIMESTAMP)
    mode = Column(Enum("online", "offline", "hybrid", name="hackathon_mode"), default="online")
    location = Column(String(200))
    prize_pool = Column(String(100))
    website_url = Column(String(255))
    banner_url = Column(String(255))
    max_team_size = Column(Integer, default=4)
    min_team_size = Column(Integer, default=1)
    status = Column(Enum("upcoming", "ongoing", "completed", name="hackathon_status"), default="upcoming", index=True)
    created_by = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    teams = relationship("Team", back_populates="hackathon", cascade="all, delete-orphan")


class Team(Base):
    __tablename__ = "teams"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    hackathon_id = Column(String(36), ForeignKey("hackathons.id", ondelete="CASCADE"), index=True)
    leader_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"))
    max_members = Column(Integer, default=4)
    current_members = Column(Integer, default=1)
    is_open = Column(Boolean, default=True)
    status = Column(Enum("forming", "complete", "disbanded", name="team_status"), default="forming", index=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    hackathon = relationship("Hackathon", back_populates="teams")
    members = relationship("TeamMember", back_populates="team", cascade="all, delete-orphan")
    requests = relationship("TeamRequest", back_populates="team", cascade="all, delete-orphan")


class TeamMember(Base):
    __tablename__ = "team_members"
    
    team_id = Column(String(36), ForeignKey("teams.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role = Column(String(50))
    joined_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    team = relationship("Team", back_populates="members")
    user = relationship("User", back_populates="teams")


class TeamRequest(Base):
    __tablename__ = "team_requests"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    team_id = Column(String(36), ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    message = Column(Text)
    status = Column(Enum("pending", "accepted", "rejected", name="request_status"), default="pending")
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    team = relationship("Team", back_populates="requests")


class UserInteraction(Base):
    __tablename__ = "user_interactions"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    target_type = Column(Enum("post", "comment", "user", "hackathon", "community", name="target_type"), nullable=False)
    target_id = Column(String(36), nullable=False, index=True)
    interaction_type = Column(Enum("view", "like", "bookmark", "share", "join", "comment", name="interaction_type"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), index=True)
    
    # Relationships
    user = relationship("User", back_populates="interactions")
