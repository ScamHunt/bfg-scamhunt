from .supabase import supabase
from postgrest import APIError
import logging
from datetime import datetime
from typing import Optional
from ..openai.ocr import ScamType, Screenshot


class Report:
    """Structure of a scam report."""

    def __init__(
        self,
        description: str,
        reasoning: str,
        scam_likelihood: int,
        is_advertisement: bool,
        is_sponsored: bool,
        is_photo: bool,
        is_video: bool,
        is_social_media_post: bool,
        created_by_tg_id: int,
        likes: int,
        comments: int,
        shares: int,
        scam_types: list[ScamType],
        links: list[str],
        phone_numbers: list[str],
        emails: list[str],
        id: Optional[int] = None,
        platform: Optional[str] = None,
        from_user: Optional[str] = None,
        to_user: Optional[str] = None,
        caption: Optional[str] = None,
        location: Optional[str] = None,
        report_url: Optional[str] = None,
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
        self.created_at = created_at
        self.scam_types = scam_types
        self.links = links
        self.phone_numbers = phone_numbers
        self.emails = emails
        self.likes = likes
        self.comments = comments
        self.shares = shares

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    @classmethod
    def from_screenshot(self, screenshot: Screenshot, created_by_tg_id: int):
        self.created_by_tg_id = created_by_tg_id
        for key, value in screenshot.dict().items():
            setattr(self, key, value)


def create_report(report: Report) -> (Report, Exception):
    new = report.__dict__
    del new["id"]
    try:
        data = supabase.table("report").insert(new).execute()
        return (data.data[0], None)
    except APIError as e:
        logging.error(f"Error creating report: {e}")
        return (None, e)


def get_report(report_id: int) -> (Report, Exception):
    try:
        data = (
            supabase.table("report")
            .select("*")
            .eq("id", report_id)
            .limit(1)
            .single()
            .execute()
        )
        return (Report.from_dict(data.data), None)
    except APIError as e:
        logging.error(f"Error getting report: {e}")
        return (None, e)
    except TypeError as e:
        logging.error(f"Error getting report: {e}")
        return (None, e)


def get_reports_by_user(user_id: int) -> (list[Report], Exception):
    try:
        data = (
            supabase.table("report")
            .select("*")
            .eq("created_by_tg_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )
        reports = [Report.from_dict(report) for report in data.data]
        return (reports, None)
    except APIError as e:
        logging.error(f"Error getting reports by user: {e}")
        return (None, e)
    except TypeError as e:
        logging.error(f"Error getting reports by user: {e}")
        return (None, e)
