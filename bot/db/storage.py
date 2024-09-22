from .supabase import supabase, supa_url
from telegram import PhotoSize, User

public_storage_url = supa_url + "/storage/v1/object/public"


def upload_img_to_supabase(image: PhotoSize, reporter_id: int, report_id: int):
    """Upload an image to the 'screenshots bucket in Supabase.'"""
    logging.info("Uploading image to Supabase")
    file_mimetype = mimetypes.guess_type(image.file_path)
    image_bytes = await file.download_as_bytearray()
    img_type = file_mimetype[0]
    supabase.storage.from_("screenshots").upload(
        file=bytes(img_bytes),
        path=f"/{reporter_id}/report_{report_id}",
        file_options={"content-type": img_type, "upsert": "true"},
    )


def get_img_from_supabase(reporter_id, report_id) -> bytes:
    """Get images from the 'screenshots' bucket in Supabase."""
    byte_img = supabase.storage.from_("screenshots").download(f"/{reporter_id}/report_{report_id}")
    return byte_img
