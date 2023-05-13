import pyroaddon
from pyrogram import Client, ContinuePropagation, filters
from pyrogram.types import ChatMemberUpdated, Message

from KeysSecret import *

plugin = dict(root="Powers.plugin")
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=plugin
    )


pre = ["/", "!", "$"]


bot.run()
