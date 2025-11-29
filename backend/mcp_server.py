from mcp.server.fastmcp import FastMCP
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# Load .env explicitly
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

from app.core.database import SessionLocal
from app.models.mysql.models import User, Hackathon, Community
from app.models.mysql.enhanced_models import Project, Event
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional

# Initialize FastMCP server
mcp = FastMCP("College Katta MCP Server")

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@mcp.tool()
def list_users() -> str:
    """List all users in the database."""
    db = SessionLocal()
    try:
        users = db.query(User).limit(10).all()
        if not users:
            return "No users found."
        return "\n".join([f"ID: {u.id}, Username: {u.username}, Email: {u.email}, Role: {u.role}" for u in users])
    finally:
        db.close()

@mcp.tool()
def search_students(query: str) -> str:
    """Search for students by username or full name."""
    db = SessionLocal()
    try:
        users = db.query(User).filter(
            User.role == "student",
            or_(
                User.username.ilike(f"%{query}%"),
                User.full_name.ilike(f"%{query}%")
            )
        ).limit(10).all()
        
        if not users:
            return f"No students found matching '{query}'."
            
        return "\n".join([f"ID: {u.id}, Name: {u.full_name}, Username: {u.username}, Email: {u.email}" for u in users])
    finally:
        db.close()

@mcp.tool()
def create_project(title: str, description: str, user_id: str, category: str = "General") -> str:
    """Create a new project showcase post."""
    db = SessionLocal()
    try:
        # Verify user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return f"Error: User with ID {user_id} not found."
            
        project = Project(
            title=title,
            description=description,
            user_id=user_id,
            category=category
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        return f"Project created successfully! ID: {project.id}, Title: {project.title}"
    except Exception as e:
        db.rollback()
        return f"Error creating project: {str(e)}"
    finally:
        db.close()

@mcp.tool()
def create_hackathon(title: str, description: str, start_date: str, end_date: str, organizer_name: str, created_by_user_id: str, mode: str = "online") -> str:
    """
    Create a new hackathon.
    Dates should be in ISO format (YYYY-MM-DD HH:MM:SS).
    Mode can be 'online', 'offline', or 'hybrid'.
    """
    db = SessionLocal()
    try:
        # Verify user exists
        user = db.query(User).filter(User.id == created_by_user_id).first()
        if not user:
            return f"Error: User with ID {created_by_user_id} not found."

        try:
            start_dt = datetime.fromisoformat(start_date)
            end_dt = datetime.fromisoformat(end_date)
        except ValueError:
            return "Error: Invalid date format. Please use ISO format (YYYY-MM-DD HH:MM:SS)."

        hackathon = Hackathon(
            title=title,
            description=description,
            start_date=start_dt,
            end_date=end_dt,
            organizer=organizer_name,
            created_by=created_by_user_id,
            mode=mode
        )
        db.add(hackathon)
        db.commit()
        db.refresh(hackathon)
        return f"Hackathon created successfully! ID: {hackathon.id}, Title: {hackathon.title}"
    except Exception as e:
        db.rollback()
        return f"Error creating hackathon: {str(e)}"
    finally:
        db.close()

@mcp.tool()
def create_event(title: str, description: str, start_time: str, end_time: str, organizer_user_id: str, event_type: str = "workshop") -> str:
    """
    Create a new event.
    Dates should be in ISO format (YYYY-MM-DD HH:MM:SS).
    Event type can be 'workshop', 'webinar', 'meetup', etc.
    """
    db = SessionLocal()
    try:
        # Verify user exists
        user = db.query(User).filter(User.id == organizer_user_id).first()
        if not user:
            return f"Error: User with ID {organizer_user_id} not found."

        try:
            start_dt = datetime.fromisoformat(start_time)
            end_dt = datetime.fromisoformat(end_time)
        except ValueError:
            return "Error: Invalid date format. Please use ISO format (YYYY-MM-DD HH:MM:SS)."

        event = Event(
            title=title,
            description=description,
            start_time=start_dt,
            end_time=end_dt,
            organizer_id=organizer_user_id,
            event_type=event_type
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        return f"Event created successfully! ID: {event.id}, Title: {event.title}"
    except Exception as e:
        db.rollback()
        return f"Error creating event: {str(e)}"
    finally:
        db.close()

@mcp.tool()
def list_hackathons() -> str:
    """List upcoming hackathons."""
    db = SessionLocal()
    try:
        hackathons = db.query(Hackathon).limit(10).all()
        if not hackathons:
            return "No hackathons found."
        return "\n".join([f"Title: {h.title}, Mode: {h.mode}, Status: {h.status}" for h in hackathons])
    finally:
        db.close()

@mcp.tool()
def list_communities() -> str:
    """List all communities."""
    db = SessionLocal()
    try:
        communities = db.query(Community).limit(10).all()
        if not communities:
            return "No communities found."
        return "\n".join([f"Name: {c.name}, Category: {c.category}, Members: {c.member_count}" for c in communities])
    finally:
        db.close()

if __name__ == "__main__":
    mcp.run()
