import reflex as rx
import asyncio
import datetime
from typing import TypedDict
import logging
from ably import AblyRealtime, AblyException
from app.states.settings_state import SettingsState


class VehicleData(TypedDict):
    vehicle_registration: str
    latitude: str
    longitude: str
    timestamp: str


class AblyState(rx.State):
    client_id: str = "unity10i99p2"
    channel_name: str = "chat"
    vehicle_data: list[VehicleData] = []
    entry_1_text: str = ""
    _client: AblyRealtime | None = None
    _channel: asyncio.Future | None = None

    @rx.event
    async def ably_monitor(self):
        if self._client is not None:
            return
        try:
            settings_state = await self.get_state(SettingsState)
            self._client = AblyRealtime(
                settings_state.ably_api_key, client_id=self.client_id
            )
            self._channel = self._client.channels.get(self.channel_name)
            await self._channel.subscribe("chat-message", self._message_handler)
            print("Server is listening for incoming messages...")
        except AblyException as e:
            logging.exception(f"Error initializing Ably: {e}")

    async def _message_handler(self, message):
        try:
            if message.client_id != self._client.auth.client_id:
                data = message.data
                vehicle_registration = data.get("vehicle_registration", "Unknown")
                latitude = data.get("latitude", "18.4241")
                longitude = data.get("longitude", "-33.9249")
                timestamp = data.get(
                    "timestamp", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                if vehicle_registration and latitude and longitude and timestamp:
                    async with self:
                        new_data: VehicleData = {
                            "vehicle_registration": vehicle_registration,
                            "latitude": latitude,
                            "longitude": longitude,
                            "timestamp": timestamp,
                        }
                        self.vehicle_data.append(new_data)
                else:
                    print("Received message with incomplete data. Ignoring message.")
            else:
                print("Message sent by this client, ignoring.")
        except Exception as e:
            logging.exception(f"Error in message handler: {e}")

    @rx.event
    async def broadcast_vehicle_data(self):
        if not self._channel:
            print("Ably channel not initialized.")
            return
        try:
            await self._channel.publish(
                "chat-message", {"vehicle_registration": self.entry_1_text}
            )
            print(f"Broadcast sent: {self.entry_1_text}")
            self.entry_1_text = ""
        except AblyException as e:
            logging.exception(f"Error broadcasting data: {e}")

    def trace_selected_vehicle(self, row_data: VehicleData):
        pass