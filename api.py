from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel, HttpUrl
from bot.scam_check import is_image_scam, is_link_scam, is_phone_scam


app = FastAPI(
    title="Scam Detection API",
    description="API for detecting scams in images, links, and phone numbers",
    version="1.0.0",
    root_path="/api/v1",
)


class ImageUpload(BaseModel):
    image: UploadFile = File(...)

class LinkUpload(BaseModel):
    link: str

class PhoneUpload(BaseModel):
    phone: str


@app.get("/health")
def health():
    # TODO: Add health check for the API
    return {"status": "ok"}

@app.post("/check-image")
async def check_image(image: UploadFile = File(...)):
    return await is_image_scam(image)

@app.post("/check-link")
async def check_link(link: str):
    return await is_link_scam(link)

@app.post("/check-phone")
async def check_phone(phone: str):
    return await is_phone_scam(phone)
