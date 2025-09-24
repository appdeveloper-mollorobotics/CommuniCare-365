import reflex as rx
from app.states.settings_state import SettingsState
from app.states.auth_state import AuthState


def setting_input(
    label: str, name: str, value: rx.Var, is_password: rx.Var
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="text-sm font-medium"),
        rx.el.div(
            rx.el.input(
                name=name,
                default_value=value,
                class_name="w-full p-2 border rounded-md mt-1 text-sm pr-10",
                type=rx.cond(is_password, "password", "text"),
            ),
            rx.el.button(
                rx.icon(rx.cond(is_password, "eye-off", "eye"), size=16),
                on_click=SettingsState.toggle_show_password(name),
                class_name="absolute inset-y-0 right-0 px-3 flex items-center text-gray-500",
                type="button",
            ),
            class_name="relative",
        ),
        class_name="space-y-1 mt-4",
    )


def settings_view() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Application Settings"),
            rx.dialog.description(
                "Configure your application settings below.", class_name="mb-4"
            ),
            rx.el.h3("API & Database", class_name="text-lg font-semibold mt-4 mb-2"),
            rx.el.form(
                setting_input(
                    "Database URL",
                    "database_url",
                    SettingsState.database_url,
                    SettingsState.show_passwords["database_url"],
                ),
                setting_input(
                    "Ably API Key",
                    "ably_api_key",
                    SettingsState.ably_api_key,
                    SettingsState.show_passwords["ably_api_key"],
                ),
                setting_input(
                    "FastAPI Webhook URL",
                    "fastapi_webhook_url",
                    SettingsState.fastapi_webhook_url,
                    SettingsState.show_passwords["fastapi_webhook_url"],
                ),
                rx.el.div(
                    rx.el.button(
                        "Save",
                        type="submit",
                        class_name="px-4 py-2 bg-blue-500 text-white rounded-md text-sm",
                    ),
                    class_name="flex justify-end mt-4",
                ),
                on_submit=SettingsState.save_settings,
                reset_on_submit=True,
            ),
            rx.el.hr(class_name="my-6"),
            rx.el.h3("Security", class_name="text-lg font-semibold mb-2"),
            rx.el.form(
                rx.el.div(
                    rx.el.label("Current Password", class_name="text-sm font-medium"),
                    rx.el.input(
                        name="current_password",
                        type="password",
                        class_name="w-full p-2 border rounded-md mt-1 text-sm",
                        required=True,
                    ),
                    class_name="space-y-1 mt-4",
                ),
                rx.el.div(
                    rx.el.label("New Password", class_name="text-sm font-medium"),
                    rx.el.input(
                        name="new_password",
                        type="password",
                        class_name="w-full p-2 border rounded-md mt-1 text-sm",
                        required=True,
                    ),
                    class_name="space-y-1 mt-4",
                ),
                rx.el.div(
                    rx.el.button(
                        "Change Password",
                        type="submit",
                        class_name="px-4 py-2 bg-blue-500 text-white rounded-md text-sm",
                    ),
                    class_name="flex justify-end mt-4",
                ),
                on_submit=AuthState.change_password,
                reset_on_submit=True,
            ),
            rx.el.p(
                AuthState.change_password_status,
                class_name="text-sm text-center mt-2",
                color=rx.cond(
                    AuthState.change_password_status.contains("success"), "green", "red"
                ),
            ),
            rx.el.div(
                rx.dialog.close(
                    rx.el.button(
                        "Close",
                        type="button",
                        class_name="px-4 py-2 bg-gray-200 rounded-md text-sm w-full mt-6",
                    )
                )
            ),
        ),
        open=SettingsState.show_dialog,
        on_open_change=SettingsState.set_show_dialog,
    )