from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
import uuid


class ActionStatus(str, Enum):
    """Action status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class ActionCreate(BaseModel):
    """Request model for creating an action"""
    incident_id: str
    title: str = Field(..., min_length=5)
    description: str
    suggested_by: str = Field(default="ai", description="Who suggested this action")
    priority: int = Field(default=1, ge=1, le=5, description="Priority 1 (highest) to 5 (lowest)")


class Action(BaseModel):
    """Remediation action model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    incident_id: str
    title: str
    description: str
    status: ActionStatus = ActionStatus.PENDING
    suggested_by: str = "ai"
    executed_by: Optional[str] = None
    priority: int = 1

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    # Results
    result: Optional[str] = None
    error: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "incident_id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Restart Redis cache service",
                "description": "Restart redis-cache-01 to clear memory leak",
                "priority": 1,
                "suggested_by": "AI Commander"
            }
        }
