from telegram import Update
from telegram.ext import ContextTypes

from bot.messages import ScamHuntMessages as messages
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.handler.utils import (
    BotStates,
    CallbackData,
)

from bot.handler.receiver import extract_platform
from bot.onboarding.onboarding import is_onboarding, onboarding
from bot.handler import commands

from bot.openai.ocr import ocr_image, Platform
from bot.openai.embeddings import get_embedding
import logging
from bot.db import report, embeddings
from bot.user_metrics import track_user_event, Event
from bot.feedback import process_feedback, is_feedback
from bot.db.user import create_user_if_not_exists
from bot.db.storage import upload_img_to_supabase
from bot.db.image_hash import create_image_hash, get_image_report
from bot.handler.utils import get_inline_keyboard_for_scam_result
from bot.db.report import update_report_correctness
from bot.db.user import is_banned


@is_banned
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the callback query from the inline keyboard."""
    track_user_event(update, context)
    await scam_result_feedback(update, context)
    if is_onboarding(update.callback_query.data):
        await onboarding(update, context)
        return
    if is_feedback(update.callback_query.data):
        await process_feedback(update, context)
        return
    query = update.callback_query
    await query.answer()
    match query.data:
        case CallbackData.REPORT_SCAM:
            await commands.report(update, context)
        case CallbackData.CANCEL:
            track_user_event(update, context, Event.CANCEL)
            await commands.report(update, context)
        case CallbackData.CONFIRM:
            if context.user_data["state"] == BotStates.RECEIVE_SCREENSHOT:
                await confirm_screenshot(update, context)
            elif context.user_data["state"] == BotStates.RECEIVE_LINK:
                await confirm_link(update, context)
        case CallbackData.FEEDBACK:
            await commands.feedback(update, context)


async def confirm_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    track_user_event(update, context, Event.CONFIRM_LINK)
    links = context.user_data["links"]
    platform = extract_platform(links[0])
    context.user_data["report"] = report.Report(
        platform=platform.value,
        report_url=links[0],
        is_advertisement=False,
        is_sponsored=False,
        is_photo=False,
        is_video=False,
        is_social_media_post=False,
        created_by_tg_id=update.effective_user.id,  # Using the Telegram user's ID
    )

    create_user_if_not_exists(update, context)
    r, err = report.create_report(context.user_data["report"])
    track_user_event(update, context, Event.REPORT_CREATED)
    await send_confirmation_message(update, context)


async def confirm_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    track_user_event(update, context, Event.CONFIRM_SCREENSHOT)
    query = update.callback_query
    message = await query.edit_message_text(
        text=messages.looking_into_scam, parse_mode="Markdown"
    )
    # Download file
    image = await context.bot.get_file(context.user_data["photo"].file_id)
    # Attempt to get the report associated with the image
    result = await get_image_report(image)
    is_duplicate = True if result else False
    if not result:
        # If no report is found, attempt OCR
        result, exception = await ocr_image(image)
        result.scam_types = [scam_type.dict() for scam_type in result.scam_types]
        if not result.is_screenshot or result.platform == Platform.UNKNOWN:
            logging.error(
                f"Invalid platform: {result.platform}, Is screenshot: {result.is_screenshot}"
            )
            await query.edit_message_text(
                text=messages.not_a_screenshot_message,
                parse_mode="Markdown",
            )
            return

    scam_likelihood = result.scam_likelihood

    context.user_data["confirmation_message"] = (
        messages.get_screenshot_confirmation_message(scam_likelihood=scam_likelihood)
    )
    await message.edit_text(
        text=messages.get_screenshot_result_message(
            scam_likelihood, reasoning=result.reasoning
        ),
        parse_mode="Markdown",
        reply_markup=get_inline_keyboard_for_scam_result(),
    )

    r = report.Report(
        platform=result.platform,
        from_user=result.from_user,
        to_user=result.to_user,
        caption=result.caption,
        location=result.location,
        description=result.description,
        reasoning=result.reasoning,
        scam_likelihood=result.scam_likelihood,
        is_advertisement=result.is_advertisement,
        is_sponsored=result.is_sponsored,
        is_photo=result.is_photo,
        is_video=result.is_video,
        is_social_media_post=result.is_social_media_post,
        created_by_tg_id=update.effective_user.id,
        scam_types=result.scam_types,
        links=result.links,
        phone_numbers=result.phone_numbers,
        emails=result.emails,
        likes=result.likes,
        comments=result.comments,
        shares=result.shares,
    )

    try:
        create_user_if_not_exists(update, context)
        r = report.create_report(r)
        track_user_event(update, context, Event.REPORT_CREATED)

        if not is_duplicate:
            embed_result = await get_embedding(f"{result.caption} {result.description}")
            embeddings.insert_embedding(embed_result.embedding, r.id)
            await create_image_hash(
                image, report_id=r.id, user_id=update.effective_user.id
            )
            await upload_img_to_supabase(image, update.effective_user.id, r.id)

    except Exception as err:
        logging.error(f"Report created without embedding or id: {err}")
        await query.edit_message_text(text=messages.error, parse_mode="Markdown")
        return


async def send_confirmation_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    confirmation_message: str = messages.confirm,
):
    await update.callback_query.edit_message_text(
        text=confirmation_message,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Hunt on Facebook", url="https://www.facebook.com"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Hunt on Instagram", url="https://www.instagram.com"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Report suspicious post", callback_data=CallbackData.REPORT_SCAM
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Share your feedback", callback_data=CallbackData.FEEDBACK
                    )
                ],
            ]
        ),
    )

    if context.user_data["is_new"]:
        await commands.feedback(update, context)


async def scam_result_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query.data in [
        CallbackData.YES,
        CallbackData.NO,
        CallbackData.UNSURE,
    ]:
        report_id = context.user_data.get("report_id")
        if report_id:
            correctness = update.callback_query.data
            try:
                update_report_correctness(report_id, correctness)
            except Exception as e:
                logging.error(f"Error updating report correctness: {e}")

        confirmation_message = context.user_data["confirmation_message"]
        await send_confirmation_message(update, context, confirmation_message)
