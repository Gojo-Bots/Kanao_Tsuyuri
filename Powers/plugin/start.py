from pyrogram.enums import ChatType as CT
from pyrogram.types import InlineKeyboardMarkup as IKM, CallbackQuery

from KeysSecret import *
from Powers import *
from Powers.database.stuffs import STUFF
from Powers.database.user_info import USERS
from Powers.utils.keyboard import *


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
`/addcat` <name of CATEGORY should be str | pass nothing> : Add a new CATEGORY

**NOTE**: Your info will be stored in database when you type `/link` in the group

**db** standas for **DataBase**
"""
    await m.reply_text(txt)
    return

@bot.on_message(filters.command(["links", "link"], pre) & ~filters.bot & (filters.chat(CHAT_ID) | filters.private))
async def link_(c: bot, m: Message):
    try:
        await bot.send_message(m.from_user.id, "Genrating your link...")
    except Exception:
        await m.reply_text("Start the bot first")
        return
    is_user = USERS.is_user(m.from_user.id)
    if not is_user:
        try:
            c_link = (await bot.create_chat_invite_link(int(CHAT_ID))).invite_link
        except Exception as e:
            await m.reply_text(f"Failed to create chat invite link due to following error:\n{e}")
        User = USERS(m.from_user.id)
        User.save_user(c_link)
        await m.reply_text(f"Here is your invite link:\n`{c_link}`")
        return

    elif is_user:
        User = USERS(m.from_user.id)
        await m.reply_text(
            f"You already have an invite link\n[Here is your link]({User.get_link()})",
            reply_markup=IKM(yes_no),
            disable_web_page_preview=True
        )
        return

@bot.on_callback_query(filters.regex("^new_"))
async def new_linkkk(c: bot, q: CallbackQuery):
    data = q.data.split("_")[1]
    User = USERS(q.from_user.id)
    if q.message.reply_to_message.from_user.id != q.from_user.id:
        await q.answer("This is not for you baka")
        return
    if data == "yus":
        try:
            c_link = (await bot.create_chat_invite_link(CHAT_ID)).invite_link
        except Exception as e:
            await q.message.reply_text("Failed to create chat invite link")
        User.update_link(c_link)
        await q.message.reply_to_message.reply_text(f"Here is your new invite link:\n`{c_link}`\nYou will not get reward if any user join with your previous invite link")
        await q.message.delete
        return
    elif data == "noi":
        await q.message.reply_to_message.reply_text("Ok I haven't created new link for you")
        await q.message.delete()
        return

@bot.on_message(filters.command(["mylink"], pre))
async def u_link(c: bot, m: Message):
    User = USERS(m.from_user.id)
    link = User.get_link()
    if link:
        await m.reply_text(f"Here is your link:\n`{link}`")
        return
    await m.reply_text("Seems link you are not registered in my db\nType `/link` to get registered")
    return

@bot.on_message(filters.command(["profile", "myprofile"], pre))
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
        👥 User joined via user's link = `{joined}`
        """
        await m.reply_text(txt, disable_web_page_preview=True)
        return
    else:
        await m.reply_text("No info available")

@bot.on_message(filters.command(["addcat"], pre) & filters.private)
async def cat_adder(c:bot, m:Message):
    if m.from_user.id != OWNER_ID:
        await m.reply_text("You can't do that")
        return
    if len(m.text.split(None)) == 2:
        CATEGORY.append(str(m.text.split(None)[1].capitalize))
        added = str(m.text.split(None)[1].capitalize)
        await m.reply_text(f"Added {added} to CATEGORY")
        return
    else:
        x = await bot.ask(text = "Send me the name of CATEGORY",
        chat_id = m.from_user.id,
        filters=filters.text)
        CATEGORY.append(str(x.capitalize))

        await m.reply_text(f"Added {x.capitalize} to CATEGORY")
        return



@bot.on_message(filters.command(["addfile"], pre) & filters.private)
async def file_adder(c: bot, m: Message):
    if m.from_user.id != OWNER_ID:
        await m.reply_text("You can't do that")
        return
    Stuff = STUFF()
    ff_name = await bot.ask(
        text="Send me the name of the file", 
        chat_id = m.from_user.id,
        filters=filters.text
        )
    f_name = str(ff_name.text)
    await bot.send_message(m.from_user.id, "File name received")
    ff_link = await bot.ask(
        text = "Send me the link of the file",
        chat_id = m.from_user.id,
        filters=filters.text
        )
    await bot.send_message(m.from_user.id, "File link received")
    f_link = str(ff_link.text)
    while True:
        ff_coin = await bot.ask(
            text = "Send me the amount of the file you want to set",
            chat_id = m.from_user.id,
            filters=filters.text
            )
        f_coin = ff_coin

        try:
            f_coin = abs(int(f_coin.text))
            if f_coin:
                await bot.send_message(m.from_user.id, "File amount received")
                
                break
            else:
                await bot.send_message(m.from_user.id, "Amount should not be 0")
        except ValueError:
            await bot.send_message(m.from_user.id, "Amount should be natural number")

    txt = "Send me type of the file you want to set available types:\n"
    for i in CATEGORY:
        txt += f"\n{i}\n"
    txt += "\n If the file name contains space between them seprate them using **_**"
    while True:
        ff_type = await bot.ask(
            text = txt,
            chat_id = m.from_user.id,
            filters=filters.text
            )
        f_type = str(ff_type.text)

        if str(f_type).lower() not in CATEGORY:
            await bot.send_message(m.from_user.id, "Invalid file type")
        elif str(f_type).lower() in CATEGORY:
            await bot.send_message(m.from_user.id, "File type received")
            break
    
    edit = await bot.send_message(m.from_user.id, "All value recieved initalizing database")

    Stuff.add_file(f_name, f_link, f_coin, f_type)

    await bot.edit_message_text(m.from_user.id, edit.id, "Added the file and it's info to database")

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


@bot.on_chat_member_updated(filters.chat(CHAT_ID))
async def coin_increaser(c: bot, u: ChatMemberUpdated):
    if u.new_chat_member:
        try:
            link = u.invite_link.invite_link
            if not link:
                return
            USERS.update_coin(str(link), int(AMOUNT))
            USERS.update_joined(str(link))
            return
        except AttributeError:
            return
    else:
        return

