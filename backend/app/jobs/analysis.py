import asyncio
from typing import Dict, Optional
from datetime import datetime

from ..ai.commander import ai_commander
from ..db.storage import storage
from ..models import TimelineEntry, TimelineEntryType


class JobQueue:
    """Simple async job queue for background tasks"""

    def __init__(self):
        self.running_jobs: Dict[str, asyncio.Task] = {}

    async def run_incident_analysis(self, incident_id: str) -> Dict:
        """Run deep incident analysis in background"""
        try:
            # Perform AI analysis
            analysis = await ai_commander.analyze_incident(incident_id)

            # Add timeline entry
            timeline_entry = TimelineEntry(
                incident_id=incident_id,
                entry_type=TimelineEntryType.AI_ANALYSIS,
                title="Deep analysis completed",
                description=f"AI Commander completed deep analysis",
                actor="Background Job"
            )
            storage.add_timeline_entry(timeline_entry)

            return analysis

        except Exception as e:
            print(f"Analysis job error: {e}")
            return {"error": str(e)}

    async def generate_postmortem(self, incident_id: str) -> Optional[str]:
        """Generate incident postmortem"""
        incident = storage.get_incident(incident_id)
        if not incident:
            return None

        # Get timeline
        timeline = storage.get_timeline(incident_id)

        # Get actions
        actions = storage.list_actions(incident_id)

        # Build postmortem
        postmortem = f"""
# Incident Postmortem: {incident.title}

## Summary
**Incident ID:** {incident.id}
**Severity:** {incident.severity.value}
**Duration:** {incident.mttr_minutes or 'Ongoing'} minutes
**Status:** {incident.status.value}

## Description
{incident.description}

## Timeline
"""
        for entry in reversed(timeline[:10]):
            postmortem += f"\n- **{entry.timestamp.strftime('%Y-%m-%d %H:%M:%S')}**: {entry.title} - {entry.description}"

        postmortem += f"""

## Root Cause
{incident.root_cause or 'Under investigation'}

## Actions Taken
"""
        for action in actions:
            status_emoji = "✅" if action.status.value == "completed" else "⏳"
            postmortem += f"\n{status_emoji} {action.title}: {action.description}"

        postmortem += f"""

## Lessons Learned
- Review monitoring and alerting for earlier detection
- Update runbooks based on resolution steps
- Consider preventive measures to avoid recurrence

## Follow-up Actions
- Schedule post-incident review meeting
- Update documentation and runbooks
- Implement monitoring improvements
"""

        return postmortem

    def submit_job(self, job_id: str, coro):
        """Submit an async job"""
        task = asyncio.create_task(coro)
        self.running_jobs[job_id] = task
        return task


# Global job queue
job_queue = JobQueue()
