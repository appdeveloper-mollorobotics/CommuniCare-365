import reflex as rx
import reflex_enterprise as rxe
from reflex_enterprise.components.map.types import latlng
from app.states.ably_state import AblyState
from app.states.record_state import RecordState


def communicare_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2("Broadcast Vehicle Data", class_name="text-lg font-semibold"),
                rx.el.div(
                    rx.el.input(
                        on_change=AblyState.set_entry_1_text,
                        placeholder="Enter vehicle registration",
                        class_name="p-2 border rounded-md w-full",
                        default_value=AblyState.entry_1_text,
                    ),
                    rx.el.button(
                        ">>",
                        on_click=AblyState.broadcast_vehicle_data,
                        class_name="p-2 bg-blue-500 text-white rounded-md hover:bg-blue-600",
                    ),
                    rx.el.button(
                        "Import",
                        on_click=lambda: rx.toast.info(
                            "Import functionality not implemented."
                        ),
                        class_name="p-2 bg-gray-500 text-white rounded-md hover:bg-gray-600",
                    ),
                    class_name="flex items-center space-x-2",
                ),
                class_name="p-4 bg-white shadow-sm rounded-lg space-y-4",
            ),
            rx.el.div(
                rx.el.h2("Live Vehicle Data", class_name="text-lg font-semibold"),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Vehicle Registration", class_name="px-4 py-2"
                                ),
                                rx.el.th("Location", class_name="px-4 py-2"),
                                rx.el.th("Timestamp", class_name="px-4 py-2"),
                                class_name="text-left bg-gray-50 border-b",
                            )
                        ),
                        rx.el.tbody(
                            rx.foreach(
                                AblyState.vehicle_data,
                                lambda vehicle: rx.el.tr(
                                    rx.el.td(
                                        vehicle["vehicle_registration"],
                                        class_name="px-4 py-2",
                                    ),
                                    rx.el.td(
                                        f"{vehicle['latitude']}, {vehicle['longitude']}",
                                        class_name="px-4 py-2",
                                    ),
                                    rx.el.td(
                                        vehicle["timestamp"], class_name="px-4 py-2"
                                    ),
                                    on_click=lambda: RecordState.show_details(
                                        {
                                            "gps_location": f"{vehicle['latitude']},{vehicle['longitude']}",
                                            "vehicle_reg": vehicle[
                                                "vehicle_registration"
                                            ],
                                            "created_at": vehicle["timestamp"],
                                            "userid": 0,
                                            "username": "Live",
                                            "contact_number": "",
                                            "images": "[]",
                                        }
                                    ),
                                    class_name="cursor-pointer hover:bg-gray-100 border-b",
                                ),
                            )
                        ),
                        class_name="w-full text-sm",
                    ),
                    class_name="h-[300px] overflow-y-auto border rounded-lg",
                ),
                class_name="p-4 bg-white shadow-sm rounded-lg space-y-4",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-6",
        ),
        rx.el.div(
            rxe.map(
                rxe.map.tile_layer(
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                ),
                rx.foreach(
                    AblyState.vehicle_data,
                    lambda vehicle: rxe.map.marker(
                        position=latlng(
                            lat=vehicle["latitude"].to(float),
                            lng=vehicle["longitude"].to(float),
                        ),
                        content=rx.icon("map-pin", color="blue"),
                    ),
                ),
                rx.cond(
                    RecordState.trace_path.length() > 0,
                    rxe.map.polyline(
                        positions=RecordState.trace_path,
                        path_options=rxe.map.path_options(color="purple"),
                    ),
                    None,
                ),
                id="communicare-map-view",
                center=RecordState.map_center,
                zoom=RecordState.map_zoom,
                height="400px",
                width="100%",
                class_name="rounded-lg shadow-sm border mt-6",
            ),
            rx.el.div(
                rx.el.h3("Trace Vehicle Path", class_name="text-lg font-semibold"),
                rx.el.div(
                    rx.el.input(
                        placeholder="Enter vehicle registration to trace",
                        on_change=RecordState.set_trace_vehicle_reg,
                        class_name="p-2 border rounded-md w-full",
                    ),
                    rx.el.button(
                        "Trace",
                        on_click=RecordState.trace_vehicle,
                        class_name="p-2 bg-purple-500 text-white rounded-md hover:bg-purple-600",
                    ),
                    class_name="flex items-center space-x-2",
                ),
                class_name="p-4 bg-white shadow-sm rounded-lg space-y-4 mt-4",
            ),
        ),
        class_name="p-6",
        on_mount=AblyState.ably_monitor,
    )