import reflex as rx
from app.states.routes_state import RoutesState


def edit_route_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.el.div()),
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(RoutesState.editing_route, "Edit Route", "Add Route")
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.label("Set User ID", class_name="font-medium"),
                    rx.el.input(
                        name="setuserid",
                        default_value=rx.cond(
                            RoutesState.editing_route,
                            RoutesState.editing_route["setuserid"],
                            "",
                        ),
                        class_name="w-full p-2 border rounded-md",
                    ),
                    class_name="space-y-2",
                ),
                rx.el.div(
                    rx.el.label("Endpoint", class_name="font-medium"),
                    rx.el.input(
                        name="endpoint",
                        default_value=rx.cond(
                            RoutesState.editing_route,
                            RoutesState.editing_route["endpoint"],
                            "",
                        ),
                        class_name="w-full p-2 border rounded-md",
                    ),
                    class_name="space-y-2 mt-4",
                ),
                rx.el.div(
                    rx.el.label("Connection", class_name="font-medium"),
                    rx.el.select(
                        rx.foreach(
                            RoutesState.connection_options,
                            lambda option: rx.el.option(option, value=option),
                        ),
                        name="connection",
                        default_value=rx.cond(
                            RoutesState.editing_route,
                            RoutesState.editing_route["connection"],
                            "webhook",
                        ),
                        class_name="w-full p-2 border rounded-md bg-white",
                    ),
                    class_name="space-y-2 mt-4",
                ),
                rx.el.div(
                    rx.el.label("Optional", class_name="font-medium"),
                    rx.el.input(
                        name="optional",
                        default_value=rx.cond(
                            RoutesState.editing_route,
                            RoutesState.editing_route["optional"],
                            "",
                        ),
                        class_name="w-full p-2 border rounded-md",
                    ),
                    class_name="space-y-2 mt-4",
                ),
                rx.el.div(
                    rx.el.label("IMEI Number", class_name="font-medium"),
                    rx.el.input(
                        name="imei_number",
                        default_value=rx.cond(
                            RoutesState.editing_route,
                            RoutesState.editing_route["imei_number"],
                            "",
                        ),
                        class_name="w-full p-2 border rounded-md",
                    ),
                    class_name="space-y-2 mt-4",
                ),
                rx.el.div(
                    rx.dialog.close(
                        rx.el.button(
                            "Cancel",
                            type="button",
                            on_click=RoutesState.close_dialog,
                            class_name="px-4 py-2 bg-gray-200 rounded-md",
                        )
                    ),
                    rx.el.button(
                        "Save",
                        type="submit",
                        class_name="px-4 py-2 bg-blue-500 text-white rounded-md",
                    ),
                    class_name="flex justify-end space-x-2 mt-4",
                ),
                on_submit=RoutesState.save_route,
            ),
        ),
        open=RoutesState.show_edit_dialog,
    )


def routes_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Manage Routes", class_name="text-2xl font-bold"),
            rx.el.div(
                rx.el.input(
                    placeholder="Filter routes...",
                    on_change=RoutesState.set_filter_text,
                    class_name="p-2 border rounded-md",
                ),
                rx.el.button(
                    "Add Route",
                    on_click=RoutesState.open_add_dialog,
                    class_name="px-4 py-2 bg-green-500 text-white rounded-md",
                ),
                rx.el.button(
                    "Delete Selected",
                    on_click=RoutesState.delete_selected,
                    disabled=RoutesState.selected_routes.length() == 0,
                    class_name="px-4 py-2 bg-red-500 text-white rounded-md disabled:opacity-50",
                ),
                rx.el.button(
                    "Export CSV",
                    on_click=RoutesState.export_data,
                    class_name="px-4 py-2 bg-gray-600 text-white rounded-md",
                ),
                class_name="flex space-x-4",
            ),
            class_name="flex justify-between items-center mb-4",
        ),
        edit_route_dialog(),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            rx.el.input(
                                type="checkbox",
                                on_change=RoutesState.toggle_select_all,
                                checked=RoutesState.all_selected,
                            ),
                            class_name="px-4 py-2",
                        ),
                        rx.el.th("Set User ID", class_name="px-4 py-2"),
                        rx.el.th("Endpoint", class_name="px-4 py-2"),
                        rx.el.th("Connection", class_name="px-4 py-2"),
                        rx.el.th("Optional", class_name="px-4 py-2"),
                        rx.el.th("IMEI Number", class_name="px-4 py-2"),
                        rx.el.th("Actions", class_name="px-4 py-2"),
                        class_name="text-left bg-gray-50 border-b",
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        RoutesState.filtered_routes,
                        lambda route: rx.el.tr(
                            rx.el.td(
                                rx.el.input(
                                    type="checkbox",
                                    on_change=lambda checked: RoutesState.toggle_selection(
                                        route["endpoint"], checked
                                    ),
                                    checked=RoutesState.selected_routes.contains(
                                        route["endpoint"]
                                    ),
                                ),
                                class_name="px-4 py-2",
                            ),
                            rx.el.td(route["setuserid"], class_name="px-4 py-2"),
                            rx.el.td(route["endpoint"], class_name="px-4 py-2"),
                            rx.el.td(route["connection"], class_name="px-4 py-2"),
                            rx.el.td(route["optional"], class_name="px-4 py-2"),
                            rx.el.td(route["imei_number"], class_name="px-4 py-2"),
                            rx.el.td(
                                rx.el.div(
                                    rx.el.button(
                                        "Edit",
                                        on_click=lambda: RoutesState.open_edit_dialog(
                                            route
                                        ),
                                        class_name="text-blue-500 hover:underline text-sm font-medium",
                                    ),
                                    rx.el.button(
                                        "Delete",
                                        on_click=lambda: RoutesState.delete_route(
                                            route["endpoint"]
                                        ),
                                        class_name="text-red-500 hover:underline text-sm font-medium",
                                    ),
                                    class_name="flex space-x-2",
                                ),
                                class_name="px-4 py-2",
                            ),
                            class_name="border-b hover:bg-gray-50",
                        ),
                    )
                ),
                class_name="w-full text-sm",
            ),
            class_name="border rounded-lg overflow-hidden",
        ),
        class_name="p-6",
        on_mount=RoutesState.fetch_routes,
    )