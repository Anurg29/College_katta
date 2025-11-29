from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api.deps import get_current_user, get_db
from app.models.mysql.models import User
from app.models.mysql.enhanced_models import (
    Resource, ResourceVote, ResourceCategory
)
from app.schemas.enhanced_schemas import (
    ResourceCreate, ResourceUpdate, ResourceResponse, ResourceVoteCreate
)
from datetime import datetime

router = APIRouter()


@router.post("/", response_model=ResourceResponse, status_code=status.HTTP_201_CREATED)
async def create_resource(
    resource_data: ResourceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new resource.
    Upload files and share study materials with the community.
    """
    resource = Resource(
        **resource_data.dict(),
        user_id=current_user.id
    )
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return resource


@router.get("/", response_model=List[ResourceResponse])
async def list_resources(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[ResourceCategory] = None,
    subject: Optional[str] = None,
    semester: Optional[int] = None,
    university: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: str = Query("created_at", regex="^(created_at|upvotes|downloads|views)$"),
    order: str = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    """
    List all resources with optional filters.
    
    Filters:
    - category: Filter by resource category
    - subject: Filter by subject
    - semester: Filter by semester
    - university: Filter by university
    - search: Search in title and description
    - sort_by: Sort by field (created_at, upvotes, downloads, views)
    - order: Sort order (asc, desc)
    """
    query = db.query(Resource).filter(Resource.is_active == True)
    
    if category:
        query = query.filter(Resource.category == category)
    if subject:
        query = query.filter(Resource.subject.ilike(f"%{subject}%"))
    if semester:
        query = query.filter(Resource.semester == semester)
    if university:
        query = query.filter(Resource.university.ilike(f"%{university}%"))
    if search:
        query = query.filter(
            (Resource.title.ilike(f"%{search}%")) | 
            (Resource.description.ilike(f"%{search}%"))
        )
    
    # Sorting
    sort_column = getattr(Resource, sort_by)
    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())
    
    resources = query.offset(skip).limit(limit).all()
    return resources


@router.get("/{resource_id}", response_model=ResourceResponse)
async def get_resource(
    resource_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific resource by ID."""
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    
    # Increment views
    resource.views += 1
    db.commit()
    
    return resource


@router.put("/{resource_id}", response_model=ResourceResponse)
async def update_resource(
    resource_id: str,
    resource_data: ResourceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a resource (only by owner)."""
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    
    if resource.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this resource"
        )
    
    for field, value in resource_data.dict(exclude_unset=True).items():
        setattr(resource, field, value)
    
    db.commit()
    db.refresh(resource)
    return resource


@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resource(
    resource_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a resource (only by owner)."""
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    
    if resource.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this resource"
        )
    
    db.delete(resource)
    db.commit()
    return None


@router.post("/{resource_id}/vote", status_code=status.HTTP_200_OK)
async def vote_resource(
    resource_id: str,
    vote_data: ResourceVoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upvote or downvote a resource."""
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    
    # Check if user already voted
    existing_vote = db.query(ResourceVote).filter(
        ResourceVote.resource_id == resource_id,
        ResourceVote.user_id == current_user.id
    ).first()
    
    if existing_vote:
        # Update vote if different
        if existing_vote.vote_type != vote_data.vote_type:
            # Remove old vote count
            if existing_vote.vote_type == "upvote":
                resource.upvotes -= 1
            else:
                resource.downvotes -= 1
            
            # Add new vote count
            if vote_data.vote_type == "upvote":
                resource.upvotes += 1
            else:
                resource.downvotes += 1
            
            existing_vote.vote_type = vote_data.vote_type
        else:
            # Remove vote if same
            if vote_data.vote_type == "upvote":
                resource.upvotes -= 1
            else:
                resource.downvotes -= 1
            db.delete(existing_vote)
    else:
        # Create new vote
        new_vote = ResourceVote(
            resource_id=resource_id,
            user_id=current_user.id,
            vote_type=vote_data.vote_type
        )
        db.add(new_vote)
        
        if vote_data.vote_type == "upvote":
            resource.upvotes += 1
        else:
            resource.downvotes += 1
    
    db.commit()
    return {
        "message": "Vote recorded",
        "upvotes": resource.upvotes,
        "downvotes": resource.downvotes
    }


@router.post("/{resource_id}/download", status_code=status.HTTP_200_OK)
async def download_resource(
    resource_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Track resource download."""
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    
    # Increment download count
    resource.downloads += 1
    db.commit()
    
    return {
        "message": "Download tracked",
        "download_url": resource.file_url,
        "downloads": resource.downloads
    }


@router.get("/user/{user_id}", response_model=List[ResourceResponse])
async def get_user_resources(
    user_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all resources uploaded by a specific user."""
    resources = db.query(Resource).filter(
        Resource.user_id == user_id,
        Resource.is_active == True
    ).order_by(Resource.created_at.desc()).offset(skip).limit(limit).all()
    
    return resources
