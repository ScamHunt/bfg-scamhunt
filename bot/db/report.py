from .supabase import supabase
from postgrest import APIError
import logging
from datetime import datetime
from typing import Optional
from datetime import datetime
from ..openai.ocr import ScamType, Screenshot, Platform

supabase = supabase.schema('public')

class Report:
    """Structure of a scam report."""

    def __init__(
        self,
        platform: Platform,
        is_advertisement: bool,
        is_sponsored: bool,
        is_photo: bool,
        is_video: bool,
        is_social_media_post: bool,
        created_by_tg_id: int,
        emails: list[str] = [],
        phone_numbers: list[str] = [],
        likes: int = 0,
        comments: int = 0,
        shares: int = 0,
        links: list[str] = [],
        scam_types: list[ScamType] = [],
        id: Optional[int] = None,
        reasoning: Optional[str] = None,
        description: Optional[str] = None,
        scam_likelihood: Optional[int] = None,
        from_user: Optional[str] = None,
        to_user: Optional[str] = None,
        caption: Optional[str] = None,
        location: Optional[str] = None,
        report_url: Optional[str] = None,
        correctness: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = id  # Let the database handle auto-increment
        self.platform = platform
        self.from_user = from_user
        self.to_user = to_user
        self.caption = caption
        self.location = location
        self.report_url = report_url
        self.description = description
        self.reasoning = reasoning
        self.scam_likelihood = scam_likelihood
        self.is_advertisement = is_advertisement
        self.is_sponsored = is_sponsored
        self.is_photo = is_photo
        self.is_video = is_video
        self.is_social_media_post = is_social_media_post
        self.created_by_tg_id = created_by_tg_id
        self.scam_types = scam_types
        self.links = links
        self.phone_numbers = phone_numbers
        self.emails = emails
        self.likes = likes
        self.comments = comments
        self.shares = shares
        self.correctness = correctness
        self.created_at = created_at

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    @classmethod
    def from_screenshot(cls, screenshot: Screenshot, created_by_tg_id: int):
        cls.created_by_tg_id = created_by_tg_id
        for key, value in screenshot.model_dump().items():
            setattr(cls, key, value)
        return cls

    @classmethod
    def to_dict(cls):
        new = cls.__dict__.copy()
        return new

def create_report(report: Report) -> Report:
    new = report.__dict__.copy()
    del new["id"]
    del new["created_at"]
    try:
        data = supabase.table("report").insert(new).execute()
        return Report.from_dict(data.data[0])
    except APIError as e:
        logging.error(f"Error creating report: {e}")
        raise e


def get_report(report_id: int) -> Report:
    try:
        data = (
            supabase.table("report")
            .select("*")
            .eq("id", report_id)
            .limit(1)
            .single()
            .execute()
        )
        return Report.from_dict(data.data)
    except APIError as e:
        logging.error(f"Error getting report: {e}")
    except TypeError as e:
        logging.error(f"Error getting report: {e}")


def get_reports_by_user(user_id: int) -> list[Report]:
    try:
        data = (
            supabase.table("report")
            .select("*")
            .eq("created_by_tg_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )
        reports = [Report.from_dict(report) for report in data.data]
        return reports
    except APIError as e:
        logging.error(f"Error getting reports by user: {e}")
    except TypeError as e:
        logging.error(f"Error getting reports by user: {e}")

def get_leaderboard():
    try:
        data = (
            supabase.table("report")
            .select("created_by_tg_id, created_by_tg_id.count()")
            .execute()
        )
        leaderboard = sorted(data.data, key=lambda x: x["count"], reverse=True)
        formatted_leaderboard = [{"user_id": entry["created_by_tg_id"], "report_count": entry["count"]} for entry in leaderboard]
        logging.info("Leaderboard data fetched successfully")
        return formatted_leaderboard
    except APIError as e:
        logging.error(f"Error getting leaderboard: {e}")
    except TypeError as e:
        logging.error(f"Error getting leaderboard: {e}")
        
def update_report_correctness(report_id: int, correctness: str):
    try:
        supabase.table("report").update({"correctness": correctness}).eq(
            "id", report_id
        ).execute()
    except APIError as e:
        logging.error(f"Error updating report correctness: {e}")
