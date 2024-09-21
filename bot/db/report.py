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


def create_report(report: Report):
    new = report.__dict__
    del new["id"]
    return supabase.table("report").insert(new).execute()


def get_report(report_id: int) -> Report:
    return supabase.table("report").select("*").eq("id", report_id).execute()
