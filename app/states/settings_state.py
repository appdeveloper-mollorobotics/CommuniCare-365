import reflex as rx


class SettingsState(rx.State):
    database_url: str = rx.LocalStorage(
        "postgresql://appdeveloper:GDwIvB9TEp1b9Y2LEJy31lds4Scga3ir@dpg-d1v92jje5dus739jbm4g-a.oregon-postgres.render.com/staysecure365_db",
        name="database_url",
    )
    ably_api_key: str = rx.LocalStorage(
        "pFIw1g.499zGg:nKBRLfocPzJeIA_Uwe7vXw5MbPsnj7EB1dk3P8X4WsQ", name="ably_api_key"
    )
    show_dialog: bool = False

    @rx.event
    def save_settings(self, form_data: dict):
        self.database_url = form_data["database_url"]
        self.ably_api_key = form_data["ably_api_key"]
        self.show_dialog = False
        return rx.toast.success("Settings saved successfully!")

    @rx.event
    def toggle_show_dialog(self):
        self.show_dialog = not self.show_dialog