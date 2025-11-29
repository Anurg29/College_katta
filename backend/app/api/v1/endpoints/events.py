from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.api.deps import get_current_user, get_db
from app.models.mysql.models import User
from app.models.mysql.enhanced_models import (
    Event, EventAttendee, EventType, RSVPStatus
)
from app.schemas.enhanced_schemas import (
    EventCreate, EventUpdate, EventResponse, EventRSVPCreate
)

router = APIRouter()


@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
    event_data: EventCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new event."""
    event = Event(
        **event_data.dict(),
        organizer_id=current_user.id
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@router.get("/", response_model=List[EventResponse])
async def list_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    event_type: Optional[EventType] = None,
    is_virtual: Optional[bool] = None,
    search: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    is_active: bool = True,
    sort_by: str = Query("start_time", regex="^(start_time|created_at|current_attendees)$"),
    order: str = Query("asc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    """
    List all events with filters.
    
    Filters:
    - event_type: Filter by event type
    - is_virtual: Filter virtual/in-person events
    - search: Search in title and description
    - start_date, end_date: Filter by date range
    """
    query = db.query(Event).filter(Event.is_active == is_active)
    
    if event_type:
        query = query.filter(Event.event_type == event_type)
    if is_virtual is not None:
        query = query.filter(Event.is_virtual == is_virtual)
    if search:
        query = query.filter(
            (Event.title.ilike(f"%{search}%")) | 
            (Event.description.ilike(f"%{search}%"))
        )
    if start_date:
        query = query.filter(Event.start_time >= start_date)
    if end_date:
        query = query.filter(Event.end_time <= end_date)
    
    # Sorting
    sort_column = getattr(Event, sort_by)
    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())
    
    events = query.offset(skip).limit(limit).all()
    return events


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific event by ID."""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return event


@router.put("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: str,
    event_data: EventUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an event (only by organizer)."""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    if event.organizer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this event"
        )
    
    for field, value in event_data.dict(exclude_unset=True).items():
        setattr(event, field, value)
    
    db.commit()
    db.refresh(event)
    return event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete an event (only by organizer)."""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    if event.organizer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this event"
        )
    
    db.delete(event)
    db.commit()
    return None


@router.post("/{event_id}/rsvp", status_code=status.HTTP_200_OK)
async def rsvp_event(
    event_id: str,
    rsvp_data: EventRSVPCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """RSVP to an event."""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Check if event is full
    if event.max_attendees and event.current_attendees >= event.max_attendees:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Event is full"
        )
    
    # Check existing RSVP
    existing_rsvp = db.query(EventAttendee).filter(
        EventAttendee.event_id == event_id,
        EventAttendee.user_id == current_user.id
    ).first()
    
    if existing_rsvp:
        # Update RSVP
        old_status = existing_rsvp.rsvp_status
        existing_rsvp.rsvp_status = rsvp_data.rsvp_status
        
        # Update attendee count
        if old_status == RSVPStatus.GOING and rsvp_data.rsvp_status != RSVPStatus.GOING:
            event.current_attendees -= 1
        elif old_status != RSVPStatus.GOING and rsvp_data.rsvp_status == RSVPStatus.GOING:
            event.current_attendees += 1
    else:
        # Create new RSVP
        new_rsvp = EventAttendee(
            event_id=event_id,
            user_id=current_user.id,
            rsvp_status=rsvp_data.rsvp_status
        )
        db.add(new_rsvp)
        
        if rsvp_data.rsvp_status == RSVPStatus.GOING:
            event.current_attendees += 1
    
    db.commit()
    return {
        "message": "RSVP updated",
        "rsvp_status": rsvp_data.rsvp_status,
        "current_attendees": event.current_attendees
    }


@router.get("/{event_id}/attendees")
async def get_event_attendees(
    event_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    rsvp_status: Optional[RSVPStatus] = None,
    db: Session = Depends(get_db)
):
    """Get all attendees for an event."""
    query = db.query(EventAttendee).filter(EventAttendee.event_id == event_id)
    
    if rsvp_status:
        query = query.filter(EventAttendee.rsvp_status == rsvp_status)
    
    attendees = query.offset(skip).limit(limit).all()
    return attendees


@router.get("/my-events/attending", response_model=List[EventResponse])
async def get_my_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all events I'm attending."""
    # Get event IDs where user is attending
    event_ids = db.query(EventAttendee.event_id).filter(
        EventAttendee.user_id == current_user.id,
        EventAttendee.rsvp_status == RSVPStatus.GOING
    ).all()
    
    event_ids = [e[0] for e in event_ids]
    
    events = db.query(Event).filter(
        Event.id.in_(event_ids),
        Event.is_active == True
    ).order_by(Event.start_time.asc()).offset(skip).limit(limit).all()
    
    return events


@router.get("/my-events/organizing", response_model=List[EventResponse])
async def get_my_organized_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all events I'm organizing."""
    events = db.query(Event).filter(
        Event.organizer_id == current_user.id
    ).order_by(Event.start_time.desc()).offset(skip).limit(limit).all()
    
    return events
