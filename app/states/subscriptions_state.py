import reflex as rx
import pandas as pd
import sqlalchemy
import logging
from typing import TypedDict

DATABASE_URL = "postgresql://appdeveloper:GDwIvB9TEp1b9Y2LEJy31lds4Scga3ir@dpg-d1v92jje5dus739jbm4g-a.oregon-postgres.render.com/staysecure365_db"
engine = sqlalchemy.create_engine(DATABASE_URL)


class Subscription(TypedDict):
    id: int
    user_id: str
    plan: str
    status: str


class SubscriptionsState(rx.State):
    subscriptions: list[Subscription] = []

    @rx.event
    async def fetch_subscriptions(self):
        try:
            with engine.connect() as conn:
                df = pd.read_sql("SELECT * FROM subscriptions", conn)
            self.subscriptions = df.to_dict("records")
        except Exception as e:
            logging.exception(f"Error fetching subscriptions: {e}")
            self.subscriptions = []