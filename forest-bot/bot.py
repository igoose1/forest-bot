import datetime
import functools
import logging

from pyrogram import Client, errors, filters, types

from . import (
    API_HASH,
    API_ID,
    BOT_TOKEN,
    FOREST_CHAT_ID,
    HELP_TEXT,
    PUNISHMENT_DURATION,
    STICKER_WHITELIST,
    THROTTLING_PERIOD,
    THROTTLING_RATE,
)
from .utils import Throttle, is_shout

__all__ = ("app",)

logger = logging.getLogger("forest-bot")
sender_throttle = Throttle(THROTTLING_RATE, THROTTLING_PERIOD)
app = Client("bot", API_ID, API_HASH, bot_token=BOT_TOKEN)


def punish_by_throttling(client, message: types.Message):
    logger.info("user (id=%d) was punished.", message.from_user.id)
    message.pin().delete()
    try:
        client.restrict_chat_member(
            message.chat.id,
            message.from_user.id,
            types.ChatPermissions(
                can_send_messages=False,
                can_change_info=False,
                can_pin_messages=False,
            ),
            int((datetime.datetime.now() + PUNISHMENT_DURATION).timestamp()),
        )
    except errors.exceptions.bad_request_400.UserAdminInvalid:
        logger.warning("user (id=%d) couldn't be banned.", message.from_user.id)


def sender_throttling(function):
    @functools.wraps(function)
    def wrapper(client, message):
        if getattr(message, "from_user", None) and not sender_throttle(
            message.from_user.id,
        ):
            punish_by_throttling(client, message)
        return function(client, message)

    return wrapper


@app.on_message(filters.chat(FOREST_CHAT_ID))
@sender_throttling
def filter_messages(client, message: types.Message):
    logger.info("new message was received (id=%d).", message.message_id)
    if message.sticker and message.sticker.file_unique_id in STICKER_WHITELIST:
        return
    if (
        not getattr(message, "text", None)
        or message.media
        or not is_shout(message.text.markdown)
    ):
        logger.info("message (id=%d) was deleted.", message.message_id)
        message.delete()


@app.on_message(filters.command("start"))
def start(client, message: types.Message):
    message.reply(HELP_TEXT, quote=True, disable_web_page_preview=True)
