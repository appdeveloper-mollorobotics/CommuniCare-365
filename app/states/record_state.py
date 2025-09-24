import reflex as rx
import reflex_enterprise as rxe
from reflex_enterprise.components.map.types import LatLng, latlng
import pandas as pd
import sqlalchemy
import json
import logging
from typing import TypedDict
from app.states.settings_state import SettingsState


class Record(TypedDict):
    userid: int
    username: str
    vehicle_reg: str
    created_at: str
    contact_number: str
    gps_location: str
    images: str


class RecordState(rx.State):
    records: list[Record] = []
    usernames: list[str] = ["All"]
    selected_username: str = "All"
    start_date: str = ""
    end_date: str = ""
    selected_record: Record | None = None
    map_center: LatLng = latlng(lat=25.0, lng=25.0)
    map_zoom: float = 4.5
    active_tab: str = "Dashboard"
    trace_vehicle_reg: str = ""
    trace_path: list[LatLng] = []

    async def _get_engine(self):
        settings_state = await self.get_state(SettingsState)
        return sqlalchemy.create_engine(settings_state.database_url)

    def set_active_tab(self, tab: str):
        self.active_tab = tab

    @rx.event
    async def fetch_records(self):
        self.records = []
        self.usernames = ["All"]
        try:
            engine = await self._get_engine()
            inspector = sqlalchemy.inspect(engine)
            if not inspector.has_table("records"):
                logging.warning("Table 'records' not found, using sample data.")
                self.records = [
                    {
                        "userid": 1,
                        "username": "sample_user",
                        "vehicle_reg": "XYZ-123",
                        "created_at": "2024-05-20 10:00:00",
                        "contact_number": "1234567890",
                        "gps_location": "34.0522,-118.2437",
                        "images": "[]",
                    },
                    {
                        "userid": 2,
                        "username": "another_user",
                        "vehicle_reg": "ABC-456",
                        "created_at": "2024-05-20 11:30:00",
                        "contact_number": "0987654321",
                        "gps_location": "40.7128,-74.0060",
                        "images": "[]",
                    },
                ]
                self.usernames.extend(["sample_user", "another_user"])
                return
            with engine.connect() as conn:
                df = pd.read_sql("SELECT * FROM records", conn)
            if df.empty:
                self.records = [
                    {
                        "userid": 1,
                        "username": "sample_user",
                        "vehicle_reg": "XYZ-123",
                        "created_at": "2024-05-20 10:00:00",
                        "contact_number": "1234567890",
                        "gps_location": "34.0522,-118.2437",
                        "images": "[]",
                    },
                    {
                        "userid": 2,
                        "username": "another_user",
                        "vehicle_reg": "ABC-456",
                        "created_at": "2024-05-20 11:30:00",
                        "contact_number": "0987654321",
                        "gps_location": "40.7128,-74.0060",
                        "images": "[]",
                    },
                ]
                self.usernames.extend(["sample_user", "another_user"])
            else:
                self.records = df.to_dict("records")
                self.usernames.extend(df["username"].unique().tolist())
        except Exception as e:
            logging.exception(f"Error fetching records: {e}")

    @rx.var
    def filtered_records(self) -> list[Record]:
        df = pd.DataFrame(self.records)
        if df.empty:
            return []
        filtered_df = df.copy()
        if self.selected_username != "All":
            filtered_df = filtered_df[filtered_df["username"] == self.selected_username]
        if self.start_date and self.end_date:
            try:
                start_dt = pd.to_datetime(self.start_date)
                end_dt = pd.to_datetime(self.end_date)
                filtered_df["created_at_dt"] = pd.to_datetime(filtered_df["created_at"])
                filtered_df = filtered_df[
                    (filtered_df["created_at_dt"] >= start_dt)
                    & (filtered_df["created_at_dt"] <= end_dt)
                ]
                filtered_df = filtered_df.drop(columns=["created_at_dt"])
            except Exception as e:
                logging.exception(f"Date filter error: {e}")
        return filtered_df.to_dict("records")

    def _parse_gps(self, gps_str: str) -> list[float] | None:
        try:
            lat, lon = map(float, gps_str.split(","))
            return [lat, lon]
        except Exception as e:
            logging.exception(f"Error parsing GPS string: {e}")
            return None

    @rx.var
    def map_markers(self) -> list[rx.Component]:
        markers = []
        for record in self.filtered_records:
            coords = self._parse_gps(record["gps_location"])
            if coords:
                markers.append(
                    rxe.map.marker(
                        position=latlng(lat=coords[0], lng=coords[1]),
                        content=rx.icon("map-pin", color="red"),
                    )
                )
        return markers

    @rx.var
    def image_urls(self) -> list[str]:
        if not self.selected_record or not self.selected_record["images"]:
            return ["/placeholder.svg"]
        try:
            image_filenames = json.loads(self.selected_record["images"])
            if not image_filenames:
                return ["/placeholder.svg"]
            return [f"/received_images/{fname}" for fname in image_filenames]
        except (json.JSONDecodeError, TypeError) as e:
            logging.exception(f"Error decoding image JSON: {e}")
            return ["/placeholder.svg"]

    @rx.event
    def show_details(self, record: Record):
        self.selected_record = record
        coords = self._parse_gps(record["gps_location"])
        if coords:
            self.map_center = latlng(lat=coords[0], lng=coords[1])
            self.map_zoom = 15.0

    @rx.event
    def set_trace_vehicle_reg(self, reg: str):
        self.trace_vehicle_reg = reg

    @rx.event
    def trace_vehicle(self):
        if not self.trace_vehicle_reg:
            return rx.toast.warning("Please enter a vehicle registration.")
        vehicle_records = [
            r for r in self.records if r["vehicle_reg"] == self.trace_vehicle_reg
        ]
        if not vehicle_records:
            self.trace_path = []
            return rx.toast.info(f"No records found for {self.trace_vehicle_reg}")
        try:
            sorted_records = sorted(
                vehicle_records, key=lambda r: pd.to_datetime(r["created_at"])
            )
        except Exception as e:
            logging.exception(f"Error sorting records by date: {e}")
            sorted_records = vehicle_records
        path = []
        for record in sorted_records:
            coords = self._parse_gps(record["gps_location"])
            if coords:
                path.append(latlng(lat=coords[0], lng=coords[1]))
        self.trace_path = path
        if path:
            self.map_center = path[0]
            self.map_zoom = 12.0
            return rx.toast.success(f"Showing trace for {self.trace_vehicle_reg}")