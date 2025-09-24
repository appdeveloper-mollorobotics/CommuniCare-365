import reflex as rx
import reflex_enterprise as rxe
from app.components.auth_sidebar import auth_sidebar
from app.components.dashboard_view import dashboard_view
from app.states.auth_state import AuthState


def index() -> rx.Component:
    return rx.el.div(
        rx.image(
            src="/nice_background_dashboard.png",
            class_name="absolute inset-0 w-full h-full object-cover opacity-10 z-0",
        ),
        rx.el.div(
            rx.cond(
                AuthState.is_logged_in,
                dashboard_view(),
                rx.el.div(
                    auth_sidebar(),
                    class_name="flex items-center justify-center h-full w-full",
                ),
            ),
            class_name="relative z-10 w-screen h-screen",
        ),
        class_name="font-['Inter'] bg-gray-50 relative",
    )


app = rxe.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, title="CommuniCare EcoSystem 365°")