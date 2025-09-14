import reflex as rx
import pandas as pd
import logging
from typing import TypedDict, Optional
from sqlalchemy import text


class Route(TypedDict):
    setuserid: str
    endpoint: Optional[str]
    connection: str


class RouteState(rx.State):
    routes: list[Route] = []
    selected_route: Optional[Route] = None
    is_editing: bool = False

    @rx.event
    async def fetch_routes(self):
        try:
            async with rx.asession() as session:
                result = await session.execute(
                    text("SELECT * FROM routes ORDER BY setuserid")
                )
                self.routes = result.mappings().all()
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

    async def _add_route_db(self, form_data: dict):
        try:
            async with rx.asession() as session:
                await session.execute(
                    text(
                        "INSERT INTO routes (setuserid, endpoint, connection) VALUES (:setuserid, :endpoint, :connection)"
                    ),
                    params=form_data,
                )
                await session.commit()
        except Exception as e:
            logging.exception(f"Error adding route: {e}")

    @rx.event
    async def add_route(self, form_data: dict):
        await self._add_route_db(form_data)
        yield RouteState.fetch_routes
        self.is_editing = False

    async def _update_route_db(self, form_data: dict):
        if not self.selected_route:
            return
        try:
            async with rx.asession() as session:
                params = {
                    "endpoint": form_data["endpoint"],
                    "connection": form_data["connection"],
                    "setuserid": self.selected_route["setuserid"],
                }
                await session.execute(
                    text(
                        "UPDATE routes SET endpoint=:endpoint, connection=:connection WHERE setuserid=:setuserid"
                    ),
                    params=params,
                )
                await session.commit()
        except Exception as e:
            logging.exception(f"Error updating route: {e}")

    @rx.event
    async def update_route(self, form_data: dict):
        await self._update_route_db(form_data)
        yield RouteState.fetch_routes
        yield RouteState.deselect_route

    async def _delete_route_db(self, route_id: str):
        try:
            async with rx.asession() as session:
                await session.execute(
                    text("DELETE FROM routes WHERE setuserid=:setuserid"),
                    params={"setuserid": route_id},
                )
                await session.commit()
        except Exception as e:
            logging.exception(f"Error deleting route: {e}")

    @rx.event
    async def delete_route(self, route_id: str):
        await self._delete_route_db(route_id)
        yield RouteState.fetch_routes
        yield RouteState.deselect_route

    @rx.event
    def set_new_route(self):
        self.selected_route = None
        self.is_editing = True