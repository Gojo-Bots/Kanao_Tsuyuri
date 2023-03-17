from pyrogram.enums import ChatType as CT
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
    owner_user = (await bot.get_users(OWNER)).username
    if m.chat.type == CT.PRIVATE:
        if len(m.text.split()) > 1:
            option = (m.text.split(None, 1)[1]).lower()
            if option.startswith("compensate"):
                coins = int(m.text.split("_", 1)[1])
                Users = USERS(m.from_user.id).give_coin(coins)
                if not Users:
                    await m.reply_text(f"Failed to give {COIN_NAME} {COIN_EMOJI}\nType /link and try again")
                    return
                TEMP().drop_collection(m.from_user.id)
                await m.reply_text(f"You got your {COIN_NAME} {COIN_EMOJI} back")
                return
    txt = f"Hi! {m.from_user.mention}\nDo /help to know what I can do."
    if m.chat.type == CT.PRIVATE:
        await bot.send_message(m.chat.id, txt, reply_markup=help_kb(owner_user))
        return
    else:
        await m.reply_text(txt,reply_markup=help_kb(owner_user))
        return
@bot.on_callback_query(filters.regex("^menu_"), group=-1)
async def help_menu_back(c: bot, q: CallbackQuery):
    data = q.data.split("_")[-1]
    owner_user = (await bot.get_users(OWNER)).username
    if data == "help":
        await q.answer("Help menu")
        await q.edit_message_text(help_txt, reply_markup=back_kb)
        return
    elif data == "back":
        await q.answer("Back")
        await q.edit_message_text(f"Hi! {q.message.from_user.mention}\nDo /help to know what I can do.", reply_markup=help_kb(owner_user))
        return

@bot.on_message(filters.command(["help"], pre))
async def help_(c: bot, m: Message):
    await m.reply_text(help_txt, reply_markup=back_kb)
    return
@bot.on_message(filters.command(["addowner"], pre))
async def owner_add(c: bot, m: Message):
    if m.from_user.id not in OWNER_ID:
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
    OWNER_ID.append(user)
    await m.reply_text(f"Added user id `{user}` to owner's list")
    return
@bot.on_message(filters.command(["rmowner"], pre))
async def owner_rm(c: bot, m: Message):
    if m.from_user.id not in OWNER:
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
    for i in OWNER_ID:
        if user == i:
            OWNER_ID.remove(i)
    await m.reply_text("Removed the user")

@bot.on_message(filters.command(["owners"], pre))
async def owners_info(c: bot, m: Message):
    try:
        infos = await bot.get_users(OWNER_ID)
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
    User = USERS(m.from_user.id)
    link = User.get_link()
    if link:
        await m.reply_text(f"Here is your link:\n`{link}`")
        return
    await m.reply_text("Seems link you are not registered in my db\nType /link to get registered")
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
                    try:
                        user = (await bot.get_users(split[1].split("/")[-1])).id
                    except:
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
    if m.from_user.id not in OWNER_ID:
        await m.reply_text("You can't do that")
        return
    if len(m.text.split(None,1)) == 2:
        CATEGORY.append(str(m.text.split(None,1)[1].replace(" ", "_").lower()))
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
        CATEGORY.append(str(x.text.replace(" ", "_").lower()))

        await m.reply_text(f"Added {x.text.capitalize()} to CATEGORY")
        return

@bot.on_message(filters.command(['forward'], pre))
async def forwarder(c:bot, m: Message):
    if m.from_user.id not in OWNER_ID:
        await m.reply_text("You can't do that")
        return
    if not m.reply_to_message:
        await m.reply_text("Reply to a message to forward it")
        return
    users = USERS.get_all_users()
    i = 0
    um = await m.reply_text("Forwarding the message")
    for user in users:
        try:
            await bot.forward_messages(int(user), m.chat.id, m.reply_to_message_id)
        except Exception:
            i += 1
            pass
    
    await um.delete()
    if i == len(users):
        await m.reply_text("Failed to forward message")
    await m.reply_text(f"Successfully forwardeded the message to {len(users) - i} out of {len(users)} users")
    return

async def help_broadcast(file,m_id):
    users = USERS.get_all_users()
    i = 0
    for user in users:
        try:
            if file.animation:
                await bot.send_animation(int(user),m_id)
            elif file.photo:
                await bot.send_photo(int(user),m_id)
            elif file.video:
                await bot.send_video(int(user),m_id)
            elif file.document:
                await bot.send_document(int(user),m_id)
            else:
                i = "Unsupported file type"
        except Exception:
            i += 1
            pass
    return i, len(users)

@bot.on_message(filters.command(["broadcast"], pre))
async def broadcaster(c: bot, m: Message):
    if m.from_user.id not in OWNER_ID:
        await m.reply_text("You can't do that")
        return
    if m.chat.type != CT.PRIVATE:
        await m.reply_text("Meant to be used in private.....however you can use /forward in chats")
        return
    if m.reply_to_message:
        reply_to = m.reply_to_message
        file = m.reply_to_message_id
        um = await m.reply_text("Broadcasting message...")
        x, y = await help_broadcast(reply_to, file)
        
        await um.delete()
        if type(i) == str:
            await m.reply_text(i)
            return
        suc = y-x
        if not suc:
            await m.reply_text("Failed to broadcast the message.")
            return
        await m.reply_text(f"Successfully broadcasted message to {suc} users out of {y} users")
        return
    else:
        file = await bot.ask(
            text = "Send me the file\nType /cancel to abort the operation",
            chat_id = m.from_user.id
            )
        z = await bot.send_message(m.chat.id,"File recived hold tight will I fetch data and broadcast it")
        if is_cancel(file.text):
            await bot.send_message(m.chat.id,"Aborted the task")
            return
        mess = await bot.get_messages(m.chat.id,z.id-1)
        m_id = mess.id
        await z.delete()
        await file.delete()
        um = await m.reply_text("Broadcasting message...")
        x = await help_broadcast(mess,m_id)
        await um.delete()
        if type(i) == str:
            await m.reply_text(i)
            return
        suc = y-x
        if not suc:
            await m.reply_text("Failed to broadcast the message.")
            return
        await m.reply_text(f"Successfully broadcasted message to {suc} users out of {y} users")
        return
       
@bot.on_message(filters.command(["gift"], pre))
async def gift_one(c: bot, m: Message):
    if m.from_user.id != OWNER:
        await m.reply_text("Only owner can do it")
        return
    split = m.text.split(None)
    if len(split) < 3 and not (len(split) == 2 and m.reply_to_message):
        await m.reply_text("Use /help to see how to use this command")
        return
    COIN_NAME = COIN_NAME +" "+ COIN_EMOJI
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
        owner = (await bot.get_users(OWNER)).mention
        try:
            await bot.send_message(user,f"{owner} of the bot gave you {money} {COIN_NAME}  enjoy🎉")
            USERS.update_coin(str(link), money)
            await m.reply_text(f"Successfully given {user} {money} {COIN_NAME}")
            return
        except Exception:
            await m.reply_text("Tell the user to start the bot first")
            return
    if len(split) == 2:
        user = m.reply_to_message.from_user.id
        money = split[1]
        try:
            money = abs(int(split[1]))
        except ValueError:
            await m.reply_text("Coin should be natural number")
        User = USERS(user).get_info()
        link = User["link"]
        try:
            await bot.send_message(user,f"{owner} of the gave you {money} {COIN_NAME} enjoy🎉")
            USERS.update_coin(str(link), money)
            await m.reply_text(f"Successfully given {user} {money} {COIN_NAME}")
            return
        except Exception:
            await m.reply_text("Tell the user to start the bot first")
            return

@bot.on_message(filters.command(["giftall"], pre))
async def gift_all(c: bot, m: Message):
    if m.from_user.id != OWNER:
        await m.reply_text("Only owner can do it")
        return
    split = m.text.split(None)
    COIN_NAME = COIN_NAME +" "+ COIN_EMOJI
    if len(split) != 2:
        await m.reply_text("Type /help to see how")
        return
    try:
        money = abs(int(split[1]))
    except ValueError:
        await m.reply_text("Coin should be natural number")
        return
    users = USERS.get_all_users()
    links = {}
    for user in users:
        User = USERS(user).get_info()
        link = User["link"]
        links[user] = str(link)
    um = await m.reply_text(f"Trying to give all users {money} {COIN_NAME}")
    l = 0
    owner = (await bot.get_users(OWNER)).mention
    try:
        for i,j in links.items():
            await bot.send_message(int(i), f"{owner} of the bot gave you {money} {COIN_NAME} enjoy🎉")
            USERS.update_coin(j,money)
    except Exception:
        l+=1
        pass
    await um.delete()
    if l == len(links):
        await m.reply_text("Failed to give any user gifts.")
        return
    await m.reply_text(f"Successfully given {len(links) - l} out of {len(links)} users {money} {COIN_NAME}")
    return

@bot.on_message(filters.command(["addfile"], pre) & filters.private)
async def file_adder(c: bot, m: Message):
    if m.from_user.id not in OWNER_ID:
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
        text = "Send me the file\nType /cancel to abort the operation",
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
    else:
        x = await x.edit_text("Unsupported file type provided")
        return
    x = await x.edit_text("File id received")
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
    for i in sorted(list(set(CATEGORY))):
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

        if str(f_type).lower() not in CATEGORY:
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
        elif str(f_type).lower() in CATEGORY:
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

@bot.on_message(filters.command(["update", "rename"], pre))
async def rename_f(c: bot,  m: Message):
    if m.from_user.id != int(DEV):
        await m.reply_text("Only dev can do this")
        return
    try:
        splited = m.text.split(None,1)[1]
    except IndexError:
        await m.reply_text("See help to know how to use this cmd")
        return
    keys = splited.split("|").strip()
    try:
        old = keys[0]
        new = keys[1]
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
    if m.from_user.id not in OWNER_ID:
        await m.reply_text("Only owner and sudoer can do that")
        return
    um = await m.reply_text("Exporting users database in new collection")
    data = USERS.get_all_users()
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
    if m.from_user.id not in OWNER_ID:
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
            await bot.send_message(i["user_id"], com_link, reply_markup=kb)
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

users = USERS.get_all_users()
@bot.on_message(~filters.bot & filters.user(users) & ~filters.private)
async def message_increaser(c: bot, m: Message):
    u_id = m.from_user.id
    User = USERS(u_id)
    mess = User["message"]
    link = User["link"]
    if mess >= NUMBER_MESSAGE:
        try:
            await bot.send_message(u_id, f"Keep chatting and you will again get some {COIN_NAME} after {NUMBER_MESSAGE} messages")
            USERS.update_coin(str(link), int(COIN_MESSAGE))
            User.mess_update(True)
            return
        except Exception:
            return
    elif mess <= NUMBER_MESSAGE:
        User.mess_update()
        return
