from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api.deps import get_current_user, get_db
from app.models.mysql.models import User
from app.models.mysql.enhanced_models import (
    MentorProfile, Mentorship, MentorshipSession, MentorshipStatus, SessionStatus
)
from app.schemas.enhanced_schemas import (
    MentorProfileCreate, MentorProfileUpdate, MentorProfileResponse,
    MentorshipRequestCreate, MentorshipResponse,
    SessionCreate, SessionUpdate, SessionResponse
)

router = APIRouter()


# ==================== MENTOR PROFILES ====================

@router.post("/become-mentor", response_model=MentorProfileResponse, status_code=status.HTTP_201_CREATED)
async def become_mentor(
    mentor_data: MentorProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Register as a mentor."""
    # Check if already a mentor
    existing = db.query(MentorProfile).filter(
        MentorProfile.user_id == current_user.id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already registered as a mentor"
        )
    
    mentor_profile = MentorProfile(
        user_id=current_user.id,
        **mentor_data.dict()
    )
    db.add(mentor_profile)
    db.commit()
    db.refresh(mentor_profile)
    return mentor_profile


@router.get("/mentors", response_model=List[MentorProfileResponse])
async def list_mentors(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    expertise: Optional[str] = None,
    min_rating: Optional[float] = None,
    max_rate: Optional[float] = None,
    is_active: bool = True,
    sort_by: str = Query("rating", regex="^(rating|total_sessions|created_at)$"),
    order: str = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    """
    List all mentors with filters.
    
    Filters:
    - expertise: Filter by expertise area
    - min_rating: Minimum rating
    - max_rate: Maximum hourly rate
    """
    query = db.query(MentorProfile).filter(MentorProfile.is_active == is_active)
    
    # Filter by available mentors (not at max capacity)
    query = query.filter(MentorProfile.current_mentees < MentorProfile.max_mentees)
    
    if expertise:
        # Search in JSON array
        query = query.filter(MentorProfile.expertise.contains([expertise]))
    if min_rating is not None:
        query = query.filter(MentorProfile.rating >= min_rating)
    if max_rate is not None:
        query = query.filter(MentorProfile.hourly_rate <= max_rate)
    
    # Sorting
    sort_column = getattr(MentorProfile, sort_by)
    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())
    
    mentors = query.offset(skip).limit(limit).all()
    return mentors


@router.get("/mentors/{user_id}", response_model=MentorProfileResponse)
async def get_mentor_profile(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific mentor profile."""
    mentor = db.query(MentorProfile).filter(MentorProfile.user_id == user_id).first()
    if not mentor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mentor profile not found"
        )
    return mentor


@router.put("/my-mentor-profile", response_model=MentorProfileResponse)
async def update_mentor_profile(
    mentor_data: MentorProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update my mentor profile."""
    mentor = db.query(MentorProfile).filter(
        MentorProfile.user_id == current_user.id
    ).first()
    
    if not mentor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mentor profile not found. Please register as a mentor first."
        )
    
    for field, value in mentor_data.dict(exclude_unset=True).items():
        setattr(mentor, field, value)
    
    db.commit()
    db.refresh(mentor)
    return mentor


# ==================== MENTORSHIPS ====================

@router.post("/request", response_model=MentorshipResponse, status_code=status.HTTP_201_CREATED)
async def request_mentorship(
    request_data: MentorshipRequestCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Request mentorship from a mentor."""
    # Check if mentor exists and is active
    mentor = db.query(MentorProfile).filter(
        MentorProfile.user_id == request_data.mentor_id,
        MentorProfile.is_active == True
    ).first()
    
    if not mentor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mentor not found or inactive"
        )
    
    # Check if mentor has capacity
    if mentor.current_mentees >= mentor.max_mentees:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mentor has reached maximum mentee capacity"
        )
    
    # Check if already requested
    existing = db.query(Mentorship).filter(
        Mentorship.mentee_id == current_user.id,
        Mentorship.mentor_id == request_data.mentor_id,
        Mentorship.status.in_([MentorshipStatus.PENDING, MentorshipStatus.ACTIVE])
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have a pending or active mentorship with this mentor"
        )
    
    mentorship = Mentorship(
        mentee_id=current_user.id,
        mentor_id=request_data.mentor_id,
        message=request_data.message,
        goals=request_data.goals
    )
    db.add(mentorship)
    db.commit()
    db.refresh(mentorship)
    return mentorship


@router.get("/my-mentorships", response_model=List[MentorshipResponse])
async def get_my_mentorships(
    status_filter: Optional[MentorshipStatus] = None,
    as_mentor: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all my mentorships (as mentee or mentor)."""
    if as_mentor:
        query = db.query(Mentorship).filter(Mentorship.mentor_id == current_user.id)
    else:
        query = db.query(Mentorship).filter(Mentorship.mentee_id == current_user.id)
    
    if status_filter:
        query = query.filter(Mentorship.status == status_filter)
    
    mentorships = query.order_by(Mentorship.created_at.desc()).all()
    return mentorships


@router.put("/mentorships/{mentorship_id}/status", response_model=MentorshipResponse)
async def update_mentorship_status(
    mentorship_id: str,
    new_status: MentorshipStatus,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update mentorship status (accept/reject by mentor, cancel by either party)."""
    mentorship = db.query(Mentorship).filter(Mentorship.id == mentorship_id).first()
    if not mentorship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mentorship not found"
        )
    
    # Check authorization
    is_mentor = mentorship.mentor_id == current_user.id
    is_mentee = mentorship.mentee_id == current_user.id
    
    if not (is_mentor or is_mentee):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this mentorship"
        )
    
    # Only mentor can accept/reject pending requests
    if new_status in [MentorshipStatus.ACTIVE] and mentorship.status == MentorshipStatus.PENDING:
        if not is_mentor:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only mentor can accept mentorship requests"
            )
        
        # Update mentor's mentee count
        mentor = db.query(MentorProfile).filter(
            MentorProfile.user_id == mentorship.mentor_id
        ).first()
        mentor.current_mentees += 1
    
    # Handle completion or cancellation
    if new_status in [MentorshipStatus.COMPLETED, MentorshipStatus.CANCELLED]:
        if mentorship.status == MentorshipStatus.ACTIVE:
            # Decrease mentor's mentee count
            mentor = db.query(MentorProfile).filter(
                MentorProfile.user_id == mentorship.mentor_id
            ).first()
            mentor.current_mentees -= 1
    
    mentorship.status = new_status
    db.commit()
    db.refresh(mentorship)
    return mentorship


# ==================== SESSIONS ====================

@router.post("/sessions", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def schedule_session(
    session_data: SessionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Schedule a mentorship session."""
    # Check if mentorship exists and is active
    mentorship = db.query(Mentorship).filter(
        Mentorship.id == session_data.mentorship_id,
        Mentorship.status == MentorshipStatus.ACTIVE
    ).first()
    
    if not mentorship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active mentorship not found"
        )
    
    # Check if user is part of the mentorship
    if current_user.id not in [mentorship.mentee_id, mentorship.mentor_id]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to schedule sessions for this mentorship"
        )
    
    session = MentorshipSession(
        **session_data.dict()
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@router.get("/sessions", response_model=List[SessionResponse])
async def get_my_sessions(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status_filter: Optional[SessionStatus] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all my mentorship sessions."""
    # Get all mentorships where user is involved
    mentorship_ids = db.query(Mentorship.id).filter(
        (Mentorship.mentee_id == current_user.id) | 
        (Mentorship.mentor_id == current_user.id)
    ).all()
    
    mentorship_ids = [m[0] for m in mentorship_ids]
    
    query = db.query(MentorshipSession).filter(
        MentorshipSession.mentorship_id.in_(mentorship_ids)
    )
    
    if status_filter:
        query = query.filter(MentorshipSession.status == status_filter)
    
    sessions = query.order_by(MentorshipSession.scheduled_at.desc()).offset(skip).limit(limit).all()
    return sessions


@router.put("/sessions/{session_id}", response_model=SessionResponse)
async def update_session(
    session_id: str,
    session_data: SessionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a mentorship session."""
    session = db.query(MentorshipSession).filter(
        MentorshipSession.id == session_id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    # Check if user is part of the mentorship
    mentorship = db.query(Mentorship).filter(
        Mentorship.id == session.mentorship_id
    ).first()
    
    if current_user.id not in [mentorship.mentee_id, mentorship.mentor_id]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this session"
        )
    
    for field, value in session_data.dict(exclude_unset=True).items():
        setattr(session, field, value)
    
    # Update mentor stats if session is completed with rating
    if session_data.status == SessionStatus.COMPLETED and session_data.rating:
        mentor = db.query(MentorProfile).filter(
            MentorProfile.user_id == mentorship.mentor_id
        ).first()
        
        # Update total sessions
        mentor.total_sessions += 1
        
        # Update rating (simple average for now)
        if mentor.rating == 0:
            mentor.rating = session_data.rating
        else:
            mentor.rating = (mentor.rating * (mentor.total_sessions - 1) + session_data.rating) / mentor.total_sessions
    
    db.commit()
    db.refresh(session)
    return session


@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel a mentorship session."""
    session = db.query(MentorshipSession).filter(
        MentorshipSession.id == session_id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    # Check if user is part of the mentorship
    mentorship = db.query(Mentorship).filter(
        Mentorship.id == session.mentorship_id
    ).first()
    
    if current_user.id not in [mentorship.mentee_id, mentorship.mentor_id]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to cancel this session"
        )
    
    session.status = SessionStatus.CANCELLED
    db.commit()
    return None
