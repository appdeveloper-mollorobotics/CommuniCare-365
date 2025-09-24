import reflex as rx


class SettingsState(rx.State):
    database_url: str = rx.LocalStorage(
        "postgresql://appdeveloper:GDwIvB9TEp1b9Y2LEJy31lds4Scga3ir@dpg-d1v92jje5dus739jbm4g-a.oregon-postgres.render.com/staysecure365_db",
        name="database_url",
    )
    ably_api_key: str = rx.LocalStorage(
        "pFIw1g.499zGg:nKBRLfocPzJeIA_Uwe7vXw5MbPsnj7EB1dk3P8X4WsQ", name="ably_api_key"
    )
    fastapi_webhook_url: str = rx.LocalStorage("", name="fastapi_webhook_url")
    show_dialog: bool = False
    show_passwords: dict[str, bool] = {
        "database_url": True,
        "ably_api_key": True,
        "fastapi_webhook_url": True,
    }

    @rx.event
    def save_settings(self, form_data: dict):
        self.database_url = form_data["database_url"]
        self.ably_api_key = form_data["ably_api_key"]
        self.fastapi_webhook_url = form_data["fastapi_webhook_url"]
        return rx.toast.success("Settings saved successfully!")

    @rx.event
    def toggle_show_dialog(self):
        self.show_dialog = not self.show_dialog

    def toggle_show_password(self, field_name: str):
        self.show_passwords[field_name] = not self.show_passwords[field_name]