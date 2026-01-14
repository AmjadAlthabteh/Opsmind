from fastapi import APIRouter, HTTPException
from typing import List

from ..models import Event, EventCreate
from ..db.storage import storage
from ..observability.metrics import events_ingested

router = APIRouter(prefix="/api/ingest", tags=["ingestion"])


@router.post("/events", response_model=Event, status_code=201)
async def ingest_event(event_data: EventCreate) -> Event:
    """Ingest a single event (log, metric, alert)"""

    # Verify incident exists
    incident = storage.get_incident(event_data.incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    # Create event
    event = Event(
        incident_id=event_data.incident_id,
        event_type=event_data.event_type,
        message=event_data.message,
        level=event_data.level,
        source=event_data.source,
        metadata=event_data.metadata,
    )

    # Save to storage
    storage.create_event(event)

    # Update metrics
    events_ingested.labels(
        event_type=event.event_type.value,
        source=event.source
    ).inc()

    return event


@router.post("/events/batch", response_model=List[Event], status_code=201)
async def ingest_events_batch(events_data: List[EventCreate]) -> List[Event]:
    """Ingest multiple events in batch"""

    created_events = []

    for event_data in events_data:
        # Verify incident exists
        incident = storage.get_incident(event_data.incident_id)
        if not incident:
            continue  # Skip invalid incidents in batch

        # Create event
        event = Event(
            incident_id=event_data.incident_id,
            event_type=event_data.event_type,
            message=event_data.message,
            level=event_data.level,
            source=event_data.source,
            metadata=event_data.metadata,
        )

        # Save to storage
        storage.create_event(event)
        created_events.append(event)

        # Update metrics
        events_ingested.labels(
            event_type=event.event_type.value,
            source=event.source
        ).inc()

    return created_events


@router.get("/events/{incident_id}", response_model=List[Event])
async def get_incident_events(
    incident_id: str,
    limit: int = 100
) -> List[Event]:
    """Get events for a specific incident"""

    # Verify incident exists
    incident = storage.get_incident(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    return storage.list_events(incident_id, limit=limit)
