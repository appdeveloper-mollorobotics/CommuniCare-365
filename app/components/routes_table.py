import reflex as rx
from app.states.routes_state import RoutesState


def routes_table() -> rx.Component:
    return rx.el.div(
        rx.el.h1("Manage Routes", class_name="text-2xl font-bold mb-4"),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th("Set User ID", class_name="px-4 py-2"),
                        rx.el.th("Endpoint", class_name="px-4 py-2"),
                        rx.el.th("Connection", class_name="px-4 py-2"),
                        class_name="text-left bg-gray-50 border-b",
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        RoutesState.routes,
                        lambda route: rx.el.tr(
                            rx.el.td(route["setuserid"], class_name="px-4 py-2"),
                            rx.el.td(route["endpoint"], class_name="px-4 py-2"),
                            rx.el.td(route["connection"], class_name="px-4 py-2"),
                            class_name="border-b hover:bg-gray-50",
                        ),
                    )
                ),
                class_name="w-full text-sm",
            ),
            class_name="border rounded-lg overflow-hidden",
        ),
        class_name="p-6",
        on_mount=RoutesState.fetch_routes,
    )