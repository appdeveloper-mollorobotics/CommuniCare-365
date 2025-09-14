import reflex as rx
import reflex_enterprise as rxe
from app.states.record_state import RecordState


def map_view() -> rx.Component:
    return rxe.map(
        rxe.map.tile_layer(url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"),
        rx.foreach(RecordState.map_markers, lambda marker: marker),
        id="map-view",
        center=RecordState.map_center,
        zoom=RecordState.map_zoom,
        height="400px",
        width="100%",
        class_name="rounded-lg shadow-sm border",
    )