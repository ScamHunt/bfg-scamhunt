from .supabase import supabase
from postgrest import APIError
import logging
from datetime import datetime

from .report import Report


class User:
    def __init__(self, id: int, username: str, first_name: str, last_name: str):
        self.id = id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            username=data["username"],
            first_name=data["first_name"],
            last_name=data["last_name"],
        )

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }


def create_user(user: User) -> (User, Exception):
    new = user.to_dict()
    try:
        data = supabase.table("user").insert(new).execute()
        return (data.data[0], None)
    except APIError as e:
        logging.error(f"Error creating user: {e}")


def get_user(id: int) -> (User | None, Exception | None):
    try:
        data = supabase.table("user").select("*").eq("id", id).limit(1).execute()
        if not data.data:
            return (None, None)
        user_data = data.data[0]
        return (User.from_dict(user_data), None)
    except APIError as e:
        logging.error(f"Error getting user: {e}")
        return (None, e)


def get_user_reports(id: int) -> (list[Report], Exception):
    try:
        data = supabase.table("report").select("*").in_("user_id", [id]).execute()
        return (data.data, None)
    except APIError as e:
        logging.error(f"Error getting user reports: {e}")
        return (None, e)
