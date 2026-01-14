from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field
import uuid


class IncidentStatus(str, Enum):
    """Incident status enum"""
    OPEN = "open"
    INVESTIGATING = "investigating"
    IDENTIFIED = "identified"
    MONITORING = "monitoring"
    RESOLVED = "resolved"
    CLOSED = "closed"


class IncidentSeverity(str, Enum):
    """Incident severity levels"""
    CRITICAL = "critical"  # P0: Total system outage
    HIGH = "high"          # P1: Major feature broken
    MEDIUM = "medium"      # P2: Minor feature impacted
    LOW = "low"            # P3: Small issue
    INFO = "info"          # Informational


class IncidentCreate(BaseModel):
    """Request model for creating an incident"""
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=10)
    severity: IncidentSeverity = IncidentSeverity.MEDIUM
    source: str = Field(default="manual", description="Source of the incident (manual, alert, log)")
    tags: List[str] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)


class Incident(BaseModel):
    """Incident data model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    status: IncidentStatus = IncidentStatus.OPEN
    severity: IncidentSeverity
    source: str = "manual"
    tags: List[str] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None

    # AI Analysis
    ai_summary: Optional[str] = None
    root_cause: Optional[str] = None
    suggested_actions: List[str] = Field(default_factory=list)
    similar_incidents: List[str] = Field(default_factory=list)

    # Metrics
    mttr_minutes: Optional[float] = None  # Mean Time To Resolution

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Database connection timeout",
                "description": "Users experiencing 502 errors due to database connection timeouts",
                "severity": "high",
                "source": "datadog",
                "tags": ["database", "postgres", "timeout"],
            }
        }
