from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
import uuid


class EventType(str, Enum):
    """Event type classification"""
    LOG = "log"
    METRIC = "metric"
    ALERT = "alert"
    TRACE = "trace"
    USER_ACTION = "user_action"


class EventCreate(BaseModel):
    """Request model for creating an event"""
    incident_id: str
    event_type: EventType
    message: str
    level: str = Field(default="info", description="Log level: debug, info, warning, error, critical")
    source: str = Field(default="unknown")
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Event(BaseModel):
    """Event data model - logs, metrics, alerts"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    incident_id: str
    event_type: EventType
    message: str
    level: str = "info"
    source: str = "unknown"
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Vector embedding for semantic search
    embedding: Optional[list] = Field(default=None, exclude=True)

    class Config:
        json_schema_extra = {
            "example": {
                "incident_id": "123e4567-e89b-12d3-a456-426614174000",
                "event_type": "log",
                "message": "PostgreSQL connection pool exhausted",
                "level": "error",
                "source": "api-server-01",
                "metadata": {
                    "service": "user-api",
                    "region": "us-east-1",
                    "container_id": "abc123"
                }
            }
        }
