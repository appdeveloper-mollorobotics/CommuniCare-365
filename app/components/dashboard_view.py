import reflex as rx
from app.states.auth_state import AuthState
from app.states.record_state import RecordState
from app.components.map_view import map_view
from app.components.record_table import record_table
from app.components.record_details import record_details
from app.components.routes_table import routes_table
from app.components.subscriptions_table import subscriptions_table
from app.components.communicare_view import communicare_view


def header_component() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("StaySecure Monitor 365", class_name="text-2xl font-bold"),
            rx.el.p(
                rx.el.span("Welcome, "),
                rx.el.span(AuthState.user_name, class_name="font-semibold"),
                class_name="text-gray-600",
            ),
        ),
        rx.el.button(
            "Log out",
            on_click=AuthState.logout,
            class_name="p-2 bg-red-500 text-white rounded-md hover:bg-red-600 text-sm font-semibold",
        ),
        class_name="flex items-center justify-between w-full p-4 border-b border-gray-200 bg-gray-50/50 backdrop-blur-sm sticky top-0 z-20",
    )


def tabs_component() -> rx.Component:
    tabs = ["Dashboard", "Manage Routes", "Manage Subscriptions", "CommuniCare (Unity)"]
    return rx.el.div(
        rx.foreach(
            tabs,
            lambda tab: rx.el.button(
                tab,
                on_click=lambda: RecordState.set_active_tab(tab),
                class_name=rx.cond(
                    RecordState.active_tab == tab,
                    "px-4 py-2 text-sm font-semibold text-white bg-blue-500 rounded-md shadow-sm",
                    "px-4 py-2 text-sm font-semibold text-gray-600 hover:bg-gray-200 rounded-md",
                ),
            ),
        ),
        class_name="flex space-x-2 p-4 border-b border-gray-200",
    )


def filter_controls() -> rx.Component:
    return rx.el.div(
        rx.el.select(
            rx.foreach(RecordState.usernames, lambda u: rx.el.option(u, value=u)),
            on_change=RecordState.set_selected_username,
            value=RecordState.selected_username,
            class_name="p-2 border rounded-md bg-white text-sm",
        ),
        rx.el.input(
            type="date",
            on_change=RecordState.set_start_date,
            class_name="p-2 border rounded-md bg-white text-sm",
        ),
        rx.el.input(
            type="date",
            on_change=RecordState.set_end_date,
            class_name="p-2 border rounded-md bg-white text-sm",
        ),
        class_name="flex items-center space-x-2 flex-wrap",
    )


def dashboard_tab_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            filter_controls(), class_name="p-4 border-b border-gray-200 bg-gray-50/50"
        ),
        rx.el.div(
            map_view(),
            rx.el.div(
                record_table(),
                record_details(),
                class_name="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6",
            ),
            class_name="p-6",
        ),
    )


def dashboard_view() -> rx.Component:
    return rx.el.div(
        header_component(),
        tabs_component(),
        rx.el.div(
            rx.match(
                RecordState.active_tab,
                ("Dashboard", dashboard_tab_content()),
                ("Manage Routes", routes_table()),
                ("Manage Subscriptions", subscriptions_table()),
                ("CommuniCare (Unity)", communicare_view()),
                dashboard_tab_content(),
            ),
            class_name="overflow-y-auto",
        ),
        class_name="w-full h-full grid grid-rows-[auto_auto_1fr]",
        on_mount=RecordState.fetch_records,
    )