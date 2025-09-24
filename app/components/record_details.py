import reflex as rx
from app.states.record_state import RecordState


def detail_row(label: str, value: rx.Var) -> rx.Component:
    return rx.el.tr(
        rx.el.td(label, class_name="font-semibold px-4 py-2"),
        rx.el.td(value, class_name="px-4 py-2"),
        class_name="border-b",
    )


def record_details() -> rx.Component:
    return rx.el.div(
        rx.cond(
            RecordState.selected_record,
            rx.el.div(
                rx.el.div(
                    rx.el.h3("Record Details", class_name="text-xl font-bold"),
                    rx.el.div(
                        rx.el.a(
                            rx.icon("message-circle", size=20),
                            href=f"https://wa.me/{RecordState.selected_record['contact_number']}",
                            is_external=True,
                            class_name="p-1 text-green-600 hover:bg-gray-200 rounded-full",
                        ),
                        rx.el.button(
                            "Assign",
                            on_click=lambda: rx.toast.info(
                                "Assign functionality not implemented."
                            ),
                            class_name="px-3 py-1 bg-blue-500 text-white text-xs font-semibold rounded-md hover:bg-blue-600",
                        ),
                        class_name="flex items-center space-x-2",
                    ),
                    class_name="flex justify-between items-center mb-4",
                ),
                rx.el.table(
                    rx.el.tbody(
                        detail_row(
                            "Vehicle", RecordState.selected_record["vehicle_reg"]
                        ),
                        detail_row(
                            "Contact", RecordState.selected_record["contact_number"]
                        ),
                        detail_row("GPS", RecordState.selected_record["gps_location"]),
                        detail_row(
                            "Timestamp", RecordState.selected_record["created_at"]
                        ),
                    ),
                    class_name="w-full text-sm table-fixed",
                ),
                rx.el.hr(class_name="my-4"),
                rx.el.h4("Images", class_name="font-semibold text-md mb-2"),
                rx.el.div(
                    rx.foreach(
                        RecordState.image_urls,
                        lambda img_url: rx.image(
                            src=img_url,
                            class_name="w-full h-auto object-cover rounded-md border",
                        ),
                    ),
                    class_name="grid grid-cols-2 md:grid-cols-3 gap-2",
                ),
            ),
            rx.el.div(
                rx.el.p("Select a record to see details.", class_name="text-gray-500"),
                class_name="flex items-center justify-center h-full",
            ),
        ),
        class_name="p-4 bg-white shadow-sm rounded-lg h-full",
    )