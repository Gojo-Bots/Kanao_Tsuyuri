from pyrogram.enums import ChatType as CT

from KeysSecret import *
from Powers import *
from Powers.database.stuffs import STUFF
from Powers.database.user_info import USERS


@bot.on_message(filters.command(["start"], pre))
async def start_(c: bot, m: Message):
    txt = f"Hi! {m.from_user.mention}\nDo `/help` to know what I can do."

    if m.chat.type == CT.PRIVATE:
        await bot.send_message(m.chat.id, txt)
        return
    else:
        await m.reply_text(txt)
        return

@bot.on_message(filters.command(["help"], pre))
async def help_(c: bot, m: Message):
    txt = """
    Type `/link` in the chat to get invite link of the chat.
    Per join with you link will reward you some coin, which will further used to buy stuffs.

    Note that every /link will command will update the link you have created before in db
    and the user joined by that link will not considered as any base to give reward to you

    `/mylink` : To get previous genrated link of the chat by you.

    `/profile` <user id | username> : To get you information.

    `/premium`: To get link of premium channel. Works only in private chat

    `buy` : To buy stuffs. Works only in private chat

    **OWNER ONLY**
    `/addfile` : To add file
    `/rmfile` <link of the file>: To remove file

    **NOTE**: Your info will be stored in database when you type `/link` in the group

    """
    await m.reply_text(txt)
    return

@bot.on_message(filters.command(["links", "link"], pre) & ~filters.bot & filters.chat(CHAT_ID))
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
            if len(CHAT_ID) == 1:
                c_link = await bot.create_chat_invite_link(int(CHAT_ID))
            else:
                c_link = await bot.create_chat_invite_link(int(CHAT_ID))
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
                    return
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

@bot.on_message(filters.command(["addfile"], pre) & filters.private)
async def file_adder(c: bot, m: Message):
    if m.from_user.id != OWNER_ID:
        await m.reply_text("You can't do that")
        return
    Stuff = STUFF()
    f_name = await bot.ask(
        text="Send me the name of the file", 
        identifier = (m.chat.id, m.from_user.id, m.id),
        chat_id = m.from_user.id,
        filters=filters.text
        )
    f_name = str(f_name)
    await bot.send_message(m.from_user.id, "File name received")
    f_link = await bot.ask(
        text = "Send me the link of the file",
        identifier = (m.chat.id, m.from_user.id, m.id),
        chat_id = m.from_user.id,
        filters=filters.text
        )
    await bot.send_message(m.from_user.id, "File link received")
    while True:
        f_coin = await bot.ask(
            text = "Send me the amount of the file you want to set",
            identifier = (m.chat.id, m.from_user.id, m.id),
            chat_id = m.from_user.id,
            filters=filters.text
            )
        try:
            f_coin = abs(int(f_coin))
            if f_coin:
                await bot.send_message(m.from_user.id, "File amount received")
                break
            else:
                await bot.send_message(m.from_user.id, "Amount should not be 0")
        except ValueError:
            await bot.send_message(m.from_user.id, "Amount should be natural number")

    txt = "Send me type of the file you want to set available types:\n"
    for i in Category:
        txt += f"\n{i}\n"
    txt += "\n If the file name contains space between them seprate them using **_**"
    while True:
        f_type = await bot.ask(
            text = txt,
            identifier = (m.chat.id, m.from_user.id, m.id),
            chat_id = m.from_user.id,
            filters=filters.text
            )
        if str(f_type).lower() not in Category:
            await bot.send_message(m.from_user.id, "Invalid file type")
        elif str(f_type).lower() in Category:
            await bot.send_message(m.from_user.id, "File type received")
            break
    
    edit = await bot.send_message(m.from_user.id, "All value recieved initalizing database")

    Stuff.add_file(f_name, f_link, f_coin, f_type)

    await bot.edit_message_text(m.from_user.id, edit.id, "Added the file and it's info to db")

@bot.on_message(filters.command(["rmfile"], pre) & filters.private)
async def rm_file(c: bot, m: Message):
    Stuff = STUFF
    split = m.text.split(None,1)
    if len(split) == 1:
        await m.reply_text("USAGE : `/rmfile` <link of the file>")
        return
    link = split[1]
    rm = Stuff.remove_file(link)
    if rm:
        await m.reply_text("Removed file")
        return
    else:
        await m.reply_text("Unable to find file with corresponding link.")
        return



@bot.on_chat_member_updated(filters.new_chat_members)
async def coin_increaser(c: bot, u: ChatMemberUpdated):
    link = u.invite_link
    if not link:
        return
    USERS.update_coin(str(link))
    return

