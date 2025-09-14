import reflex as rx


class AuthState(rx.State):
    USER_DB: dict[str, str] = {"admin": "admin123", "user": "user123"}
    is_logged_in: bool = rx.LocalStorage(False, name="is_logged_in")
    user_name: str = rx.LocalStorage("", name="user_name")
    login_status: str = ""
    register_status: str = ""
    reset_status: str = ""

    @rx.event
    def login(self, form_data: dict):
        user = form_data["username"]
        pwd = form_data["password"]
        if self.USER_DB.get(user) == pwd:
            self.login_status = "✅ Login successful!"
            self.is_logged_in = True
            self.user_name = user
        else:
            self.login_status = "❌ Invalid username or password."

    @rx.event
    def register(self, form_data: dict):
        user = form_data["reg_username"]
        pwd = form_data["reg_password"]
        if not user or not pwd:
            self.register_status = "⚠️ Username and password required."
        elif user in self.USER_DB:
            self.register_status = "⚠️ Username already exists."
        else:
            self.USER_DB[user] = pwd
            self.register_status = "✅ Registered successfully."

    @rx.event
    def reset_password(self, form_data: dict):
        user = form_data["reset_username"]
        new_pwd = form_data["new_password"]
        if user not in self.USER_DB:
            self.reset_status = "❌ Username not found."
        elif not new_pwd:
            self.reset_status = "⚠️ New password cannot be empty."
        else:
            self.USER_DB[user] = new_pwd
            self.reset_status = "✅ Password reset successfully."

    @rx.event
    def logout(self):
        self.is_logged_in = False
        self.user_name = ""
        self.login_status = ""