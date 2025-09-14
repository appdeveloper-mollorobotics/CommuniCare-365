import reflex as rx
from app.states.record_state import RecordState


def record_details() -> rx.Component:
    return rx.cond(
        RecordState.selected_record,
        rx.el.div(
            rx.el.h3("Record Details", class_name="text-xl font-bold mb-2"),
            rx.el.p(f"Vehicle: {RecordState.selected_record['vehicle_reg']}"),
            rx.el.p(f"Contact: {RecordState.selected_record['contact_number']}"),
            rx.el.p(f"GPS: {RecordState.selected_record['gps_location']}"),
            rx.el.p(f"Timestamp: {RecordState.selected_record['created_at']}"),
            rx.el.h4("Images", class_name="font-semibold mt-4"),
            rx.foreach(
                RecordState.image_urls,
                lambda img_url: rx.image(
                    src=img_url,
                    width=150,
                    fit="contain",
                    class_name="border rounded-md",
                ),
            ),
            class_name="p-4 border rounded-lg bg-white shadow-sm",
        ),
        rx.el.div(
            rx.el.p("Select a record to see details.", class_name="text-gray-500"),
            class_name="flex items-center justify-center h-full p-4 border rounded-lg bg-white shadow-sm",
        ),
    )