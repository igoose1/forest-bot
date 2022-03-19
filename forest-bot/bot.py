import datetime
import functools
import logging

from telethon import TelegramClient, events

from . import (
    API_HASH,
    API_ID,
    BOT_TOKEN,
    FOREST_CHAT_ID,
    HELP_TEXT,
    PUNISHMENT_DURATION,
    THROTTLING_PERIOD,
    THROTTLING_RATE,
)
from .utils import Throttle, is_shout, nop

__all__ = ("bot",)

logger = logging.getLogger()
sender_throttle = Throttle(THROTTLING_RATE, THROTTLING_PERIOD)
bot = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)


def in_forest(function):
    @functools.wraps(function)
    def wrapper(event):
        if event.chat_id == FOREST_CHAT_ID:
            return function(event)
        logger.info("chatting in another group.")
        return nop()

    return wrapper


async def punish_by_throttling(event):
    logger.info("punishing %d", event.sender_id)
    await bot.edit_permissions(
        await event.get_chat(),
        await event.get_sender(),
        datetime.datetime.utcnow() + PUNISHMENT_DURATION,
        send_messages=False,
        send_media=False,
        send_stickers=False,
        send_gifs=False,
        send_games=False,
        send_inline=False,
        embed_link_previews=False,
        send_polls=False,
        change_info=False,
        invite_users=True,
        pin_messages=False,
    )


def sender_throttling(function):
    @functools.wraps(function)
    def wrapper(event):
        if getattr(event, "sender_id", None) is None or sender_throttle(
            event.sender_id,
        ):
            return function(event)
        return punish_by_throttling(event)

    return wrapper


@bot.on(events.NewMessage)
@bot.on(events.MessageEdited)
@bot.on(events.ChatAction)
@in_forest
@sender_throttling
async def ignore_new_message(event):
    if not hasattr(event, "text") or not is_shout(event.text):
        await event.delete()
    raise events.StopPropagation


@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.reply(HELP_TEXT, link_preview=False)
