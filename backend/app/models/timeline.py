from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
import uuid


class TimelineEntryType(str, Enum):
    """Timeline entry types"""
    STATUS_CHANGE = "status_change"
    AI_ANALYSIS = "ai_analysis"
    USER_ACTION = "user_action"
    SYSTEM_EVENT = "system_event"
    COMMENT = "comment"


class TimelineEntry(BaseModel):
    """Timeline entry for incident history"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    incident_id: str
    entry_type: TimelineEntryType
    title: str
    description: str
    actor: str = Field(default="system", description="Who/what caused this entry")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict = Field(default_factory=dict)

    class Config:
        json_schema_extra = {
            "example": {
                "incident_id": "123e4567-e89b-12d3-a456-426614174000",
                "entry_type": "ai_analysis",
                "title": "Root cause identified",
                "description": "Redis memory leak detected in cache service",
                "actor": "AI Commander",
            }
        }
