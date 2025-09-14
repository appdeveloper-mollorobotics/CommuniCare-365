import reflex as rx
import pandas as pd
import sqlite3
import json
import logging
from typing import TypedDict, Optional

DB_FILE = "records.db"


class Route(TypedDict):
    setuserid: str
    endpoint: Optional[str]
    connection: str


class RouteState(rx.State):
    routes: list[Route] = []
    selected_route: Optional[Route] = None
    is_editing: bool = False

    def _init_db(self):
        """Initializes the database and creates the routes table if it doesn't exist."""
        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "\n                    CREATE TABLE IF NOT EXISTS routes (\n                        setuserid TEXT PRIMARY KEY,\n                        endpoint TEXT,\n                        connection TEXT NOT NULL\n                    )\n                    "
                )
                cursor.execute("SELECT COUNT(*) FROM routes")
                if cursor.fetchone()[0] == 0:
                    sample_data = [
                        ("user1", "/api/v1/data", "active"),
                        ("user2", "/api/v1/status", "inactive"),
                    ]
                    cursor.executemany(
                        "INSERT INTO routes (setuserid, endpoint, connection) VALUES (?,?,?)",
                        sample_data,
                    )
                    logging.info(
                        "Database initialized and populated with sample route data."
                    )
                conn.commit()
        except Exception as e:
            logging.exception(f"Error initializing routes table: {e}")

    @rx.event
    def fetch_routes(self):
        self._init_db()
        try:
            with sqlite3.connect(DB_FILE) as conn:
                df = pd.read_sql("SELECT * FROM routes ORDER BY setuserid", conn)
            self.routes = df.to_dict("records")
        except Exception as e:
            logging.exception(f"Error fetching routes: {e}")
            self.routes = []

    @rx.event
    def select_route(self, route: Route):
        self.selected_route = route
        self.is_editing = True

    @rx.event
    def deselect_route(self):
        self.selected_route = None
        self.is_editing = False

    @rx.event
    def handle_submit(self, form_data: dict):
        if self.selected_route:
            return RouteState.update_route(form_data)
        else:
            return RouteState.add_route(form_data)

    def _add_route_db(self, form_data: dict):
        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO routes (setuserid, endpoint, connection) VALUES (?, ?, ?)",
                    (
                        form_data["setuserid"],
                        form_data["endpoint"],
                        form_data["connection"],
                    ),
                )
                conn.commit()
        except Exception as e:
            logging.exception(f"Error adding route: {e}")

    @rx.event
    def add_route(self, form_data: dict):
        self._add_route_db(form_data)
        yield RouteState.fetch_routes
        self.is_editing = False

    def _update_route_db(self, form_data: dict):
        if not self.selected_route:
            return
        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE routes SET endpoint=?, connection=? WHERE setuserid=?",
                    (
                        form_data["endpoint"],
                        form_data["connection"],
                        self.selected_route["setuserid"],
                    ),
                )
                conn.commit()
        except Exception as e:
            logging.exception(f"Error updating route: {e}")

    @rx.event
    def update_route(self, form_data: dict):
        self._update_route_db(form_data)
        yield RouteState.fetch_routes
        yield RouteState.deselect_route

    def _delete_route_db(self, route_id: str):
        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM routes WHERE setuserid=?", (route_id,))
                conn.commit()
        except Exception as e:
            logging.exception(f"Error deleting route: {e}")

    @rx.event
    def delete_route(self, route_id: str):
        self._delete_route_db(route_id)
        yield RouteState.fetch_routes
        yield RouteState.deselect_route

    @rx.event
    def set_new_route(self):
        self.selected_route = None
        self.is_editing = True