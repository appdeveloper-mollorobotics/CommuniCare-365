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
                logging.warning("Table 'records' not found, skipping fetch.")
                return
            with engine.connect() as conn:
                df = pd.read_sql("SELECT * FROM records", conn)
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
            return []
        try:
            image_filenames = json.loads(self.selected_record["images"])
            return [f"/received_images/{fname}" for fname in image_filenames]
        except Exception as e:
            logging.exception(f"Error parsing image URLs: {e}")
            return []

    @rx.event
    def show_details(self, record: Record):
        self.selected_record = record
        coords = self._parse_gps(record["gps_location"])
        if coords:
            self.map_center = latlng(lat=coords[0], lng=coords[1])
            self.map_zoom = 15.0