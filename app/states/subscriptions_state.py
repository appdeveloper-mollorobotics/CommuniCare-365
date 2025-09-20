import reflex as rx
import pandas as pd
import sqlalchemy
import logging
from typing import TypedDict, Optional

DATABASE_URL = "postgresql://appdeveloper:GDwIvB9TEp1b9Y2LEJy31lds4Scga3ir@dpg-d1v92jje5dus739jbm4g-a.oregon-postgres.render.com/staysecure365_db"
engine = sqlalchemy.create_engine(DATABASE_URL)


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
    selected_subscriptions: set[int] = set()

    @rx.event
    async def fetch_subscriptions(self):
        try:
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
    def save_subscription(self, form_data: dict):
        user_id = form_data.get("user_id")
        if not user_id:
            return rx.toast.error("User ID is required.")
        is_valid = form_data.get("is_valid", False)
        is_fully_licensed = form_data.get("is_fully_licensed", False)
        if self.editing_subscription:
            sub_id = self.editing_subscription["id"]
            for i, sub in enumerate(self.subscriptions):
                if sub["id"] == sub_id:
                    self.subscriptions[i]["user_id"] = user_id
                    self.subscriptions[i]["is_valid"] = is_valid
                    self.subscriptions[i]["is_fully_licensed"] = is_fully_licensed
                    break
            yield rx.toast.success("Subscription updated successfully.")
        else:
            new_id = max([s["id"] for s in self.subscriptions] or [0]) + 1
            new_sub = {
                "id": new_id,
                "user_id": user_id,
                "is_valid": is_valid,
                "is_fully_licensed": is_fully_licensed,
            }
            self.subscriptions.append(new_sub)
            yield rx.toast.success("Subscription added successfully.")
        self._reset_edit_state()

    @rx.event
    def delete_subscription(self, sub_id: int):
        self.subscriptions = [s for s in self.subscriptions if s["id"] != sub_id]
        yield rx.toast.info("Subscription deleted.")

    @rx.event
    def toggle_selection(self, sub_id: int):
        if sub_id in self.selected_subscriptions:
            self.selected_subscriptions.remove(sub_id)
        else:
            self.selected_subscriptions.add(sub_id)

    @rx.var
    def all_selected(self) -> bool:
        return (
            len(self.selected_subscriptions) == len(self.filtered_subscriptions)
            and len(self.filtered_subscriptions) > 0
        )

    @rx.event
    def toggle_select_all(self):
        if self.all_selected:
            self.selected_subscriptions = set()
        else:
            self.selected_subscriptions = {
                sub["id"] for sub in self.filtered_subscriptions
            }

    @rx.event
    def delete_selected(self):
        deleted_count = len(self.selected_subscriptions)
        self.subscriptions = [
            s for s in self.subscriptions if s["id"] not in self.selected_subscriptions
        ]
        self.selected_subscriptions = set()
        yield rx.toast.info(f"Deleted {deleted_count} subscriptions.")

    @rx.event
    def export_data(self):
        df = pd.DataFrame(self.filtered_subscriptions)
        if df.empty:
            return rx.toast.warning("No data to export.")
        csv_data = df.to_csv(index=False)
        return rx.download(data=csv_data, filename="subscriptions.csv")