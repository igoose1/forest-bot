import functools
import logging

from telethon import events
from text_unidecode import unidecode

from . import FOREST_CHAT_ID, HELP_TEXT, bot

__all__ = ()

logger = logging.getLogger()


def in_forest(function):
    async def nop():
        pass

    @functools.wraps(function)
    def wrapper(event):
        if event.chat_id == FOREST_CHAT_ID:
            return function(event)
        return nop()

    return wrapper


async def is_shout(message) -> bool:
    decoded_text = unidecode(message.text).lower()
    is_every_symbol_a_shout = all(
        map(lambda symbol: symbol == "a", decoded_text)
    )
    return is_every_symbol_a_shout


@bot.on(events.NewMessage)
@bot.on(events.MessageEdited)
@bot.on(events.ChatAction)
@in_forest
async def ignore_new_message(event):
    if hasattr(event, "text") and await is_shout(event):
        return
    await event.delete()
    raise events.StopPropagation


@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.reply(HELP_TEXT)
