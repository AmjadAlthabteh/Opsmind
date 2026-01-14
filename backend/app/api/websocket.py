from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Set
import json
from datetime import datetime

from ..observability.metrics import websocket_connections

router = APIRouter()


class ConnectionManager:
    """Manages WebSocket connections for incident rooms"""

    def __init__(self):
        # incident_id -> set of WebSocket connections
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, incident_id: str):
        """Connect a client to an incident room"""
        await websocket.accept()

        if incident_id not in self.active_connections:
            self.active_connections[incident_id] = set()

        self.active_connections[incident_id].add(websocket)
        websocket_connections.inc()

        # Send welcome message
        await self.send_personal_message({
            "type": "connection",
            "message": f"Connected to incident room: {incident_id}",
            "timestamp": datetime.utcnow().isoformat()
        }, websocket)

    def disconnect(self, websocket: WebSocket, incident_id: str):
        """Disconnect a client from an incident room"""
        if incident_id in self.active_connections:
            self.active_connections[incident_id].discard(websocket)
            websocket_connections.dec()

            # Clean up empty rooms
            if not self.active_connections[incident_id]:
                del self.active_connections[incident_id]

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send a message to a specific client"""
        await websocket.send_json(message)

    async def broadcast_to_room(self, message: dict, incident_id: str):
        """Broadcast a message to all clients in an incident room"""
        if incident_id in self.active_connections:
            disconnected = set()

            for connection in self.active_connections[incident_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    disconnected.add(connection)

            # Remove disconnected clients
            for connection in disconnected:
                self.disconnect(connection, incident_id)

    async def broadcast_incident_update(self, incident_id: str, update_type: str, data: dict):
        """Broadcast an incident update to all connected clients"""
        message = {
            "type": update_type,
            "incident_id": incident_id,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.broadcast_to_room(message, incident_id)


# Global connection manager
manager = ConnectionManager()


@router.websocket("/ws/incidents/{incident_id}")
async def incident_room_websocket(websocket: WebSocket, incident_id: str):
    """WebSocket endpoint for real-time incident updates"""
    await manager.connect(websocket, incident_id)

    try:
        while True:
            # Receive messages from client
            data = await websocket.receive_text()

            try:
                message = json.loads(data)

                # Echo user messages to all connected clients
                await manager.broadcast_to_room({
                    "type": "user_message",
                    "incident_id": incident_id,
                    "message": message.get("message", ""),
                    "user": message.get("user", "anonymous"),
                    "timestamp": datetime.utcnow().isoformat()
                }, incident_id)

            except json.JSONDecodeError:
                await manager.send_personal_message({
                    "type": "error",
                    "message": "Invalid JSON format"
                }, websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket, incident_id)
        await manager.broadcast_to_room({
            "type": "user_disconnected",
            "incident_id": incident_id,
            "timestamp": datetime.utcnow().isoformat()
        }, incident_id)
