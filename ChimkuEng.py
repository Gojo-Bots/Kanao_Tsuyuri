from pyrogram import Client , filters
import tgcrypto
from datetime import datetime , timedelta
from KeysSecret import api_id,api_hash,bot_token

bot = Client("Chimku-Bot",
             api_id=api_id,
             api_hash=api_hash,
             bot_token=bot_token)


#When User commands "/link" The following code create a private link to invite users for them which is active for 1 day i.e 24 hours
@bot.on_message(filters.command(commands=['link']) & filters.private)
def link(Client,message):
        link = Client.create_chat_invite_link("@Lowde_ka_channel", expire_date=datetime.now() + timedelta(days=1))
        message.reply_text(link.invite_link)


@bot.on_message(filters.text & filters.private)
def NoCmd(Client,message):
    message.reply_text(text="No command was given , try again")


bot.run()


