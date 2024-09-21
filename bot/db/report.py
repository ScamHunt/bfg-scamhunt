from .supabase import supabase
from dataclasses import dataclass
import json
import logging
from typing import Optional


@dataclass
class Report:
    """Structure of a scam report."""

    platform: str
    poster_username: str
    post_description: str
    telegram_created_by: str
    id: int = 0
    report_url: Optional[str] = None
    screenshot_url: Optional[str] = None


def create_report(report: Report) -> (Report, Exception):
    new = report.__dict__
    del new["id"]
    try:
        data = supabase.table("report").insert(new).execute()
        return (data.data, None)
    except APIError as e:
        logging.error(f"Error creating report: {e}")
        (None, e)



def get_report(report_id: int) -> Report:
    return supabase.table("report").select("*").eq("id", report_id).execute()
