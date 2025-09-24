import reflex as rx
import pandas as pd
import sqlalchemy
import logging
from typing import TypedDict, Optional
from app.states.settings_state import SettingsState


class Subscription(TypedDict):
    id: int
    user_id: str
    is_valid: bool
    is_fully_licensed: bool


class SubscriptionsState(rx.State):
    subscriptions: list[Subscription] = []
    filter_user_id: str = ""
    show_edit_dialog: bool = False
    editing_subscription: Optional[Subscription] = None
    selected_subscriptions: list[int] = []

    async def _get_engine(self):
        settings_state = await self.get_state(SettingsState)
        return sqlalchemy.create_engine(settings_state.database_url)

    @rx.event
    async def fetch_subscriptions(self):
        try:
            engine = await self._get_engine()
            with engine.connect() as conn:
                df = pd.read_sql("SELECT * FROM subscriptions", conn)
                if "is_valid" in df.columns:
                    df["is_valid"] = df["is_valid"].astype(bool)
                if "is_fully_licensed" in df.columns:
                    df["is_fully_licensed"] = df["is_fully_licensed"].astype(bool)
            self.subscriptions = df.to_dict("records")
        except Exception as e:
            logging.exception(f"Error fetching subscriptions: {e}")
            self.subscriptions = []

    @rx.var
    def filtered_subscriptions(self) -> list[Subscription]:
        if not self.filter_user_id:
            return self.subscriptions
        return [
            s
            for s in self.subscriptions
            if self.filter_user_id.lower() in s["user_id"].lower()
        ]

    def _reset_edit_state(self):
        self.show_edit_dialog = False
        self.editing_subscription = None

    @rx.event
    def open_add_dialog(self):
        self.editing_subscription = None
        self.show_edit_dialog = True

    @rx.event
    def open_edit_dialog(self, subscription: Subscription):
        self.editing_subscription = subscription
        self.show_edit_dialog = True

    @rx.event
    def close_dialog(self):
        self._reset_edit_state()

    @rx.event
    async def save_subscription(self, form_data: dict):
        user_id = form_data.get("user_id")
        if not user_id:
            yield rx.toast.error("User ID is required.")
            return
        is_valid = form_data.get("is_valid", False)
        is_fully_licensed = form_data.get("is_fully_licensed", False)
        try:
            engine = await self._get_engine()
            with engine.connect() as conn:
                if self.editing_subscription:
                    sub_id = self.editing_subscription["id"]
                    stmt = sqlalchemy.text(
                        "UPDATE subscriptions SET user_id = :user_id, is_valid = :is_valid, is_fully_licensed = :is_fully_licensed WHERE id = :id"
                    )
                    conn.execute(
                        stmt,
                        parameters={
                            "user_id": user_id,
                            "is_valid": is_valid,
                            "is_fully_licensed": is_fully_licensed,
                            "id": sub_id,
                        },
                    )
                    conn.commit()
                    yield rx.toast.success("Subscription updated successfully.")
                else:
                    stmt = sqlalchemy.text(
                        "INSERT INTO subscriptions (user_id, is_valid, is_fully_licensed) VALUES (:user_id, :is_valid, :is_fully_licensed)"
                    )
                    conn.execute(
                        stmt,
                        parameters={
                            "user_id": user_id,
                            "is_valid": is_valid,
                            "is_fully_licensed": is_fully_licensed,
                        },
                    )
                    conn.commit()
                    yield rx.toast.success("Subscription added successfully.")
        except Exception as e:
            logging.exception(f"Error saving subscription: {e}")
            yield rx.toast.error("Failed to save subscription.")
        self._reset_edit_state()
        yield SubscriptionsState.fetch_subscriptions

    @rx.event
    async def delete_subscription(self, sub_id: int):
        try:
            engine = await self._get_engine()
            with engine.connect() as conn:
                stmt = sqlalchemy.text("DELETE FROM subscriptions WHERE id = :id")
                conn.execute(stmt, parameters={"id": sub_id})
                conn.commit()
        except Exception as e:
            logging.exception(f"Error deleting subscription: {e}")
            yield rx.toast.error("Failed to delete subscription.")
            return
        self.subscriptions = [s for s in self.subscriptions if s["id"] != sub_id]
        yield rx.toast.info("Subscription deleted.")

    @rx.event
    def toggle_selection(self, sub_id: int, checked: bool):
        current_list = list(self.selected_subscriptions)
        if checked:
            if sub_id not in current_list:
                current_list.append(sub_id)
        elif sub_id in current_list:
            current_list.remove(sub_id)
        self.selected_subscriptions = current_list

    @rx.var
    def all_selected(self) -> bool:
        return (
            len(self.selected_subscriptions) == len(self.filtered_subscriptions)
            and len(self.filtered_subscriptions) > 0
        )

    @rx.event
    def toggle_select_all(self, checked: bool):
        if checked:
            self.selected_subscriptions = [
                sub["id"] for sub in self.filtered_subscriptions
            ]
        else:
            self.selected_subscriptions = []

    @rx.event
    async def delete_selected(self):
        if not self.selected_subscriptions:
            return
        deleted_count = len(self.selected_subscriptions)
        try:
            engine = await self._get_engine()
            with engine.connect() as conn:
                stmt = sqlalchemy.text("DELETE FROM subscriptions WHERE id = ANY(:ids)")
                conn.execute(stmt, parameters={"ids": self.selected_subscriptions})
                conn.commit()
        except Exception as e:
            logging.exception(f"Error deleting selected subscriptions: {e}")
            yield rx.toast.error("Failed to delete subscriptions.")
            return
        self.subscriptions = [
            s for s in self.subscriptions if s["id"] not in self.selected_subscriptions
        ]
        self.selected_subscriptions = []
        yield rx.toast.info(f"Deleted {deleted_count} subscriptions.")

    @rx.event
    def export_data(self):
        df = pd.DataFrame(self.filtered_subscriptions)
        if df.empty:
            return rx.toast.warning("No data to export.")
        csv_data = df.to_csv(index=False)
        return rx.download(data=csv_data, filename="subscriptions.csv")