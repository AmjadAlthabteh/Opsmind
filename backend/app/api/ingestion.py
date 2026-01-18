from fastapi import APIRouter, HTTPException
from typing import List
import logging

from ..models import Event, EventCreate
from ..db.storage import storage
from ..observability.metrics import events_ingested

logger = logging.getLogger(__name__)
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
    """Ingest multiple events in batch with validation"""

    # Validate batch size to prevent abuse
    if len(events_data) > 1000:
        raise HTTPException(status_code=400, detail="Batch size exceeds maximum of 1000 events")

    if len(events_data) == 0:
        raise HTTPException(status_code=400, detail="Batch cannot be empty")

    created_events = []
    errors = []

    for idx, event_data in enumerate(events_data):
        try:
            # Verify incident exists
            incident = storage.get_incident(event_data.incident_id)
            if not incident:
                errors.append(f"Event {idx}: Incident not found")
                continue

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
        except Exception as e:
            logger.error(f"Failed to process event {idx}: {e}")
            errors.append(f"Event {idx}: {str(e)}")

    if errors:
        logger.warning(f"Batch ingestion completed with {len(errors)} errors")

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
