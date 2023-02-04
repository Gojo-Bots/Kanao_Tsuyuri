from pyrogram.enums import ChatType as CT

from Chimku import *
from Chimku.database.user_info import USERS


@bot.on_message(filters.command(["start"], pre))
async def start_(c: bot, m: Message):
    txt = f"Hi! {m.from_user.mention}\nDo `/help` to know what I can do."

    if m.chat.type == CT.PRIVATE:
        await bot.send_message(m.chat.id, txt)
    else:
        await m.reply_text(txt)

@bot.on_message(filters.command(["help"], pre))
async def help_(c: bot, m: Message):
    txt = """
    Type `/link` in the chat to get invite link of the chat.
    Per join with you link will reward you some coin, which will further used to buy stuffs.

    Note that every /link will command will update the link you have created before in db
    and the user joined by that link will not considered as any base to give reward to you

    `/mylink` : To get previous genrated link of the chat by you.

    `/profile` <user id | username> : To get you information.

    **NOTE**: Your info will be stored in database when you type link in the group

    """
    await m.reply_text(txt)

@bot.on_message(filters.command(["links", "link"], pre) & ~filters.bot)
async def link_(c: bot, m: Message):
    try:
        await bot.send_message(m.from_user.id, "Genrating your link...")
    except Exception:
        await m.reply_text("Start the bot first")
        return
    is_user = USERS.is_user(m.from_user.id)
    if m.chat.type == CT.PRIVATE:
        await m.reply_text("This command is ment to be used in group")
        return
    if not is_user:
        try:
            c_link = await bot.create_chat_invite_link("Lowde_ka_channel")
        except Exception as e:
            await m.reply_text("Failed to create chat invite link")
        User = USERS(m.from_user.id)
        User.save_user(c_link)
        await m.reply_text(f"Here is your invite link:\n{c_link}")
        return

    elif is_user:
        try:
            c_link = await bot.create_chat_invite_link(m.chat.id)
        except Exception as e:
            await m.reply_text("Failed to create chat invite link")
        User = USERS(m.from_user.id)
        User.update_link(c_link)
        await m.reply_text(f"Here is your new invite link:\n{c_link}\nYou will not get reward if any user join with your previous invite link")
        return

@bot.on_message(filters.command(["mylink"], pre))
async def u_link(c: bot, m: Message):
    User = USERS(m.from_user.id)
    link = User.get_link()
    if link:
        await m.reply_text(f"Here is your link:\n{link}")
        return
    await m.reply_text("Seems link you are not registered in my db\nType `/link` to get registered")
    return

@bot.on_message(filters.command(["profile"], pre))
async def u_info(c: bot, m: Message):
    if not m.reply_to_message:
        split = m.text.split(None, 1)
        if len(split) == 1:
            user = m.from_user.id
        else:
            try:
                user = int(split[1])
            except ValueError:
                try:
                    user = (await bot.get_users(split[1])).id
                except Exception:
                    await m.reply_text("Unable to find user.")
    elif m.reply_to_message:
        user = m.reply_to_message.from_user.id
    User = USERS(user).get_info()
    if User:
        u_id = User["user_id"]
        link = User["link"]
        coin = User["coin"]
        joined = User["joined"]
        txt = f"""
        Here is the info of the user:
        🆔 User Id = `{u_id}`
        🔗 Link created = {link}
        🧿 Available coin = `{coin}`
        🧲 User joined via user's link = `{joined}`
        """
        await m.reply_text(txt)
        return
    else:
        await m.reply_text("No info available")

@bot.on_chat_member_updated(filters.new_chat_members)
async def coin_increaser(c: bot, u: ChatMemberUpdated):
    link = u.invite_link
    if not link:
        return
    USERS.update_coin(str(link))

