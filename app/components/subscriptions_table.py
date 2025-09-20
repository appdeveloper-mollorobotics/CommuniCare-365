import reflex as rx
from app.states.subscriptions_state import SubscriptionsState, Subscription


def edit_subscription_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.el.div()),
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(
                    SubscriptionsState.editing_subscription,
                    "Edit Subscription",
                    "Add Subscription",
                )
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.label("User ID", class_name="font-medium"),
                    rx.el.input(
                        name="user_id",
                        default_value=rx.cond(
                            SubscriptionsState.editing_subscription,
                            SubscriptionsState.editing_subscription["user_id"],
                            "",
                        ),
                        class_name="w-full p-2 border rounded-md",
                    ),
                    class_name="space-y-2",
                ),
                rx.el.div(
                    rx.el.label(
                        rx.el.input(
                            type="checkbox",
                            name="is_valid",
                            default_checked=rx.cond(
                                SubscriptionsState.editing_subscription,
                                SubscriptionsState.editing_subscription["is_valid"],
                                False,
                            ),
                        ),
                        " Is Valid",
                        class_name="flex items-center space-x-2",
                    ),
                    rx.el.label(
                        rx.el.input(
                            type="checkbox",
                            name="is_fully_licensed",
                            default_checked=rx.cond(
                                SubscriptionsState.editing_subscription,
                                SubscriptionsState.editing_subscription[
                                    "is_fully_licensed"
                                ],
                                False,
                            ),
                        ),
                        " Is Fully Licensed",
                        class_name="flex items-center space-x-2",
                    ),
                    class_name="flex space-x-4 mt-4",
                ),
                rx.el.div(
                    rx.dialog.close(
                        rx.el.button(
                            "Cancel",
                            type="button",
                            on_click=SubscriptionsState.close_dialog,
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
                on_submit=SubscriptionsState.save_subscription,
            ),
        ),
        open=SubscriptionsState.show_edit_dialog,
    )


def subscriptions_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Manage Subscriptions", class_name="text-2xl font-bold"),
            rx.el.div(
                rx.el.input(
                    placeholder="Filter by User ID...",
                    on_change=SubscriptionsState.set_filter_user_id,
                    class_name="p-2 border rounded-md",
                ),
                rx.el.button(
                    "Add Subscription",
                    on_click=SubscriptionsState.open_add_dialog,
                    class_name="px-4 py-2 bg-green-500 text-white rounded-md",
                ),
                rx.el.button(
                    "Delete Selected",
                    on_click=SubscriptionsState.delete_selected,
                    is_disabled=SubscriptionsState.selected_subscriptions.length() == 0,
                    class_name="px-4 py-2 bg-red-500 text-white rounded-md disabled:opacity-50",
                ),
                rx.el.button(
                    "Export CSV",
                    on_click=SubscriptionsState.export_data,
                    class_name="px-4 py-2 bg-gray-600 text-white rounded-md",
                ),
                class_name="flex space-x-4",
            ),
            class_name="flex justify-between items-center mb-4",
        ),
        edit_subscription_dialog(),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            rx.el.input(
                                type="checkbox",
                                on_change=SubscriptionsState.toggle_select_all,
                                checked=SubscriptionsState.all_selected,
                            ),
                            class_name="px-4 py-2",
                        ),
                        rx.el.th("User ID", class_name="px-4 py-2"),
                        rx.el.th("Is Valid", class_name="px-4 py-2"),
                        rx.el.th("Fully Licensed", class_name="px-4 py-2"),
                        rx.el.th("Actions", class_name="px-4 py-2"),
                        class_name="text-left bg-gray-50 border-b",
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        SubscriptionsState.filtered_subscriptions,
                        lambda sub: rx.el.tr(
                            rx.el.td(
                                rx.el.input(
                                    type="checkbox",
                                    on_change=lambda: SubscriptionsState.toggle_selection(
                                        sub["id"]
                                    ),
                                    checked=SubscriptionsState.selected_subscriptions.contains(
                                        sub["id"]
                                    ),
                                ),
                                class_name="px-4 py-2",
                            ),
                            rx.el.td(sub["user_id"], class_name="px-4 py-2"),
                            rx.el.td(
                                rx.icon(
                                    rx.cond(
                                        sub["is_valid"], "check-circle", "x-circle"
                                    ),
                                    color=rx.cond(sub["is_valid"], "green", "red"),
                                ),
                                class_name="px-4 py-2",
                            ),
                            rx.el.td(
                                rx.icon(
                                    rx.cond(
                                        sub["is_fully_licensed"],
                                        "check-circle",
                                        "x-circle",
                                    ),
                                    color=rx.cond(
                                        sub["is_fully_licensed"], "green", "red"
                                    ),
                                ),
                                class_name="px-4 py-2",
                            ),
                            rx.el.td(
                                rx.el.div(
                                    rx.el.button(
                                        "Edit",
                                        on_click=lambda: SubscriptionsState.open_edit_dialog(
                                            sub
                                        ),
                                        class_name="text-blue-500 hover:underline text-sm font-medium",
                                    ),
                                    rx.el.button(
                                        "Delete",
                                        on_click=lambda: SubscriptionsState.delete_subscription(
                                            sub["id"]
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
        on_mount=SubscriptionsState.fetch_subscriptions,
    )