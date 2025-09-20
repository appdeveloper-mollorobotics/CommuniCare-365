import reflex as rx
from app.states.record_state import RecordState


def record_table() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Records", class_name="text-xl font-bold mb-4"),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th("UserID", class_name="px-4 py-2"),
                        rx.el.th("Username", class_name="px-4 py-2"),
                        rx.el.th("Vehicle", class_name="px-4 py-2"),
                        rx.el.th("Created", class_name="px-4 py-2"),
                        class_name="text-left bg-gray-50 border-b",
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        RecordState.filtered_records,
                        lambda record: rx.el.tr(
                            rx.el.td(record["userid"], class_name="px-4 py-2"),
                            rx.el.td(record["username"], class_name="px-4 py-2"),
                            rx.el.td(record["vehicle_reg"], class_name="px-4 py-2"),
                            rx.el.td(record["created_at"], class_name="px-4 py-2"),
                            on_click=lambda: RecordState.show_details(record),
                            class_name="cursor-pointer hover:bg-gray-100 border-b",
                        ),
                    )
                ),
                class_name="w-full text-sm",
            ),
            class_name="h-[400px] overflow-y-auto border rounded-lg",
        ),
        class_name="p-4 bg-white shadow-sm rounded-lg",
    )