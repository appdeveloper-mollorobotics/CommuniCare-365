import reflex as rx
from app.states.settings_state import SettingsState


def settings_view() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Application Settings"),
            rx.dialog.description(
                "Configure your database and service API keys here.", class_name="mb-4"
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.label("Database URL", class_name="text-sm font-medium"),
                    rx.el.input(
                        name="database_url",
                        default_value=SettingsState.database_url,
                        class_name="w-full p-2 border rounded-md mt-1 text-sm",
                        type="password",
                    ),
                    class_name="space-y-1",
                ),
                rx.el.div(
                    rx.el.label("Ably API Key", class_name="text-sm font-medium"),
                    rx.el.input(
                        name="ably_api_key",
                        default_value=SettingsState.ably_api_key,
                        class_name="w-full p-2 border rounded-md mt-1 text-sm",
                        type="password",
                    ),
                    class_name="space-y-1 mt-4",
                ),
                rx.el.div(
                    rx.dialog.close(
                        rx.el.button(
                            "Cancel",
                            type="button",
                            class_name="px-4 py-2 bg-gray-200 rounded-md text-sm",
                        )
                    ),
                    rx.el.button(
                        "Save Changes",
                        type="submit",
                        class_name="px-4 py-2 bg-blue-500 text-white rounded-md text-sm",
                    ),
                    class_name="flex justify-end space-x-2 mt-6",
                ),
                on_submit=SettingsState.save_settings,
                reset_on_submit=True,
            ),
        ),
        open=SettingsState.show_dialog,
        on_open_change=SettingsState.set_show_dialog,
    )