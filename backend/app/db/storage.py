from typing import Dict, List, Optional
from datetime import datetime
from ..models import Incident, Event, TimelineEntry, Action, IncidentStatus


class InMemoryStorage:
    """In-memory storage for incidents, events, and actions"""

    def __init__(self):
        self.incidents: Dict[str, Incident] = {}
        self.events: Dict[str, Event] = {}
        self.timeline: Dict[str, List[TimelineEntry]] = {}
        self.actions: Dict[str, Action] = {}

    # Incident operations
    def create_incident(self, incident: Incident) -> Incident:
        """Create a new incident"""
        self.incidents[incident.id] = incident
        self.timeline[incident.id] = []
        return incident

    def get_incident(self, incident_id: str) -> Optional[Incident]:
        """Get incident by ID"""
        return self.incidents.get(incident_id)

    def list_incidents(self, status: Optional[IncidentStatus] = None, limit: int = 50) -> List[Incident]:
        """List all incidents with optional status filter"""
        incidents = list(self.incidents.values())
        if status:
            incidents = [i for i in incidents if i.status == status]
        # Sort by created_at descending
        incidents.sort(key=lambda x: x.created_at, reverse=True)
        return incidents[:limit]

    def update_incident(self, incident_id: str, updates: dict) -> Optional[Incident]:
        """Update incident fields"""
        incident = self.incidents.get(incident_id)
        if not incident:
            return None

        for key, value in updates.items():
            if hasattr(incident, key):
                setattr(incident, key, value)

        incident.updated_at = datetime.utcnow()
        return incident

    # Event operations
    def create_event(self, event: Event) -> Event:
        """Create a new event"""
        self.events[event.id] = event
        return event

    def list_events(self, incident_id: str, limit: int = 100) -> List[Event]:
        """List events for an incident"""
        events = [e for e in self.events.values() if e.incident_id == incident_id]
        events.sort(key=lambda x: x.timestamp, reverse=True)
        return events[:limit]

    # Timeline operations
    def add_timeline_entry(self, entry: TimelineEntry) -> TimelineEntry:
        """Add a timeline entry"""
        if entry.incident_id not in self.timeline:
            self.timeline[entry.incident_id] = []
        self.timeline[entry.incident_id].append(entry)
        return entry

    def get_timeline(self, incident_id: str) -> List[TimelineEntry]:
        """Get timeline for an incident"""
        entries = self.timeline.get(incident_id, [])
        return sorted(entries, key=lambda x: x.timestamp, reverse=True)

    # Action operations
    def create_action(self, action: Action) -> Action:
        """Create a new action"""
        self.actions[action.id] = action
        return action

    def get_action(self, action_id: str) -> Optional[Action]:
        """Get action by ID"""
        return self.actions.get(action_id)

    def list_actions(self, incident_id: str) -> List[Action]:
        """List actions for an incident"""
        actions = [a for a in self.actions.values() if a.incident_id == incident_id]
        actions.sort(key=lambda x: (x.priority, x.created_at))
        return actions

    def update_action(self, action_id: str, updates: dict) -> Optional[Action]:
        """Update action fields"""
        action = self.actions.get(action_id)
        if not action:
            return None

        for key, value in updates.items():
            if hasattr(action, key):
                setattr(action, key, value)

        return action


# Global storage instance
storage = InMemoryStorage()
