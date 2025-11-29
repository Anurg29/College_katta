from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api.deps import get_current_user, get_db
from app.models.mysql.models import User
from app.models.mysql.enhanced_models import (
    JobPosting, JobApplication, Resume, JobType, JobLocation, ApplicationStatus
)
from app.schemas.enhanced_schemas import (
    JobPostingCreate, JobPostingUpdate, JobPostingResponse,
    JobApplicationCreate, JobApplicationResponse,
    ResumeCreate, ResumeResponse
)
from datetime import datetime

router = APIRouter()


# ==================== JOB POSTINGS ====================

@router.post("/", response_model=JobPostingResponse, status_code=status.HTTP_201_CREATED)
async def create_job_posting(
    job_data: JobPostingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new job posting.
    Available for recruiters and verified users.
    """
    job = JobPosting(
        **job_data.dict(),
        posted_by=current_user.id
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.get("/", response_model=List[JobPostingResponse])
async def list_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    job_type: Optional[JobType] = None,
    location_type: Optional[JobLocation] = None,
    location: Optional[str] = None,
    company: Optional[str] = None,
    search: Optional[str] = None,
    min_salary: Optional[int] = None,
    max_salary: Optional[int] = None,
    experience_max: Optional[int] = None,
    is_active: bool = True,
    sort_by: str = Query("created_at", regex="^(created_at|views|applications_count)$"),
    order: str = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    """
    List all job postings with filters.
    
    Filters:
    - job_type: Filter by job type (internship, full_time, etc.)
    - location_type: Filter by location type (remote, onsite, hybrid)
    - location: Filter by location
    - company: Filter by company name
    - search: Search in title and description
    - min_salary, max_salary: Salary range filter
    - experience_max: Maximum years of experience required
    """
    query = db.query(JobPosting).filter(JobPosting.is_active == is_active)
    
    # Apply filters
    if job_type:
        query = query.filter(JobPosting.job_type == job_type)
    if location_type:
        query = query.filter(JobPosting.location_type == location_type)
    if location:
        query = query.filter(JobPosting.location.ilike(f"%{location}%"))
    if company:
        query = query.filter(JobPosting.company.ilike(f"%{company}%"))
    if search:
        query = query.filter(
            (JobPosting.title.ilike(f"%{search}%")) | 
            (JobPosting.description.ilike(f"%{search}%"))
        )
    if min_salary is not None:
        query = query.filter(JobPosting.salary_min >= min_salary)
    if max_salary is not None:
        query = query.filter(JobPosting.salary_max <= max_salary)
    if experience_max is not None:
        query = query.filter(JobPosting.experience_max <= experience_max)
    
    # Filter out expired jobs
    query = query.filter(
        (JobPosting.expires_at == None) | (JobPosting.expires_at > datetime.utcnow())
    )
    
    # Sorting
    sort_column = getattr(JobPosting, sort_by)
    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())
    
    jobs = query.offset(skip).limit(limit).all()
    return jobs


@router.get("/{job_id}", response_model=JobPostingResponse)
async def get_job(
    job_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific job posting by ID."""
    job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job posting not found"
        )
    
    # Increment views
    job.views += 1
    db.commit()
    
    return job


@router.put("/{job_id}", response_model=JobPostingResponse)
async def update_job(
    job_id: str,
    job_data: JobPostingUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a job posting (only by poster)."""
    job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job posting not found"
        )
    
    if job.posted_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this job posting"
        )
    
    for field, value in job_data.dict(exclude_unset=True).items():
        setattr(job, field, value)
    
    db.commit()
    db.refresh(job)
    return job


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    job_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a job posting (only by poster)."""
    job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job posting not found"
        )
    
    if job.posted_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this job posting"
        )
    
    db.delete(job)
    db.commit()
    return None


# ==================== JOB APPLICATIONS ====================

@router.post("/{job_id}/apply", response_model=JobApplicationResponse, status_code=status.HTTP_201_CREATED)
async def apply_for_job(
    job_id: str,
    application_data: JobApplicationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Apply for a job posting."""
    # Check if job exists and is active
    job = db.query(JobPosting).filter(
        JobPosting.id == job_id,
        JobPosting.is_active == True
    ).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job posting not found or inactive"
        )
    
    # Check if already applied
    existing_application = db.query(JobApplication).filter(
        JobApplication.job_id == job_id,
        JobApplication.user_id == current_user.id
    ).first()
    
    if existing_application:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already applied for this job"
        )
    
    # Create application
    application = JobApplication(
        job_id=job_id,
        user_id=current_user.id,
        **application_data.dict()
    )
    db.add(application)
    
    # Increment applications count
    job.applications_count += 1
    
    db.commit()
    db.refresh(application)
    return application


@router.get("/applications/me", response_model=List[JobApplicationResponse])
async def get_my_applications(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status_filter: Optional[ApplicationStatus] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all my job applications."""
    query = db.query(JobApplication).filter(JobApplication.user_id == current_user.id)
    
    if status_filter:
        query = query.filter(JobApplication.status == status_filter)
    
    applications = query.order_by(JobApplication.applied_at.desc()).offset(skip).limit(limit).all()
    return applications


@router.get("/{job_id}/applications", response_model=List[JobApplicationResponse])
async def get_job_applications(
    job_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status_filter: Optional[ApplicationStatus] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all applications for a job (only by job poster)."""
    job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job posting not found"
        )
    
    if job.posted_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view applications"
        )
    
    query = db.query(JobApplication).filter(JobApplication.job_id == job_id)
    
    if status_filter:
        query = query.filter(JobApplication.status == status_filter)
    
    applications = query.order_by(JobApplication.applied_at.desc()).offset(skip).limit(limit).all()
    return applications


@router.put("/applications/{application_id}/status", response_model=JobApplicationResponse)
async def update_application_status(
    application_id: str,
    new_status: ApplicationStatus,
    notes: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update application status (only by job poster)."""
    application = db.query(JobApplication).filter(JobApplication.id == application_id).first()
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    # Check if user is the job poster
    job = db.query(JobPosting).filter(JobPosting.id == application.job_id).first()
    if job.posted_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this application"
        )
    
    application.status = new_status
    if notes:
        application.notes = notes
    
    db.commit()
    db.refresh(application)
    return application


# ==================== RESUMES ====================

@router.post("/resumes", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    resume_data: ResumeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a new resume."""
    # If setting as primary, unset other primary resumes
    if resume_data.is_primary:
        db.query(Resume).filter(
            Resume.user_id == current_user.id,
            Resume.is_primary == True
        ).update({"is_primary": False})
    
    resume = Resume(
        **resume_data.dict(),
        user_id=current_user.id
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return resume


@router.get("/resumes/me", response_model=List[ResumeResponse])
async def get_my_resumes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all my resumes."""
    resumes = db.query(Resume).filter(
        Resume.user_id == current_user.id
    ).order_by(Resume.is_primary.desc(), Resume.created_at.desc()).all()
    return resumes


@router.delete("/resumes/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    resume_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a resume."""
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    db.delete(resume)
    db.commit()
    return None
