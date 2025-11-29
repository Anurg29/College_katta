from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api.deps import get_current_user, get_db
from app.models.mysql.models import User
from app.models.mysql.enhanced_models import (
    Project, ProjectCollaborator, ProjectComment, ProjectLike
)
from app.schemas.enhanced_schemas import (
    ProjectCreate, ProjectUpdate, ProjectResponse,
    ProjectCommentCreate, ProjectCommentResponse
)

router = APIRouter()


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new project showcase."""
    project = Project(
        **project_data.dict(),
        user_id=current_user.id
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.get("/", response_model=List[ProjectResponse])
async def list_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    search: Optional[str] = None,
    tech_stack: Optional[str] = None,
    is_featured: Optional[bool] = None,
    sort_by: str = Query("created_at", regex="^(created_at|likes|views)$"),
    order: str = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    """
    List all projects with filters.
    
    Filters:
    - category: Filter by project category
    - search: Search in title and description
    - tech_stack: Filter by technology
    - is_featured: Show only featured projects
    """
    query = db.query(Project).filter(Project.is_active == True)
    
    if category:
        query = query.filter(Project.category == category)
    if search:
        query = query.filter(
            (Project.title.ilike(f"%{search}%")) | 
            (Project.description.ilike(f"%{search}%"))
        )
    if tech_stack:
        # Search in JSON array
        query = query.filter(Project.tech_stack.contains([tech_stack]))
    if is_featured is not None:
        query = query.filter(Project.is_featured == is_featured)
    
    # Sorting
    sort_column = getattr(Project, sort_by)
    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())
    
    projects = query.offset(skip).limit(limit).all()
    return projects


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific project by ID."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Increment views
    project.views += 1
    db.commit()
    
    return project


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a project (only by owner or collaborators)."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Check if user is owner or collaborator
    is_collaborator = db.query(ProjectCollaborator).filter(
        ProjectCollaborator.project_id == project_id,
        ProjectCollaborator.user_id == current_user.id
    ).first()
    
    if project.user_id != current_user.id and not is_collaborator:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this project"
        )
    
    for field, value in project_data.dict(exclude_unset=True).items():
        setattr(project, field, value)
    
    db.commit()
    db.refresh(project)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a project (only by owner)."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    if project.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this project"
        )
    
    db.delete(project)
    db.commit()
    return None


@router.post("/{project_id}/like", status_code=status.HTTP_200_OK)
async def like_project(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Like or unlike a project."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Check if already liked
    existing_like = db.query(ProjectLike).filter(
        ProjectLike.project_id == project_id,
        ProjectLike.user_id == current_user.id
    ).first()
    
    if existing_like:
        # Unlike
        db.delete(existing_like)
        project.likes -= 1
        message = "Project unliked"
    else:
        # Like
        new_like = ProjectLike(
            project_id=project_id,
            user_id=current_user.id
        )
        db.add(new_like)
        project.likes += 1
        message = "Project liked"
    
    db.commit()
    return {"message": message, "likes": project.likes}


@router.post("/{project_id}/comments", response_model=ProjectCommentResponse, status_code=status.HTTP_201_CREATED)
async def add_comment(
    project_id: str,
    comment_data: ProjectCommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a comment to a project."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    comment = ProjectComment(
        project_id=project_id,
        user_id=current_user.id,
        **comment_data.dict()
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@router.get("/{project_id}/comments", response_model=List[ProjectCommentResponse])
async def get_comments(
    project_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all comments for a project."""
    comments = db.query(ProjectComment).filter(
        ProjectComment.project_id == project_id
    ).order_by(ProjectComment.created_at.desc()).offset(skip).limit(limit).all()
    
    return comments


@router.post("/{project_id}/collaborators/{user_id}", status_code=status.HTTP_201_CREATED)
async def add_collaborator(
    project_id: str,
    user_id: str,
    role: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a collaborator to a project (only by owner)."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    if project.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only project owner can add collaborators"
        )
    
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if already a collaborator
    existing = db.query(ProjectCollaborator).filter(
        ProjectCollaborator.project_id == project_id,
        ProjectCollaborator.user_id == user_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a collaborator"
        )
    
    collaborator = ProjectCollaborator(
        project_id=project_id,
        user_id=user_id,
        role=role
    )
    db.add(collaborator)
    db.commit()
    
    return {"message": "Collaborator added successfully"}


@router.delete("/{project_id}/collaborators/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_collaborator(
    project_id: str,
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove a collaborator from a project (only by owner)."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    if project.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only project owner can remove collaborators"
        )
    
    collaborator = db.query(ProjectCollaborator).filter(
        ProjectCollaborator.project_id == project_id,
        ProjectCollaborator.user_id == user_id
    ).first()
    
    if not collaborator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Collaborator not found"
        )
    
    db.delete(collaborator)
    db.commit()
    return None


@router.get("/user/{user_id}", response_model=List[ProjectResponse])
async def get_user_projects(
    user_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all projects by a specific user."""
    projects = db.query(Project).filter(
        Project.user_id == user_id,
        Project.is_active == True
    ).order_by(Project.created_at.desc()).offset(skip).limit(limit).all()
    
    return projects
