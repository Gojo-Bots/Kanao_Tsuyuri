import time
from datetime import datetime, timedelta

import pytz
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.enums import ChatType as CT
from pyrogram.enums import ParseMode as PM
from pyrogram.errors import UserIsBlocked
from pyrogram.types import CallbackQuery
from pyrogram.types import InlineKeyboardMarkup as IKM

from KeysSecret import *
from Powers import *
from Powers.database.stuffs import STUFF
from Powers.database.temp import TEMP
from Powers.database.user_info import USERS
from Powers.utils.keyboard import *
from Powers.utils.text import help_txt

info_dict = {}


DEV_LEVEL = SUDO + [OWNER] + [DEV]

def is_cancel(msg):
    if str(msg).lower() == "/cancel":
        return True
    else:
        False
back_kb = IKM(
        [
            [
                KB("⬅️ Back", "menu_back"),
                KB("❌ Close", "close")
            ]
        ]
    )
@bot.on_message(filters.command(["start"], pre))
async def start_(c: bot, m: Message):
    if m.chat.type == CT.PRIVATE:
        if len(m.text.split()) > 1:
            option = (m.text.split(None, 1)[1]).lower()
            if option.startswith("compensate"):
                is_temp = TEMP().get_temp_info(m.from_user.id)
                if not is_temp:
                    await m.reply_text("You have already claimed your reward\nOr you are trying to claim is not belongs to you")
                    return
                coins = int(m.text.split("_", 1)[1])
                Users = USERS(m.from_user.id).get_link()
                if not Users:
                    await m.reply_text(f"Failed to give {COIN_NAME} {COIN_EMOJI}\nType /link and try again")
                    return
                USERS.update_coin(str(Users), coins)
                TEMP().drop_collection(m.from_user.id)
                await bot.unpin_all_chat_messages(m.from_user.id)
                await m.reply_text(f"You got your {COIN_NAME} {COIN_EMOJI} back")
                return
    txt = f"Hi! {m.from_user.mention}\nDo /help to know what I can do."
    if m.chat.type == CT.PRIVATE:
        await bot.send_message(m.chat.id, txt, reply_markup=help_kb())
        return
    else:
        await m.reply_text(txt,reply_markup=help_kb())
        return
@bot.on_callback_query(filters.regex("^menu_"), group=-1)
async def help_menu_back(c: bot, q: CallbackQuery):
    data = q.data.split("_")[-1]
    if data == "help":
        await q.answer("Help menu")
        await q.edit_message_text(help_txt, reply_markup=back_kb)
        return
    elif data == "back":
        await q.answer("Back")
        await q.edit_message_text(f"Hi! {q.message.from_user.mention}\nDo /help to know what I can do.", reply_markup=help_kb())
        return

@bot.on_message(filters.command(["help"], pre))
async def help_(c: bot, m: Message):
    await m.reply_text(help_txt, reply_markup=back_kb)
    return
@bot.on_message(filters.command(["addowner"], pre))
async def owner_add(c: bot, m: Message):
    if not m.from_user:
        await m.reply_text("Not an user")
        return
    if m.from_user.id not in DEV_LEVEL:
        await m.reply_text("You can't do that")
        return
    if m.reply_to_message:
        user = m.reply_to_message.from_user.id
    else:
        user = m.text.split(None)[1]
        try:
            user = int(user)
        except ValueError:
            await m.reply_text("Give me id which is an integer type data")
            return
    try:
        await bot.send_message(user, "You are added as owner")
    except Exception:
        await m.reply_text("Tell him to start the bot first")
        return
    DEV_LEVEL.append(user)
    await m.reply_text(f"Added user id `{user}` to owner's list")
    return
@bot.on_message(filters.command(["rmowner"], pre))
async def owner_rm(c: bot, m: Message):
    if not m.from_user:
        await m.reply_text("Not an user")
        return
    if m.from_user.id not in DEV_LEVEL:
        await m.reply_text("You can't do that")
        return
    if m.reply_to_message:
        user = m.reply_to_message.from_user.id
    else:
        user = m.text.split(None)[1]
        try:
            user = int(user)
        except ValueError:
            await m.reply_text("Give me id which is an integer type data")
            return
    for i in DEV_LEVEL:
        if user == i:
            DEV_LEVEL.remove(i)
    await m.reply_text("Removed the user")

@bot.on_message(filters.command(["owners"], pre))
async def owners_info(c: bot, m: Message):
    try:
        infos = await bot.get_users(DEV_LEVEL)
    except Exception as e:
        await m.reply_text(f"Failed to get info of owners due to\n{e}")
        return
    txt = "**Here are the info of owners:**\n"
    
    for x in infos:
        if not x.is_deleted:
            txt += f"\nFull name : {x.first_name} {x.last_name}\nId : `{x.id}`\nUsername : @{x.username}\n\n"
        else:
            txt += f"\nThis user having id `{x.id} have deleted his account"

    await m.reply_text(txt)
    return

@bot.on_message(filters.command(["links", "link"], pre) & ~filters.bot & (filters.chat(CHAT_ID) | filters.private))
async def link_(c: bot, m: Message):
    if not m.from_user:
        await m.reply_text("Not an user")
        return
    is_user = USERS.is_user(m.from_user.id)
    if not is_user:
        try:
            to_del = await bot.send_message(m.from_user.id, "Genrating your link...")
        except Exception:
            await m.reply_text("Start the bot first")
            return
        try:
            c_link = (await bot.create_chat_invite_link(int(CHAT_ID))).invite_link
        except Exception as e:
            await m.reply_text(f"Failed to create chat invite link due to following error:\n{e}")
            return
        User = USERS(m.from_user.id)
        User.save_user(c_link)
        await m.reply_text(f"Here is your invite link:\n`{c_link}`")
        await to_del.edit_text(f"Here is your invite link:\n`{c_link}`")
        return

    elif is_user:
        User = USERS(m.from_user.id)
        await m.reply_text(
            f"You already have an invite link\nHere is your link : `{User.get_link()}`",
            reply_markup=IKM(yes_no),
            disable_web_page_preview=True
        )
        return

@bot.on_callback_query(filters.regex("^new_"), 4)
async def new_linkkk(c: bot, q: CallbackQuery):
    data = q.data.split("_")[1]
    User = USERS(q.from_user.id)
    to_del = await bot.send_message(q.from_user.id, "Genrating your link...")
    try:
        if q.message.reply_to_message.from_user.id != q.from_user.id:
            await q.answer("This is not for you baka")
            return
    except AttributeError: # This means the user asked for link in private chat
        pass 
    if data == "yus":
        try:
            c_link = (await bot.create_chat_invite_link(CHAT_ID)).invite_link
            try:
                old_link = User.get_link()
                del info_dict[f"{old_link}"]
            except KeyError:
                pass
        except Exception as e:
            await q.message.reply_text("Failed to create chat invite link")
        User.update_link(c_link)
        await q.edit_message_text(f"Here is your new invite link:\n`{c_link}`\nYou will not get reward if any user join with your previous invite link")
        await to_del.edit_text(f"Here is your new invite link:\n`{c_link}`\nYou will not get reward if any user join with your previous invite link")
        return
    elif data == "noi":
        await q.edit_message_text("Ok I haven't created new link for you")
        await to_del.edit_text("Ok I haven't created new link for you")
        return

@bot.on_message(filters.command(["mylink"], pre))
async def u_link(c: bot, m: Message):
    if not m.from_user:
        await m.reply_text("Not an user")
        return
    User = USERS(m.from_user.id)
    link = User.get_link()
    if link:
        await m.reply_text(f"Here is your link:\n`{link}`")
        return
    await m.reply_text("Seems link you are not registered in my db\nType /link to get registered")
    return

@bot.on_message(filters.command(["profile", "myprofile"], pre))
async def u_info(c: bot, m: Message):
    if not m.from_user:
        await m.reply_text("Not an user")
        return
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
                    try:
                        user = (await bot.get_users(split[1].split("/")[-1])).id
                    except:
                        await m.reply_text("Unable to find user.")
                        return
    elif m.reply_to_message:
        xXx = m.reply_to_message.from_user
        if xXx:
            user = xXx.id
        elif m.reply_to_message.sender_chat:
            user = m.from_user.id
        else:
            await m.reply_text("This is not an user I guess...")
            return
    User = USERS(user).get_info()
    if User:
        u_id = User["user_id"]
        link = User["link"]
        coin = User["coin"]
        joined = User["joined"]
        mess = User["message"]
        txt = f"""
Here is the info of the user:
🆔 User Id = `{u_id}`
🔗 Link created = {link}
{COIN_EMOJI} Available {COIN_NAME} = `{coin}`
✉️ No. of message required to get coin = {NUMBER_MESSAGE-int(mess)}
👥 User joined via user's link = `{joined}`
        """
        await m.reply_text(txt, disable_web_page_preview=True)
        return
    else:
        await m.reply_text("No info available. Seems like you are not registed. Start the bot and type /link to get registed")

@bot.on_message(filters.command(["addcat"], pre) & filters.private)
async def cat_adder(c:bot, m:Message):
    if not m.from_user:
        return
    if m.from_user.id not in DEV_LEVEL:
        await m.reply_text("You can't do that")
        return
    Category = CATEGORY
    for i in list(stuff.file_sorted()):
        Category.append(i)
    if len(m.text.split(None,1)) == 2:
        new_cat = str(m.text.split(None,1)[1].replace(" ", "_").lower())
        for i in Category:
            if i == new_cat:
                await m.reply_text("Category already exist")
                return
        CATEGORY.append(new_cat)
        added = str(m.text.split(None,1)[1].capitalize())
        await m.reply_text(f"Added {added} to CATEGORY")
        return
    else:
        x = await bot.ask(text = "Send me the name of CATEGORY",
        chat_id = m.from_user.id,
        filters=filters.text)
        if is_cancel(x.text):
            await m.reply_text("Canceled the operation")
            return
        new_cat = str(x.text.replace(" ", "_").lower())
        for i in Category:
            if i == new_cat:
                await m.reply_text("Category already exist")
                return
        CATEGORY.append(new_cat)

        await m.reply_text(f"Added {x.text.capitalize()} to CATEGORY")
        return

@bot.on_message(filters.command(['forward'], pre))
async def forwarder(c:bot, m: Message):
    if not m.from_user:
        return
    if m.from_user.id not in DEV_LEVEL:
        await m.reply_text("You can't do that")
        return
    if not m.reply_to_message:
        await m.reply_text("Reply to a message to forward it")
        return
    users = USERS.get_all_users()
    i = 0
    rem = 0
    um = await m.reply_text("Forwarding the message")
    for user in users:
        try:
            await bot.forward_messages(int(user), m.chat.id, m.reply_to_message_id)
        except Exception:
            i += 1
            try:
                USERS(user).delete_user()
                rem += 1
            except Exception:
                pass
            pass
    
    await um.delete()
    if i == len(users):
        await m.reply_text("Failed to forward message")
    await m.reply_text(f"Successfully forwardeded the message to {len(users) - i} out of {len(users)} users\nRemoved those user who have blocked me from my database\nRemoved user: {rem}")
    return

async def help_broadcast(file:Message):
    users = USERS.get_all_users()
    i = 0
    rem = 0
    mode = PM.MARKDOWN
    capt = "BROADCASTED"
    if file.media:
        capt = file.caption
    for user in users:
        try:
            if file.text:
                await bot.send_message(int(user), file.text.markdown, parse_mode=mode)
            elif file.animation:
                await bot.send_animation(int(user), file.animation.file_id, caption=capt, parse_mode=mode)
            elif file.photo:
                await bot.send_photo(int(user), file.phfoto.file_id, caption=capt, parse_mode=mode)
            elif file.video:
                await bot.send_video(int(user), file.video.file_id, caption=capt, parse_mode=mode)
            elif file.document:
                await bot.send_document(int(user), file.document.file_id, caption=capt, parse_mode=mode)
            else:
                i = "Unsupported file type"
                return i , len(users)
        except Exception:
            i += 1
            try:
                USERS(int(user)).delete_one()
                rem += 1
            except Exception:
                pass
            pass
    return i, len(users), rem

@bot.on_message(filters.command(["broadcast"], pre))
async def broadcaster(c: bot, m: Message):
    if not m.from_user:
        return
    if m.from_user.id not in DEV_LEVEL:
        await m.reply_text("You can't do that")
        return
    if m.chat.type != CT.PRIVATE:
        await m.reply_text("Meant to be used in private.....however you can use /forward in chats")
        return
    if m.reply_to_message:
        reply_to = m.reply_to_message
        um = await m.reply_text("Broadcasting message...")
        x, y, z = await help_broadcast(reply_to)
        
        await um.delete()
        if type(x) == str:
            await m.reply_text(x)
            return
        suc = y-x
        if not suc:
            await m.reply_text("Failed to broadcast the message.")
            return
        await m.reply_text(f"Successfully broadcasted message to {suc} users out of {y} users")
        return
    else:
        file = await bot.ask(
            text = "Send me the file or text\nType /cancel to abort the operation",
            chat_id = m.from_user.id
            )
        if is_cancel(file.text):
            await bot.send_message(m.chat.id,"Aborted the task")
            return
        z = await bot.send_message(m.chat.id,f"{'Text' if file.text else 'File'} recived hold tight will I fetch data and broadcast it")
        if file.text:
            await bot.get_messages(m.chat.id,file.id+1)
        else:
            mess = await bot.get_messages(m.chat.id,file.id+1)
        await z.delete()
        await file.delete()
        um = await m.reply_text("Broadcasting message...")
        x = await help_broadcast(mess)
        await um.delete()
        if type(i) == str:
            await m.reply_text(i)
            return
        suc = y-x
        if not suc:
            await m.reply_text("Failed to broadcast the message.")
            return
        await m.reply_text(f"Successfully broadcasted message to {suc} users out of {y} users\n`{int(y)-int(suc)}` users have blocked you\nRemoved those user who have blocked me from my database\nRemoved user: {z}")
        return
       
@bot.on_message(filters.command(["gift"], pre))
async def gift_one(c: bot, m: Message):
    if not m.from_user:
        return
    if m.from_user.id not in DEV_LEVEL:
        await m.reply_text("Only owner can do it")
        return
    split = m.text.split(None)
    if len(split) < 3 and not (len(split) == 2 and m.reply_to_message):
        await m.reply_text("Use /help to see how to use this command")
        return
    if len(split) == 3:
        try:
            user = int(split[1])
        except ValueError:
            await m.reply_text("Must pass user id")
            return
        try:
            money = abs(int(split[2]))
        except ValueError:
            await m.reply_text("Coin should be natural number")
        User = USERS(user).get_info()
        if not User:
            await m.reply_text("User is not registered in my database")
        link = User["link"]
        try:
            await bot.send_message(user,f"Owner of the bot gave you {money} {COIN_NAME +' '+ COIN_EMOJI}  enjoy🎉")
            USERS.update_coin(str(link), money)
            await m.reply_text(f"Successfully given {user} {money} {COIN_NAME +' '+ COIN_EMOJI}")
            return
        except Exception:
            await m.reply_text("Tell the user to start the bot first")
            return
    if len(split) == 2:
        if not m.reply_to_message.from_user:
            await m.reply_text("This is not an user I guess")
            return
        user = m.reply_to_message.from_user.id
        money = split[1]
        try:
            money = abs(int(split[1]))
        except ValueError:
            await m.reply_text("Coin should be natural number")
        User = USERS(user).get_info()
        link = User["link"]
        try:
            await bot.send_message(user,f"Owner of the bot gave you {money} {COIN_NAME +' '+ COIN_EMOJI} enjoy🎉")
            USERS.update_coin(str(link), money)
            await m.reply_text(f"Successfully given {user} {money} {COIN_NAME +' '+ COIN_EMOJI}")
            return
        except Exception:
            await m.reply_text("Tell the user to start the bot first")
            return

@bot.on_message(filters.command(["giftall"], pre))
async def gift_all(c: bot, m: Message):
    if not m.from_user:
        await m.reply_text("Not an user")
        return
    if m.from_user.id not in DEV_LEVEL:
        await m.reply_text("Only owner can do it")
        return
    split = m.text.split(None)
    if len(split) != 2:
        await m.reply_text("Type /help to see how")
        return
    try:
        money = abs(int(split[1]))
    except ValueError:
        await m.reply_text("Coin should be natural number")
        return
    um = await m.reply_text(f"Trying to give all users {money} {COIN_NAME +' '+ COIN_EMOJI}")
    users = USERS.get_all_users()
    if not users:
        await m.reply_text("No users found")
        return
    l = 0
    rem = 0
    for user in users:
        User = USERS(user).get_info()
        if not User:
            l+=1
            pass
        elif User:
            link = User["link"]
            i = User["user_id"]
            try:
                await bot.send_message(int(i), f"Owner of the bot gave you {money} {COIN_NAME +' '+ COIN_EMOJI} enjoy🎉")
                USERS.update_coin(link,money)
            except Exception:
                l+=1
                try:
                    USERS(user).delete_user()
                    rem += 1
                except Exception:
                    pass
                pass
    await um.delete()
    if l == len(users):
        await m.reply_text("Failed to give any user gifts.")
        return
    await m.reply_text(f"Successfully given {len(users) - l} out of {len(users)} users {money} {COIN_NAME +' '+ COIN_EMOJI}\nRemoved those user who have blocked me from my database\nRemoved user: {rem}")
    return

@bot.on_message(filters.command(["addfile"], pre) & filters.private)
async def file_adder(c: bot, m: Message):
    if not m.from_user:
        await m.reply_text("Not an user")
        return
    if m.from_user.id not in DEV_LEVEL:
        await m.reply_text("You can't do that")
        return
    Stuff = STUFF()
    ff_name = await bot.ask(
        text="Send me the name of the file\nType /cancel to abort the operation", 
        chat_id = m.from_user.id,
        filters=filters.text
        )
    if is_cancel(ff_name.text):
        await m.reply_text("Canceled the operation")
        return    
    f_name = str(ff_name.text.lower())
    await bot.send_message(m.from_user.id, "File name received")
    ff_link = await bot.ask(
        text = "Send me the file\nIf you want to create a join link when user clicks on this file send me the chat id\nType /cancel to abort the operation",
        chat_id = m.from_user.id
        )
    if is_cancel(ff_link.text):
        await m.reply_text("Canceled the operation")
        return
    x = await bot.send_message(m.from_user.id, "File received")
    m_id = int(x.id) - 1
    x = await x.edit_text("Trying to get file id...")
    file = await bot.get_messages(m.chat.id, m_id)
    if file.document:
        file_id = file.document.file_id
        file_type = "document"
    elif file.photo:
        file_id = file.photo.file_id
        file_type = "photo"
    elif file.video:
        file_id = file.video.file_id
        file_type = "video"
    elif file.animation:
        file_id = file.animation.file_id
        file_type = "animation"
    elif file.video_note:
        file_id = file.video_note.file_id
        file_type = "video_note"
    elif file.text:
        try:
            file_id = int(file.text)
            chats = await bot.get_chat(file_id)
            go_st = await bot.get_chat_member(chats.id, (await bot.get_me()).id)
            if go_st in [CMS.ADMINISTRATOR or CMS.OWNER]:
                file_type = "link"
            else:
                file_id = file.text.markdown
                file_type = "text"
        except Exception:
            file_id = file.text.markdown
            file_type = "text"
    else:
        x = await x.edit_text("Unsupported file type provided")
        return
    x = await x.edit_text(f"{'File id received' if not file.text else 'Text received'}")
    while True:
        ff_coin = await bot.ask(
            text = "Send me the amount of the file you want to set\nType /cancel to abort the operation",
            chat_id = m.from_user.id,
            filters=filters.text
            )
        if is_cancel(ff_coin.text):
            await m.reply_text("Canceled the operation")
            return
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
    Category = CATEGORY
    for i in list(stuff.file_sorted()):
        Category.append(i)
    for i in sorted(list(set(Category))):
        txt += f"\n`{i}`\n"
    txt += "\n If the file name contains space between them seprate them using **_**\nType /cancel to abort the operation"
    while True:
        ff_type = await bot.ask(
            text = txt,
            chat_id = m.from_user.id,
            filters=filters.text
            )
        if is_cancel(ff_type.text):
            await m.reply_text("Canceled the operation")
            return
        f_type = str(ff_type.text.lower())

        if str(f_type).lower() not in Category:
            new = await bot.ask(text = "Invalid file type\nDo you want to create new category\n type `yes` to create one and `no` to don't\nType /cancel to abort the operation", chat_id = m.from_user.id, filters = filters.text)
            if is_cancel(new.text.lower()):
                await m.reply_text("Canceled the operation")
                return
            if new.text.lower() == "yes":
                new_cat = await bot.ask(text = "Send me the name of CATEGORY\nType /cancel to abort the operation", chat_id = m.from_user.id, filters = filters.text)
                if is_cancel(new.text.lower()):
                    await m.reply_text("Canceled the operation")
                    return
                CATEGORY.append(str(new_cat.text).replace(" ", "_").lower())
                f_type = str(new_cat.text).replace(" ", "_").lower()
                await bot.send_message(m.from_user.id, "File type received")
                break
        elif str(f_type).lower() in Category:
            await bot.send_message(m.from_user.id, "File type received")
            break
    
    edit = await bot.send_message(m.from_user.id, "All value recieved initalizing database")

    is_their = Stuff.add_file(f_name, file_id, f_coin, f_type, file_type)
    if is_their:
        await bot.edit_message_text(m.from_user.id, edit.id, "Added the file and it's info to database")
        return
    else:
        await bot.edit_message_text(m.from_user.id, edit.id, "File already exsist")
        return

@bot.on_message(filters.command(["setvalue","setval"]))
async def set_user_coins_val(c: bot, m: Message):
    if not m.from_user:
        return
    if m.from_user.id not in DEV_LEVEL:
        await m.reply_text("Only owner can do it")
        return
    split = m.text.split(None)
    if len(split) < 3 and not (len(split) == 2 and m.reply_to_message):
        await m.reply_text("Use /help to see how to use this command")
        return
    if len(split) == 3:
        try:
            user = int(split[1])
        except ValueError:
            await m.reply_text("Must pass user id")
            return
        try:
            money = int(split[2])
        except ValueError:
            await m.reply_text("Coin should be natural number")
    elif len(split) == 2:
        if not m.reply_to_message.from_user:
            await m.reply_text("This is not an user I guess")
            return
        user = m.reply_to_message.from_user.id
        money = int(split[1])
    User = USERS(user).get_info()
    if not User:
        await m.reply_text("User is not registered in my database")
        return
    f_mon = User["coin"]
    try:
        await bot.send_message(user,f"Owner changed value {COIN_NAME +' '+ COIN_EMOJI} from {f_mon} to {money} 💀")
        USERS(user).set_users_coin(int(money))
        await m.reply_text(f"Successfully changed value of {user}'s {COIN_NAME +' '+ COIN_EMOJI} from {f_mon} to {money} 🗿")
        return
    except Exception:
        await m.reply_text("Tell the user to start the bot first")
        return
    
@bot.on_message(filters.command("donate"))
async def le_le_bhikhari(c: bot, m: Message):
    if not m.from_user:
        return
    split = m.command
    if len(split) != 2:
        await m.reply_text("Use /help to see how to use this command")
        return
    elif len(split) == 2:
        if not m.reply_to_message.from_user:
            await m.reply_text("This is not an user I guess")
            return
        user = m.reply_to_message.from_user.id
        money = abs(int(split[1]))
    from_u = m.from_user.id
    User = USERS(user).get_info()
    if not User:
        await m.reply_text("User is not registered in my database")
        return
    FROM_IN = USERS(from_u).get_info()
    if not FROM_IN:
        await m.reply_text("You are not registered in my database")
        return
    FROM_COIN = FROM_IN["coin"]
    USER_COIN = User["coin"]
    if FROM_COIN < money:
        await m.reply_text(f"You don't have this much {COIN_NAME +' '+ COIN_EMOJI}")
        return
    kb = IKM(
        [
            [
                KB("Yes",f"donate_{from_u}_{money}_{user}"),
                KB("No","donate_nooo")
            ]
        ]
    )
    gettt = money * 0.75
    txt = f"""Are you sure to donate the user {money} {COIN_NAME +' '+ COIN_EMOJI}
Before donation:
    You have : {FROM_COIN} {COIN_NAME +' '+ COIN_EMOJI}
    The user have: {USER_COIN} {COIN_NAME +' '+ COIN_EMOJI}

After donation:
    He/she will get: {gettt} {COIN_NAME +' '+ COIN_EMOJI}
    He/she will have : {gettt + USER_COIN} {COIN_NAME +' '+ COIN_EMOJI}
    You will have: {FROM_COIN - money} {COIN_NAME +' '+ COIN_EMOJI}

Note that the tax is 25% of transfering money i.e. it will be deducted from the money you are giving.
"""
    await m.reply_text(txt,reply_markup=kb)
    
@bot.on_callback_query(filters.regex("^donate_"),18)
async def donation_dedo(c: bot, q: CallbackQuery):
    spli = q.data.split()
    if len(spli) == 3:
        await q.answer("Cancelled")
        await q.edit_message_text("Status:\nCancelled",reply_markup=IKM([[KB("Close","close")]]))
        return
    elif len(spli) == 4:
        from_u = int(spli[1])
        money = int(spli[2])
        user = int(spli[3])
        FROM_IN = USERS(from_u).get_info()
        from_l = FROM_IN["link"]
        GIVE = USERS(user).get_info()
        give_l = GIVE["link"]
        USERS.update_coin(str(from_l), money, True)
        net_worth = money * 0.75
        USERS.update_coin(str(give_l), net_worth)
        await q.answer("DONE ✅")
        await q.edit_message_text("Status:\nComplete",reply_markup=IKM([[KB("Close","close")]]))
        return
@bot.on_message(filters.command(["update", "rename"], pre))
async def rename_f(c: bot,  m: Message):
    if not m.from_user:
        await m.reply_text("Not an user")
        return
    if m.from_user.id != int(DEV):
        await m.reply_text("Only dev can do this")
        return
    try:
        splited = m.text.split(None,1)[1]
    except IndexError:
        await m.reply_text("See help to know how to use this cmd")
        return
    keys = splited.split("|")
    try:
        old = keys[0].strip()
        new = keys[1].strip()
    except IndexError:
        await m.reply_text("See help to know how to use this cmd")
        return
    um = await m.reply_text("Changing key name")
    changed = USERS(m.from_user.id).renamefield(old, new)
    await um.delete()
    await m.reply_text(f"Done\nNumber of modified document = {changed}\nIf it is 0 then there is now such key as {old}")
    return

@bot.on_message(filters.command(["updatedb"], pre))
async def update_db(c: bot, m: Message):
    if not m.from_user:
        await m.reply_text("Not an user")
        return
    if m.from_user.id != int(DEV):
        await m.reply_text("Only dev can do this")
        return
    try:
        key = m.text.split(None,1)[1].strip()
    except IndexError:
        await m.reply_text("See help to know how to use this cmd")
        return
    um = await m.reply_text("Updating value")
    users = USERS.get_all_users()
    if not users:
        await m.reply_text("No collection found")
        return
    for user in users:
        USERS(user).new_key(key)
    await um.delete()
    await m.reply_text(f"Done added a new key with name {key} and value 0")
    return

@bot.on_message(filters.command(["save"], pre))
async def temp_save(c: bot, m: Message):
    if not m.from_user:
        await m.reply_text("Not an user")
        return
    if m.from_user.id not in DEV_LEVEL:
        await m.reply_text("Only owner and sudoer can do that")
        return
    um = await m.reply_text("Exporting users database in new collection")
    data = USERS.get_all_users(True)
    temp = TEMP()
    for i in data:
        temp.save_temp(
            i["user_id"],
            i["coin"]
        )
    await um.delete()
    await m.reply_text(f"Export complete\nType /compensate to give it to all users")

@bot.on_message(filters.command(["compensate"], pre))
async def temp_give_delete(c: bot, m: Message):
    if not m.from_user:
        await m.reply_text("Not an user")
        return
    if m.from_user.id not in DEV_LEVEL:
        await m.reply_text("Only owner and sudoer can do that")
        return
    bot_user = (await bot.get_me()).username
    um = await m.reply_text(f"Giving all users their {COIN_NAME} {COIN_EMOJI} back")
    to_give = TEMP().compensate()
    for i in to_give:
        com_link = f"**Type link before clicking. Otherwise you will not get the coins**.\n[Click Here](t.me/{bot_user}?start=compensate_{i['coin']})\n\nTo get your {COIN_NAME} {COIN_EMOJI} back\nDon't share this link with anyone else. Otherwise they will get your link and you will get nothing"
        kb = IKM(
            [[KB("Compensation",url=f"t.me/{bot_user}?start=compensate_{i['coin']}")]]
        )
        try:
            pin = await bot.send_message(i["user_id"], com_link, reply_markup=kb, disable_web_page_preview=True)
            await bot.pin_chat_message(i["user_id"], pin.id, both_sides=True)
        except Exception:
            pass
    await um.delete()
    await m.reply_text("Done")
        

@bot.on_chat_member_updated(filters.chat(CHAT_ID))
async def coin_increaser(c: bot, u: ChatMemberUpdated):
    if u.new_chat_member:
        try:
            link = u.invite_link.invite_link
            if not link:
                return
            user_joined = u.new_chat_member.user.id
            if not len(info_dict):
                info_dict[f"{link}"] = [user_joined]
                return
            try:
                if user_joined in info_dict[f"{link}"]:
                    return
                info_dict[f"{link}"].append(int(user_joined))
            except KeyError:
                info_dict[f"{link}"] = [user_joined]
            USERS.update_coin(str(link), int(AMOUNT))
            USERS.update_joined(str(link))
            return
        except AttributeError:
            return
spam = {}
blocked = {}
users = USERS.get_all_users()
async def time_for(initial_time):
    if unit == "m":
        bantime = initial_time + timedelta(minutes=int(time_num))
    elif unit == "h":
        bantime = initial_time + timedelta(hours=int(time_num))
    elif unit == "d":
        bantime = initial_time + timedelta(days=int(time_num))
    else:
        bantime = initial_time + timedelta(hours=1)
    return bantime
IST = pytz.timezone('Asia/Kolkata')
@bot.on_message(~filters.bot & filters.user(users) & ~filters.private)
async def message_increaser(c: bot, m: Message):
    if not m.from_user:
        return
    u_id = m.from_user.id
    if len(blocked):
        try:
            till = blocked[u_id]
            if datetime.now(IST) <= till:
                return
            elif datetime.now(IST) > till:
                del blocked[u_id]
                try:
                    await bot.send_message(u_id,"You are unblocked now. Don't do spam anymore otherwise you will be blocked again")
                    return
                except:
                    await m.reply_text("You are unblocked now. Don't do spam anymore otherwise you will be blocked again\nAnd unblock the bot to enjoy features")
                    return
        except KeyError:
            pass
    try:
        x = spam[u_id][1][0]
        y = spam[u_id][1][-1]
        if len(spam[u_id][0]) >= LIMIT:
            if y-x <= WITHIN:
                for_time = await time_for(datetime.now(IST))
                till_time = for_time.strftime("%H:%M:%S")
                till_date = for_time.strftime("%d-%m-%Y")
                await m.reply_text(f"⚠️ You further message will not considered 🚫\nReason : Due to sapm\nYou are blocked till:\n\t📅Date : {till_date}\n\t🕔Time : {till_time}")
                spam[u_id][0].clear()
                spam[u_id][1].clear()
                if not len(blocked):
                    blocked[u_id] = for_time
                    return
                blocked[u_id] = for_time
                return
            else:
                spam[u_id][0].clear()
                spam[u_id][1].clear()
    except (IndexError, KeyError):
        pass
    User = USERS(u_id).get_info()
    mess = User["message"]
    link = User["link"]
    if mess >= NUMBER_MESSAGE:
        try:
            await bot.send_message(u_id, f"Keep chatting and you will again get some {COIN_NAME} after {NUMBER_MESSAGE} messages")
            USERS.update_coin(str(link), int(COIN_MESSAGE))
            USERS(u_id).mess_update(True)
            return
        except Exception as e:
            await bot.send_message(DEV, f"Error\n{e}")
            return
    elif mess < NUMBER_MESSAGE:
        sec = round(time.time())
        if not len(spam):
            spam[u_id] = [["x"],[sec]] # First one is message second one is time
            USERS(u_id).mess_update()
            return
        try:
            spam[u_id][0].append("x")
            spam[u_id][1].append(sec)
        except KeyError:
            spam[u_id] = [["x"],[sec]]
        USERS(u_id).mess_update()
        return
