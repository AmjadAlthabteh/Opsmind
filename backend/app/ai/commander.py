from typing import List, Dict, Optional
from datetime import datetime
import os

try:
    from langchain_openai import ChatOpenAI
    from langchain.prompts import ChatPromptTemplate
    from langchain.chains import LLMChain
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    print("LangChain not available. AI Commander will use fallback mode.")

from ..models import Incident, Event, Action, ActionStatus, TimelineEntry, TimelineEntryType
from ..db.storage import storage
from ..observability.metrics import ai_analysis_duration, ai_suggestions_generated
import time


class AICommander:
    """AI Incident Commander using LangChain"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

        if LANGCHAIN_AVAILABLE and self.api_key:
            self.llm = ChatOpenAI(
                model="gpt-4",
                temperature=0.3,
                openai_api_key=self.api_key
            )
            self.enabled = True
        else:
            self.llm = None
            self.enabled = False
            print("AI Commander disabled: LangChain or API key not available")

    async def analyze_incident(self, incident_id: str) -> Dict:
        """Perform comprehensive incident analysis"""
        start_time = time.time()

        incident = storage.get_incident(incident_id)
        if not incident:
            return {"error": "Incident not found"}

        # Get related events
        events = storage.list_events(incident_id, limit=50)

        if not self.enabled:
            # Fallback analysis
            return self._fallback_analysis(incident, events)

        # Build context
        context = self._build_context(incident, events)

        # Create analysis prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert SRE and incident commander.
            Analyze the incident and provide:
            1. Root cause hypothesis
            2. Severity assessment
            3. Suggested remediation actions (prioritized)
            4. Similar past incidents (if any)
            5. Estimated blast radius

            Be concise and actionable."""),
            ("user", "{context}")
        ])

        try:
            # Run analysis
            chain = prompt | self.llm
            response = await chain.ainvoke({"context": context})

            # Parse response
            analysis = self._parse_analysis(response.content)

            # Update incident with AI insights
            storage.update_incident(incident_id, {
                "ai_summary": analysis.get("summary", ""),
                "root_cause": analysis.get("root_cause", ""),
                "suggested_actions": analysis.get("actions", []),
            })

            # Create suggested actions
            for i, action_desc in enumerate(analysis.get("actions", [])[:5]):
                action = Action(
                    incident_id=incident_id,
                    title=f"Action {i+1}",
                    description=action_desc,
                    priority=i+1,
                    suggested_by="AI Commander",
                    status=ActionStatus.PENDING
                )
                storage.create_action(action)

            # Add timeline entry
            timeline_entry = TimelineEntry(
                incident_id=incident_id,
                entry_type=TimelineEntryType.AI_ANALYSIS,
                title="AI analysis completed",
                description=analysis.get("summary", "Analysis complete"),
                actor="AI Commander"
            )
            storage.add_timeline_entry(timeline_entry)

            # Track metrics
            duration = time.time() - start_time
            ai_analysis_duration.labels(analysis_type="full_analysis").observe(duration)
            ai_suggestions_generated.labels(suggestion_type="action").inc(len(analysis.get("actions", [])))

            return analysis

        except Exception as e:
            print(f"AI analysis error: {e}")
            return self._fallback_analysis(incident, events)

    def _build_context(self, incident: Incident, events: List[Event]) -> str:
        """Build context string for AI analysis"""
        context = f"""
INCIDENT DETAILS:
Title: {incident.title}
Description: {incident.description}
Severity: {incident.severity.value}
Status: {incident.status.value}
Created: {incident.created_at}
Tags: {', '.join(incident.tags)}

RECENT EVENTS ({len(events)} total):
"""
        # Add most recent events
        for event in events[:10]:
            context += f"\n[{event.timestamp}] [{event.level}] {event.source}: {event.message}"

        return context

    def _parse_analysis(self, response: str) -> Dict:
        """Parse AI response into structured data"""
        # Simple parsing - in production, use structured output
        return {
            "summary": response[:200],
            "root_cause": "AI analysis in progress",
            "actions": [
                "Check service logs for errors",
                "Verify database connection pool",
                "Review recent deployments",
                "Check resource utilization"
            ]
        }

    def _fallback_analysis(self, incident: Incident, events: List[Event]) -> Dict:
        """Fallback analysis when AI is not available"""
        error_events = [e for e in events if e.level == "error"]

        actions = [
            "Review error logs and stack traces",
            "Check system resource utilization (CPU, memory, disk)",
            "Verify external service dependencies",
            "Review recent code deployments or configuration changes",
        ]

        if "database" in incident.title.lower() or "database" in incident.description.lower():
            actions.insert(0, "Check database connection pool and query performance")

        return {
            "summary": f"Detected {len(error_events)} error events. Manual investigation recommended.",
            "root_cause": "Analysis pending - AI Commander not available",
            "actions": actions,
            "similar_incidents": [],
        }


# Global AI Commander instance
ai_commander = AICommander()
