from .supabase import supabase
from dataclasses import dataclass
import json
import logging


@dataclass
class Report:
    """Structure of a scam report."""

    platform: str
    report_url: str
    screenshot_url: str
    poster_username: str
    post_description: str
    telegram_created_by: str


def create_report(report: Report):
    dump = json.dumps(report.__dict__)
    return supabase.table("report").insert(dump).execute()


def get_report(report_id: int) -> Report:
    return supabase.table("report").select("*").eq("id", report_id).execute()
