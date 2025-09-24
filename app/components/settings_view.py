import reflex as rx
from app.states.settings_state import SettingsState


def settings_view() -> rx.Component:
    return rx.el.div(
        rx.el.h1("Settings", class_name="text-2xl font-bold mb-6"),
        rx.el.form(
            rx.el.div(
                rx.el.label("Database URL", class_name="font-medium"),
                rx.el.input(
                    name="database_url",
                    default_value=SettingsState.database_url,
                    class_name="w-full p-2 border rounded-md mt-1",
                ),
                class_name="space-y-2",
            ),
            rx.el.div(
                rx.el.label("Ably API Key", class_name="font-medium"),
                rx.el.input(
                    name="ably_api_key",
                    default_value=SettingsState.ably_api_key,
                    class_name="w-full p-2 border rounded-md mt-1",
                ),
                class_name="space-y-2 mt-4",
            ),
            rx.el.div(
                rx.el.button(
                    "Save",
                    type="submit",
                    class_name="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600",
                ),
                class_name="flex justify-end mt-6",
            ),
            on_submit=SettingsState.save_settings,
        ),
        class_name="p-6",
    )