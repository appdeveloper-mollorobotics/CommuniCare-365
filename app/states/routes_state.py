import reflex as rx
import pandas as pd
import sqlalchemy
import logging
from typing import TypedDict, Optional
from app.states.settings_state import SettingsState


class Route(TypedDict):
    setuserid: str
    endpoint: str
    connection: str
    optional: str
    imei_number: str


class RoutesState(rx.State):
    routes: list[Route] = []
    filter_text: str = ""
    show_edit_dialog: bool = False
    editing_route: Optional[Route] = None
    selected_routes: set[str] = set()
    connection_options: list[str] = ["webhook", "custom"]

    async def _get_engine(self):
        settings_state = await self.get_state(SettingsState)
        return sqlalchemy.create_engine(settings_state.database_url)

    @rx.event
    async def fetch_routes(self):
        try:
            engine = await self._get_engine()
            with engine.connect() as conn:
                df = pd.read_sql(
                    "SELECT setuserid, endpoint, connection, optional, imei_number FROM routes",
                    conn,
                )
            df["optional"] = df["optional"].fillna("")
            df["imei_number"] = df["imei_number"].fillna("")
            self.routes = df.to_dict("records")
        except Exception as e:
            logging.exception(f"Error fetching routes: {e}")
            self.routes = []

    @rx.var
    def filtered_routes(self) -> list[Route]:
        if not self.filter_text:
            return self.routes
        return [
            r
            for r in self.routes
            if self.filter_text.lower() in r["setuserid"].lower()
            or self.filter_text.lower() in r["endpoint"].lower()
            or self.filter_text.lower() in r["connection"].lower()
            or (self.filter_text.lower() in str(r.get("optional", "")).lower())
            or (self.filter_text.lower() in str(r.get("imei_number", "")).lower())
        ]

    def _reset_edit_state(self):
        self.show_edit_dialog = False
        self.editing_route = None

    @rx.event
    def open_add_dialog(self):
        self.editing_route = None
        self.show_edit_dialog = True

    @rx.event
    def open_edit_dialog(self, route: Route):
        self.editing_route = route
        self.show_edit_dialog = True

    @rx.event
    def close_dialog(self):
        self._reset_edit_state()

    @rx.event
    async def save_route(self, form_data: dict):
        setuserid = form_data.get("setuserid")
        endpoint = form_data.get("endpoint")
        connection = form_data.get("connection")
        optional = form_data.get("optional", "")
        imei_number = form_data.get("imei_number", "")
        if not all([setuserid, endpoint, connection]):
            yield rx.toast.error("Set User ID, Endpoint and Connection are required.")
            return
        try:
            engine = await self._get_engine()
            with engine.connect() as conn:
                if self.editing_route:
                    original_endpoint = self.editing_route["endpoint"]
                    stmt = sqlalchemy.text("""UPDATE routes SET setuserid = :setuserid, endpoint = :endpoint, 
                        connection = :connection, optional = :optional, imei_number = :imei_number
                        WHERE endpoint = :original_endpoint""")
                    conn.execute(
                        stmt,
                        parameters={
                            "setuserid": setuserid,
                            "endpoint": endpoint,
                            "connection": connection,
                            "optional": optional,
                            "imei_number": imei_number,
                            "original_endpoint": original_endpoint,
                        },
                    )
                    conn.commit()
                    yield rx.toast.success("Route updated successfully.")
                else:
                    stmt = sqlalchemy.text("""INSERT INTO routes (setuserid, endpoint, connection, optional, imei_number) 
                        VALUES (:setuserid, :endpoint, :connection, :optional, :imei_number)""")
                    conn.execute(
                        stmt,
                        parameters={
                            "setuserid": setuserid,
                            "endpoint": endpoint,
                            "connection": connection,
                            "optional": optional,
                            "imei_number": imei_number,
                        },
                    )
                    conn.commit()
                    yield rx.toast.success("Route added successfully.")
        except Exception as e:
            logging.exception(f"Error saving route: {e}")
            yield rx.toast.error("Failed to save route.")
        self._reset_edit_state()
        yield RoutesState.fetch_routes

    @rx.event
    async def delete_route(self, endpoint: str):
        try:
            engine = await self._get_engine()
            with engine.connect() as conn:
                stmt = sqlalchemy.text("DELETE FROM routes WHERE endpoint = :endpoint")
                conn.execute(stmt, parameters={"endpoint": endpoint})
                conn.commit()
        except Exception as e:
            logging.exception(f"Error deleting route: {e}")
            yield rx.toast.error("Failed to delete route.")
            return
        self.routes = [r for r in self.routes if r["endpoint"] != endpoint]
        yield rx.toast.info("Route deleted.")

    @rx.event
    def toggle_selection(self, endpoint: str, checked: bool):
        current_set = set(self.selected_routes)
        if checked:
            current_set.add(endpoint)
        else:
            current_set.discard(endpoint)
        self.selected_routes = current_set

    @rx.var
    def all_selected(self) -> bool:
        return (
            len(self.selected_routes) == len(self.filtered_routes)
            and len(self.filtered_routes) > 0
        )

    @rx.event
    def toggle_select_all(self):
        if self.all_selected:
            self.selected_routes = set()
        else:
            self.selected_routes = {route["endpoint"] for route in self.filtered_routes}

    @rx.event
    def delete_selected(self):
        if not self.selected_routes:
            return
        deleted_count = len(self.selected_routes)
        try:
            with engine.connect() as conn:
                stmt = sqlalchemy.text(
                    "DELETE FROM routes WHERE endpoint = ANY(:endpoints)"
                )
                conn.execute(stmt, parameters={"endpoints": list(self.selected_routes)})
                conn.commit()
        except Exception as e:
            logging.exception(f"Error deleting selected routes: {e}")
            yield rx.toast.error("Failed to delete routes.")
            return
        self.routes = [
            r for r in self.routes if r["endpoint"] not in self.selected_routes
        ]
        self.selected_routes = set()
        yield rx.toast.info(f"Deleted {deleted_count} routes.")

    @rx.event
    def export_data(self):
        df = pd.DataFrame(self.filtered_routes)
        if df.empty:
            return rx.toast.warning("No data to export.")
        csv_data = df.to_csv(index=False)
        return rx.download(data=csv_data, filename="routes.csv")