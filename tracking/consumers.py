import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .tracking_module import update_driver_location, get_driver_location

class LocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Accept WebSocket connection.
        """
        await self.accept()
        self.last_location = None  # Store last known location

    async def receive(self, text_data):
        """
        Handles incoming WebSocket messages containing location updates.
        """
        try:
            data = json.loads(text_data)
            driver_id = data.get("driver_id")
            latitude = float(data.get("latitude"))
            longitude = float(data.get("longitude"))

            if not all([driver_id, latitude, longitude]):
                await self.send(json.dumps({"error": "Missing parameters"}))
                return

            # Retrieve the last known location
            last_location = get_driver_location(driver_id)

            # Update location only if it has changed
            if last_location is None or (latitude, longitude) != last_location:
                update_driver_location(driver_id, latitude, longitude)
                self.last_location = (latitude, longitude)

                # Broadcast update
                await self.send(json.dumps({
                    "message": "Location updated successfully",
                    "driver_id": driver_id,
                    "latitude": latitude,
                    "longitude": longitude
                }))

        except json.JSONDecodeError:
            await self.send(json.dumps({"error": "Invalid JSON data"}))

    async def disconnect(self, close_code):
        """
        Handle WebSocket disconnection.
        """
        print(f"WebSocket closed: {close_code}")