import pyromod
from pyrogram import Client, filters
from pyrogram.types import ChatMemberUpdated, Message

from KeysSecret import *

plugin = dict(root="Chimku.plugin")
bot = Client(
    "Chimku-Bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=plugin
    )


pre = ["/", "!", "$"]


bot.run()
