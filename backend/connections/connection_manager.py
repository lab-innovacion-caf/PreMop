import asyncio
import logging
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket) -> str:
        await websocket.accept()
        websocket_id = str(id(websocket))
        async with self._lock:
            self.active_connections[websocket_id] = websocket
        return websocket_id

    async def disconnect(self, websocket_id: str):
        if websocket_id in self.active_connections:
            logging.info(f"Disconnecting WebSocket {websocket_id}")
            await self.active_connections[websocket_id].close()
            del self.active_connections[websocket_id]

    async def send_progress(self, websocket_id: str, progress: float):
        try:
            websocket = self.active_connections.get(websocket_id)
            if websocket:
                progress_message = {
                    "type": "progress",
                    "value": progress
                }
                await asyncio.create_task(websocket.send_json(progress_message))
                logging.info(f"Progress message sent successfully to {websocket_id}")
            else:
                logging.warning(f"WebSocket {websocket_id} not found in active connections")
        except Exception as e:
            logging.error(f"Error sending progress: {e}") 