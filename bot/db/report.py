from .supabase import supabase
from dataclasses import dataclass
import json
import logging
from typing import Optional
from ..openai.ocr import ScamType, Screenshot


class Report:
    """Structure of a scam report."""

    def __init__(
        self,
        id: Optional[int],
        platform: Optional[str],
        from_user: Optional[str],
        to_user: Optional[str],
        caption: Optional[str],
        location: Optional[str],
        ai_description: str,
        reasoning: str,
        scam_likelihood: int,
        is_advertisement: bool,
        is_sponsored: bool,
        is_photo: bool,
        is_video: bool,
        created_by_tg_id: int,
        scam_types: list[ScamType],
        links: list[str] = [],
        phone_numbers: list[str] = [],
        emails: list[str] = [],
        likes: int = 0,
        comments: int = 0,
        shares: int = 0,
    ):
        self.id = id
        self.platform = platform
        self.from_user = from_user
        self.to_user = to_user
        self.caption = caption
        self.location = location
        self.ai_description = ai_description
        self.reasoning = reasoning
        self.scam_likelihood = scam_likelihood
        self.is_advertisement = is_advertisement
        self.is_sponsored = is_sponsored
        self.is_photo = is_photo
        self.is_video = is_video
        self.created_by_tg_id = created_by_tg_id
        self.scam_types = scam_types
        self.links = links
        self.phone_numbers = phone_numbers
        self.emails = emails
        self.likes = likes
        self.comments = comments
        self.shares = shares

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __init__(
        self, screenshot: Screenshot, created_by_tg_id: int
    ):
        self.created_by_tg_id = created_by_tg_id

        self.platform = screenshot.platform
        self.from_user = screenshot.from_user
        self.to_user = screenshot.to_user
        self.caption = screenshot.caption
        self.location = screenshot.location
        self.ai_description = screenshot.description
        self.reasoning = screenshot.reasoning
        self.scam_likelihood = screenshot.scam_likelihood
        self.is_advertisement = screenshot.is_advertisement
        self.is_sponsored = screenshot.is_sponsored
        self.is_photo = screenshot.is_photo
        self.is_video = screenshot.is_video
        self.scam_types = screenshot.scam_types
        self.links = screenshot.links
        self.phone_numbers = screenshot.phone_numbers
        self.emails = screenshot.emails
        self.likes = screenshot.likes
        self.comments = screenshot.comments
        self.shares = screenshot.shares


def create_report(report: Report) -> (Report, Exception):
    new = report.__dict__
    del new["id"]
    try:
        data = supabase.table("report").insert(new).execute()
        return (data.data, None)
    except APIError as e:
        logging.error(f"Error creating report: {e}")
        return (None, e)


def get_report(report_id: int) -> Report:
    return supabase.table("report").select("*").eq("id", report_id).execute()
