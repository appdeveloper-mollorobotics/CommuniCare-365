import reflex as rx
from app.states.subscriptions_state import SubscriptionsState


def subscriptions_table() -> rx.Component:
    return rx.el.div(
        rx.el.h1("Manage Subscriptions", class_name="text-2xl font-bold mb-4"),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th("ID", class_name="px-4 py-2"),
                        rx.el.th("User ID", class_name="px-4 py-2"),
                        rx.el.th("Plan", class_name="px-4 py-2"),
                        rx.el.th("Status", class_name="px-4 py-2"),
                        class_name="text-left bg-gray-50 border-b",
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        SubscriptionsState.subscriptions,
                        lambda sub: rx.el.tr(
                            rx.el.td(sub["id"], class_name="px-4 py-2"),
                            rx.el.td(sub["user_id"], class_name="px-4 py-2"),
                            rx.el.td(sub["plan"], class_name="px-4 py-2"),
                            rx.el.td(
                                rx.el.span(
                                    sub["status"],
                                    class_name=rx.cond(
                                        sub["status"] == "active",
                                        "px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800",
                                        "px-2 py-1 text-xs font-semibold rounded-full bg-red-100 text-red-800",
                                    ),
                                ),
                                class_name="px-4 py-2",
                            ),
                            class_name="border-b hover:bg-gray-50",
                        ),
                    )
                ),
                class_name="w-full text-sm",
            ),
            class_name="border rounded-lg overflow-hidden",
        ),
        class_name="p-6",
        on_mount=SubscriptionsState.fetch_subscriptions,
    )