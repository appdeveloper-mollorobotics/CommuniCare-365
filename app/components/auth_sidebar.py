import reflex as rx
from app.states.auth_state import AuthState


def auth_sidebar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "🔐 StaySecure Monitor 365", class_name="text-2xl font-bold text-center"
            ),
            rx.el.p(
                "Please log in to continue",
                class_name="text-sm text-gray-500 text-center",
            ),
            class_name="space-y-1",
        ),
        rx.el.div(
            rx.el.form(
                rx.el.input(
                    placeholder="Username",
                    name="username",
                    class_name="w-full p-2 border border-gray-300 rounded-md",
                ),
                rx.el.input(
                    placeholder="Password",
                    name="password",
                    type="password",
                    class_name="w-full p-2 border border-gray-300 rounded-md",
                ),
                rx.el.button(
                    "Log in",
                    type="submit",
                    class_name="w-full p-2 bg-blue-500 text-white rounded-md hover:bg-blue-600",
                ),
                rx.el.p(
                    AuthState.login_status,
                    class_name="text-sm text-center",
                    text_color=rx.cond(
                        AuthState.login_status.contains("succe"), "green", "red"
                    ),
                ),
                on_submit=AuthState.login,
                class_name="space-y-4",
            ),
            rx.el.div(
                rx.el.details(
                    rx.el.summary(
                        "Need an account or to reset password?",
                        class_name="cursor-pointer text-sm text-gray-600 hover:text-black font-medium",
                    ),
                    rx.el.div(
                        rx.el.hr(class_name="my-4"),
                        rx.el.h3("Register New User", class_name="font-semibold"),
                        rx.el.form(
                            rx.el.input(
                                placeholder="New Username",
                                name="reg_username",
                                class_name="w-full p-2 border border-gray-300 rounded-md",
                            ),
                            rx.el.input(
                                placeholder="New Password",
                                name="reg_password",
                                type="password",
                                class_name="w-full p-2 border border-gray-300 rounded-md",
                            ),
                            rx.el.button(
                                "Register",
                                type="submit",
                                class_name="w-full p-2 bg-gray-600 text-white rounded-md hover:bg-gray-700",
                            ),
                            rx.el.p(
                                AuthState.register_status,
                                class_name="text-sm text-center",
                                text_color=rx.cond(
                                    AuthState.register_status.contains("succe"),
                                    "green",
                                    "red",
                                ),
                            ),
                            on_submit=AuthState.register,
                            class_name="space-y-3 mt-2",
                        ),
                        rx.el.hr(class_name="my-4"),
                        rx.el.h3("Reset Password", class_name="font-semibold"),
                        rx.el.form(
                            rx.el.input(
                                placeholder="Username",
                                name="reset_username",
                                class_name="w-full p-2 border border-gray-300 rounded-md",
                            ),
                            rx.el.input(
                                placeholder="New Password",
                                name="new_password",
                                type="password",
                                class_name="w-full p-2 border border-gray-300 rounded-md",
                            ),
                            rx.el.button(
                                "Reset Password",
                                type="submit",
                                class_name="w-full p-2 bg-gray-600 text-white rounded-md hover:bg-gray-700",
                            ),
                            rx.el.p(
                                AuthState.reset_status,
                                class_name="text-sm text-center",
                                text_color=rx.cond(
                                    AuthState.reset_status.contains("succe"),
                                    "green",
                                    "red",
                                ),
                            ),
                            on_submit=AuthState.reset_password,
                            class_name="space-y-3 mt-2",
                        ),
                        class_name="mt-4",
                    ),
                ),
                class_name="text-center mt-4",
            ),
            class_name="space-y-4",
        ),
        class_name="p-8 w-96 max-w-md bg-white border border-gray-200 shadow-md rounded-xl space-y-6",
    )