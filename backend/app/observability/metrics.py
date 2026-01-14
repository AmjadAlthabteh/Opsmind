from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time
from functools import wraps


# Incident metrics
incidents_created = Counter(
    "incidents_created_total",
    "Total number of incidents created",
    ["severity", "source"]
)

incidents_resolved = Counter(
    "incidents_resolved_total",
    "Total number of incidents resolved",
    ["severity"]
)

incident_duration = Histogram(
    "incident_duration_seconds",
    "Time to resolve incidents",
    ["severity"],
    buckets=[60, 300, 900, 1800, 3600, 7200, 14400, 28800]
)

active_incidents = Gauge(
    "active_incidents",
    "Number of currently active incidents",
    ["severity", "status"]
)

# AI metrics
ai_analysis_duration = Histogram(
    "ai_analysis_duration_seconds",
    "Time taken for AI analysis",
    ["analysis_type"],
    buckets=[0.5, 1, 2, 5, 10, 30, 60]
)

ai_suggestions_generated = Counter(
    "ai_suggestions_generated_total",
    "Total AI suggestions generated",
    ["suggestion_type"]
)

# API metrics
http_requests = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

http_request_duration = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration",
    ["method", "endpoint"],
    buckets=[0.01, 0.05, 0.1, 0.5, 1, 2, 5]
)

websocket_connections = Gauge(
    "websocket_connections",
    "Active WebSocket connections"
)

# Event metrics
events_ingested = Counter(
    "events_ingested_total",
    "Total events ingested",
    ["event_type", "source"]
)


def track_request_metrics(endpoint: str):
    """Decorator to track HTTP request metrics"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            method = "POST"  # Can be extracted from request
            status = 200

            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                status = 500
                raise
            finally:
                duration = time.time() - start_time
                http_requests.labels(method=method, endpoint=endpoint, status=status).inc()
                http_request_duration.labels(method=method, endpoint=endpoint).observe(duration)

        return wrapper
    return decorator


def get_metrics():
    """Get current metrics in Prometheus format"""
    return generate_latest()
