from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Optional
from datetime import datetime

from ..models import (
    Incident,
    IncidentCreate,
    IncidentStatus,
    IncidentSeverity,
    TimelineEntry,
    TimelineEntryType,
    Action,
)
from ..db.storage import storage
from ..observability.metrics import incidents_created, active_incidents, incidents_resolved

router = APIRouter(prefix="/api/incidents", tags=["incidents"])


@router.post("/", response_model=Incident, status_code=201)
async def create_incident(
    incident_data: IncidentCreate,
    background_tasks: BackgroundTasks
) -> Incident:
    """Create a new incident and trigger AI analysis"""

    # Create incident
    incident = Incident(
        title=incident_data.title,
        description=incident_data.description,
        severity=incident_data.severity,
        source=incident_data.source,
        tags=incident_data.tags,
        metadata=incident_data.metadata,
    )

    # Save to storage
    storage.create_incident(incident)

    # Add timeline entry
    timeline_entry = TimelineEntry(
        incident_id=incident.id,
        entry_type=TimelineEntryType.STATUS_CHANGE,
        title="Incident created",
        description=f"Incident created from {incident.source}",
        actor=incident.source,
    )
    storage.add_timeline_entry(timeline_entry)

    # Update metrics
    incidents_created.labels(
        severity=incident.severity.value,
        source=incident.source
    ).inc()
    active_incidents.labels(
        severity=incident.severity.value,
        status=incident.status.value
    ).inc()

    # Trigger AI analysis in background
    # background_tasks.add_task(analyze_incident, incident.id)

    return incident


@router.get("/", response_model=List[Incident])
async def list_incidents(
    status: Optional[IncidentStatus] = None,
    limit: int = 50
) -> List[Incident]:
    """List all incidents with optional filtering"""
    return storage.list_incidents(status=status, limit=limit)


@router.get("/{incident_id}", response_model=Incident)
async def get_incident(incident_id: str) -> Incident:
    """Get a specific incident by ID"""
    incident = storage.get_incident(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


@router.patch("/{incident_id}/status")
async def update_incident_status(
    incident_id: str,
    status: IncidentStatus
) -> Incident:
    """Update incident status"""
    incident = storage.get_incident(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    old_status = incident.status

    # Update incident
    updates = {"status": status, "updated_at": datetime.utcnow()}

    # If resolving, set resolved timestamp and calculate MTTR
    if status == IncidentStatus.RESOLVED and incident.status != IncidentStatus.RESOLVED:
        updates["resolved_at"] = datetime.utcnow()
        duration = (updates["resolved_at"] - incident.created_at).total_seconds()
        updates["mttr_minutes"] = duration / 60

        # Update metrics
        incidents_resolved.labels(severity=incident.severity.value).inc()
        active_incidents.labels(
            severity=incident.severity.value,
            status=old_status.value
        ).dec()

    incident = storage.update_incident(incident_id, updates)

    # Add timeline entry
    timeline_entry = TimelineEntry(
        incident_id=incident_id,
        entry_type=TimelineEntryType.STATUS_CHANGE,
        title=f"Status changed to {status.value}",
        description=f"Status updated from {old_status.value} to {status.value}",
        actor="user",
    )
    storage.add_timeline_entry(timeline_entry)

    return incident


@router.get("/{incident_id}/timeline", response_model=List[TimelineEntry])
async def get_incident_timeline(incident_id: str) -> List[TimelineEntry]:
    """Get incident timeline"""
    incident = storage.get_incident(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    return storage.get_timeline(incident_id)


@router.get("/{incident_id}/actions", response_model=List[Action])
async def get_incident_actions(incident_id: str) -> List[Action]:
    """Get suggested actions for an incident"""
    incident = storage.get_incident(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    return storage.list_actions(incident_id)
