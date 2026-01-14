"""Seed script to populate the database with demo incidents"""
import asyncio
import sys
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from app.models import (
    Incident,
    IncidentSeverity,
    IncidentStatus,
    Event,
    EventType,
    Action,
    ActionStatus,
    TimelineEntry,
    TimelineEntryType,
)
from app.db.storage import storage
from datetime import datetime, timedelta


def create_demo_incidents():
    """Create demo incidents with events, actions, and timeline"""

    # Incident 1: Database Connection Pool Exhaustion
    incident1 = Incident(
        title="Database Connection Pool Exhausted",
        description="Users experiencing 502 errors due to PostgreSQL connection pool exhaustion. API response times degraded significantly.",
        severity=IncidentSeverity.HIGH,
        status=IncidentStatus.RESOLVED,
        source="datadog",
        tags=["database", "postgres", "api", "production"],
        created_at=datetime.utcnow() - timedelta(hours=2),
        resolved_at=datetime.utcnow() - timedelta(hours=1),
        mttr_minutes=60,
        ai_summary="Connection pool size was too small for current traffic load",
        root_cause="Database connection pool configured with max_connections=20, insufficient for peak load",
        suggested_actions=[
            "Increase connection pool size to 50",
            "Add connection pool monitoring",
            "Review query performance for long-running connections"
        ],
    )
    storage.create_incident(incident1)

    # Add events for incident 1
    events1 = [
        Event(
            incident_id=incident1.id,
            event_type=EventType.ALERT,
            message="High API error rate detected: 15% 502 errors",
            level="error",
            source="datadog",
            timestamp=datetime.utcnow() - timedelta(hours=2),
        ),
        Event(
            incident_id=incident1.id,
            event_type=EventType.LOG,
            message="FATAL: sorry, too many clients already",
            level="error",
            source="api-server-01",
            timestamp=datetime.utcnow() - timedelta(hours=2, minutes=2),
        ),
        Event(
            incident_id=incident1.id,
            event_type=EventType.METRIC,
            message="Database connection pool utilization: 100%",
            level="warning",
            source="postgres-primary",
            timestamp=datetime.utcnow() - timedelta(hours=2, minutes=5),
        ),
    ]
    for event in events1:
        storage.create_event(event)

    # Add timeline for incident 1
    timeline1 = [
        TimelineEntry(
            incident_id=incident1.id,
            entry_type=TimelineEntryType.STATUS_CHANGE,
            title="Incident created",
            description="Incident detected by Datadog monitoring",
            actor="datadog",
            timestamp=datetime.utcnow() - timedelta(hours=2),
        ),
        TimelineEntry(
            incident_id=incident1.id,
            entry_type=TimelineEntryType.AI_ANALYSIS,
            title="AI analysis completed",
            description="Root cause identified: connection pool exhaustion",
            actor="AI Commander",
            timestamp=datetime.utcnow() - timedelta(hours=1, minutes=50),
        ),
        TimelineEntry(
            incident_id=incident1.id,
            entry_type=TimelineEntryType.USER_ACTION,
            title="Connection pool size increased",
            description="Updated max_connections from 20 to 50",
            actor="SRE Team",
            timestamp=datetime.utcnow() - timedelta(hours=1, minutes=30),
        ),
        TimelineEntry(
            incident_id=incident1.id,
            entry_type=TimelineEntryType.STATUS_CHANGE,
            title="Status changed to resolved",
            description="Error rate returned to normal levels",
            actor="SRE Team",
            timestamp=datetime.utcnow() - timedelta(hours=1),
        ),
    ]
    for entry in timeline1:
        storage.add_timeline_entry(entry)

    # Incident 2: Redis Cache Memory Leak
    incident2 = Incident(
        title="Redis Cache Memory Leak",
        description="Redis memory usage growing unbounded, approaching server limits. Cache hit rate declining.",
        severity=IncidentSeverity.MEDIUM,
        status=IncidentStatus.INVESTIGATING,
        source="prometheus",
        tags=["redis", "cache", "memory", "production"],
        created_at=datetime.utcnow() - timedelta(minutes=30),
        ai_summary="Memory leak detected in Redis cache, likely due to missing TTL on keys",
    )
    storage.create_incident(incident2)

    # Add events for incident 2
    events2 = [
        Event(
            incident_id=incident2.id,
            event_type=EventType.ALERT,
            message="Redis memory usage exceeds 80% threshold",
            level="warning",
            source="prometheus",
            timestamp=datetime.utcnow() - timedelta(minutes=30),
        ),
        Event(
            incident_id=incident2.id,
            event_type=EventType.METRIC,
            message="Redis memory: 6.8GB / 8GB (85% used)",
            level="warning",
            source="redis-01",
            timestamp=datetime.utcnow() - timedelta(minutes=25),
        ),
    ]
    for event in events2:
        storage.create_event(event)

    # Add actions for incident 2
    actions2 = [
        Action(
            incident_id=incident2.id,
            title="Analyze Redis key patterns",
            description="Use SCAN command to identify keys without TTL",
            priority=1,
            status=ActionStatus.IN_PROGRESS,
            suggested_by="AI Commander",
        ),
        Action(
            incident_id=incident2.id,
            title="Set TTL on orphaned keys",
            description="Add appropriate expiration to keys missing TTL",
            priority=2,
            status=ActionStatus.PENDING,
            suggested_by="AI Commander",
        ),
        Action(
            incident_id=incident2.id,
            title="Add monitoring for keys without TTL",
            description="Create alert for growing number of keys without expiration",
            priority=3,
            status=ActionStatus.PENDING,
            suggested_by="AI Commander",
        ),
    ]
    for action in actions2:
        storage.create_action(action)

    # Incident 3: API Rate Limiting Not Working
    incident3 = Incident(
        title="API Rate Limiting Bypass Detected",
        description="User reported ability to bypass rate limiting by rotating IP addresses. Potential abuse vector.",
        severity=IncidentSeverity.CRITICAL,
        status=IncidentStatus.OPEN,
        source="manual",
        tags=["api", "security", "rate-limiting"],
        created_at=datetime.utcnow() - timedelta(minutes=5),
    )
    storage.create_incident(incident3)

    # Incident 4: Disk Space Warning
    incident4 = Incident(
        title="Application Server Disk Space at 85%",
        description="Log files and temporary data consuming excessive disk space on app-server-03",
        severity=IncidentSeverity.LOW,
        status=IncidentStatus.OPEN,
        source="nagios",
        tags=["infrastructure", "disk", "app-server"],
        created_at=datetime.utcnow() - timedelta(minutes=10),
    )
    storage.create_incident(incident4)

    print("✅ Created 4 demo incidents")
    print(f"   - {incident1.id}: {incident1.title} ({incident1.status})")
    print(f"   - {incident2.id}: {incident2.title} ({incident2.status})")
    print(f"   - {incident3.id}: {incident3.title} ({incident3.status})")
    print(f"   - {incident4.id}: {incident4.title} ({incident4.status})")
    print(f"\n✅ Created {len(events1) + len(events2)} events")
    print(f"✅ Created {len(timeline1)} timeline entries")
    print(f"✅ Created {len(actions2)} suggested actions")
    print("\nDemo data loaded successfully! 🎉")


if __name__ == "__main__":
    create_demo_incidents()
