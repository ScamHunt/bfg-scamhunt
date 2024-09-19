from .supabase import supabase
from dataclasses import dataclass
import json
import logging


@dataclass
class Report:
    """Structure of a scam report."""

    platform: str
    url: str
    screenshot_url: str
    poster_username: str
    post_description: str
    telegram_created_by: str


def create_report(report: Report):
    dump = json.dumps(report.__dict__)
    return supabase.table("report").insert(dump).execute()
