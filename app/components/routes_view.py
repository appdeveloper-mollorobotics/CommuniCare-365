import reflex as rx
from app.states.route_state import RouteState


def route_form() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            rx.cond(
                RouteState.is_editing & RouteState.selected_route,
                "Edit Route",
                "Add New Route",
            ),
            class_name="text-xl font-bold mb-4",
        ),
        rx.el.form(
            rx.el.input(
                name="name",
                placeholder="Route Name",
                default_value=rx.cond(
                    RouteState.selected_route, RouteState.selected_route["name"], ""
                ),
                key=rx.cond(
                    RouteState.selected_route,
                    RouteState.selected_route["id"].to(str) + "name",
                    "new_name",
                ),
                class_name="w-full p-2 border rounded-md",
            ),
            rx.el.input(
                name="start_location",
                placeholder="Start Location",
                default_value=rx.cond(
                    RouteState.selected_route,
                    RouteState.selected_route["start_location"],
                    "",
                ),
                key=rx.cond(
                    RouteState.selected_route,
                    RouteState.selected_route["id"].to(str) + "start",
                    "new_start",
                ),
                class_name="w-full p-2 border rounded-md",
            ),
            rx.el.input(
                name="end_location",
                placeholder="End Location",
                default_value=rx.cond(
                    RouteState.selected_route,
                    RouteState.selected_route["end_location"],
                    "",
                ),
                key=rx.cond(
                    RouteState.selected_route,
                    RouteState.selected_route["id"].to(str) + "end",
                    "new_end",
                ),
                class_name="w-full p-2 border rounded-md",
            ),
            rx.el.input(
                name="waypoints",
                placeholder="Waypoints (JSON array)",
                default_value=rx.cond(
                    RouteState.selected_route,
                    RouteState.selected_route["waypoints"],
                    "[]",
                ),
                key=rx.cond(
                    RouteState.selected_route,
                    RouteState.selected_route["id"].to(str) + "waypoints",
                    "new_waypoints",
                ),
                class_name="w-full p-2 border rounded-md",
            ),
            rx.el.div(
                rx.el.button(
                    "Cancel",
                    on_click=RouteState.deselect_route,
                    class_name="px-4 py-2 bg-gray-300 rounded-md hover:bg-gray-400",
                    type="button",
                ),
                rx.el.button(
                    rx.cond(RouteState.selected_route, "Update Route", "Add Route"),
                    type="submit",
                    class_name="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600",
                ),
                class_name="flex justify-end space-x-2 mt-4",
            ),
            on_submit=RouteState.handle_submit,
            class_name="space-y-4",
        ),
        class_name="p-4 bg-white shadow-sm rounded-lg",
    )


def routes_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Manage Routes", class_name="text-xl font-bold"),
            rx.el.button(
                "Add New Route",
                on_click=RouteState.set_new_route,
                class_name="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600",
            ),
            class_name="flex justify-between items-center mb-4",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th("Name", class_name="px-4 py-2 text-left"),
                        rx.el.th("Start", class_name="px-4 py-2 text-left"),
                        rx.el.th("End", class_name="px-4 py-2 text-left"),
                        rx.el.th("Actions", class_name="px-4 py-2 text-right"),
                        class_name="bg-gray-50 border-b",
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        RouteState.routes,
                        lambda route: rx.el.tr(
                            rx.el.td(route["name"], class_name="px-4 py-2"),
                            rx.el.td(route["start_location"], class_name="px-4 py-2"),
                            rx.el.td(route["end_location"], class_name="px-4 py-2"),
                            rx.el.td(
                                rx.el.div(
                                    rx.el.button(
                                        "Edit",
                                        on_click=lambda: RouteState.select_route(route),
                                        class_name="text-blue-500 hover:underline mr-2",
                                    ),
                                    rx.el.button(
                                        "Delete",
                                        on_click=lambda: RouteState.delete_route(
                                            route["id"]
                                        ),
                                        class_name="text-red-500 hover:underline",
                                    ),
                                    class_name="flex justify-end",
                                )
                            ),
                            class_name="border-b hover:bg-gray-100",
                        ),
                    )
                ),
                class_name="w-full text-sm",
            ),
            class_name="overflow-y-auto border rounded-lg",
        ),
        class_name="p-4 bg-white shadow-sm rounded-lg",
    )


def routes_view() -> rx.Component:
    return rx.el.div(
        rx.cond(RouteState.is_editing, route_form(), routes_table()),
        class_name="p-6",
        on_mount=RouteState.fetch_routes,
    )