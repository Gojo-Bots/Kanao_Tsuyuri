from pyrogram.enums import ChatType as CT
from pyrogram.enums import ParseMode as PM
from pyrogram.types import CallbackQuery, InlineKeyboardButton

"""from pyrogram.raw.functions.account import SetPrivacy
from pyrogram.raw.types import InputPrivacyValueDisallowContacts as IPVDC"""
from pyrogram.types import InlineKeyboardMarkup as IKM

from KeysSecret import *
from Powers import *
from Powers.database.stuffs import STUFF
from Powers.database.user_info import USERS
from Powers.utils.keyboard import *

DEV_LEVEL = SUDO + [OWNER] + [DEV]

@bot.on_message(filters.command(["myreward", "reward", "buy"], pre) & filters.private)
async def rewards(c: bot, m: Message):
    if not m.from_user:
        await m.reply_text("Not an user")
        return
    txt = "What you want to buy"
    await m.reply_text(txt, reply_markup=initial_kb())
    return

@bot.on_message(filters.command("typecat",pre))
async def list_cat_types(c:bot, m:Message):
    if not m.from_user:
        await m.reply_text("Not an user")
        return
    Category = CATEGORY
    for i in list(stuff.file_sorted()):
        Category.append(i)
    catss = ""
    catss += '\n'.join(Category)
    txt = f"Available categories\n{catss}"
    await m.reply_text(txt)
    return

@bot.on_message(filters.command(["rmcat"], pre))
async def remove_file_cat(c:bot, m: Message):
    if not m.from_user:
        await m.reply_text("Not an user")
        return
    if m.from_user.id not in DEV_LEVEL:
        await m.reply_text("You can't do that")
        return
    split = m.text.split()
    if len(split) != 2:
        await m.reply_text("**USAGE**\n/rmcat [category name]")
        return
    to_rm = split[1].lower()
    x = STUFF().remove_category(to_rm)
    if x:
        await m.reply_text(f"Done\n{x}")
        return
    await m.reply_text("No category found with the given one")
    return

@bot.on_message(filters.command(["rmfile", "removefile"], pre))
async def rem_file(c:bot , m: Message):
    if not m.from_user:
        await m.reply_text("Not an user")
        return
    if m.from_user.id not in DEV_LEVEL:
        await m.reply_text("Owner and sudoer command!")
        return
    txt = "What you want to remove"
    await m.reply_text(txt, reply_markup=initial_kb(remove=True))
    return   

@bot.on_callback_query(filters.regex(r"^buy_(.*)$") | filters.regex(r"^rmbuy_(.*)$"), 0)
async def initial_call(c: bot, q: CallbackQuery):
    if q.message.chat.type != CT.PRIVATE:
        return
    call = str(q.data).split("_",1)[1]
    rem = False
    if str(q.data).split("_",1)[0] == "rmbuy":
        rem = True
    try:
        is_present, key = stuff_kb(call, remove=rem)
        if is_present:
            await q.edit_message_text(
                f"What you want to {'buy' if not rem else 'remove'} in {call.capitalize()} section", 
                reply_markup=key)
            await q.answer("Buy menu")   
            return
        else:
            await q.edit_message_text(
                f"Nothing to {'buy' if not rem else 'remove'} here.", 
                reply_markup=key)
            await q.answer("Buy menu")
            return
    except Exception as e:
        await q.message.reply_text(f"Failed to make keyboard. Or edit Message due to\n{e}")
        print(e)
        return


@bot.on_callback_query(group=69)
async def initial_call(c: bot, q: CallbackQuery):
    if q.message.chat.type != CT.PRIVATE:
        return
    Stuff = STUFF()
    call = str(q.data)
    if call == "close":
        try:
            await q.answer("Closing")
            await q.message.delete()
            return
        except Exception as e:
            await q.message.reply_text("Failed to close menu")
            print(e)
            return
    elif call == "back":
        try:
            await q.edit_message_text(
                "What you want to buy",
                reply_markup=initial_kb()
            )
            await q.answer("Initial menu")
            return
        except Exception as e:
            await q.edit_message_text(f"Failed to change the menu due to\n{e}")
            print(e)
            return
    elif call == "rmback":
        try:
            await q.edit_message_text(
                "What you want to remove",
                reply_markup=initial_kb(remove=True)
            )
            await q.answer("Initial menu")
            return
        except Exception as e:
            await q.edit_message_text(f"Failed to change the menu due to\n{e}")
            print(e)
            return
    else:
        raise ContinuePropagation

@bot.on_callback_query(filters.regex(r"^rmbback_(.*)$") | filters.regex(r"^bback_(.*)$"),1)
async def after_rm_back(c:bot, q: CallbackQuery):
    call,need = q.data.split("_",1)
    if call == "rmbback":
        try:
            is_present, key = stuff_kb(need, remove=True)
            if is_present:
                await q.edit_message_text(
                    f"What you want to remove in {need} section",
                    reply_markup=key
                )
                await q.answer("Buy menu")
                return
            elif not is_present:
                await q.edit_message_text(
                f"Nothing to buy here.", 
                reply_markup=key)
            await q.answer("Buy menu")
            return
        except Exception as e:
            await q.message.reply_text(f"Failed to change the menu due to\n{e}")

            return
    if call == "bback":
        try:
            is_present, key = stuff_kb(need)
            if is_present:
                await q.edit_message_text(
                    f"What you want to buy in {need} section",
                    reply_markup=key
                )
                await q.answer("Buy menu")
                return
            elif not is_present:
                await q.edit_message_text(
                f"Nothing to buy here.", 
                reply_markup=key)
            await q.answer("Buy menu")
            return
        except Exception as e:
            await q.message.reply_text(f"Failed to change the menu due to\n{e}")

            return
@bot.on_callback_query(filters.regex(r"^want_(.*)$") | filters.regex(r"^rmwant_(.*)$"),2)
async def initial_call(c: bot, q: CallbackQuery):
    if q.message.chat.type != CT.PRIVATE:
        return
    Stuff = STUFF()
    split = q.data.split("_",1)[-1]
    data = split.split("/")[0]
    data2 = split.split("/",1)[-1].replace("_", " ")
    required = Stuff.get_file_info(data2,data)
    if not required:
        data2 = split.split("/",1)[-1].replace(" ", "_")
        required = Stuff.get_file_info(data2,data)
    s_file = required["f_id"]
    if q.data.split("_",1)[0] == "rmwant":
        Stuff.remove_file(s_file)
        await q.edit_message_text("Removed the file", reply_markup=IKM(purchased_kb(data, True)))
        await q.answer("Removed")
        return
    if True:
        User = USERS(q.from_user.id)
        user = User.get_info()
        if not user:
            await q.edit_message_text("You don't have any link genrated. Type /link first")
            return
        u_link = str(user["link"])
        u_coin = int(user["coin"])
        s_coin = int(required["ncoin"])
        s_type = str(required["file_type"])
        if u_coin >= s_coin:
            """privacy_settings = IPVDC()
            await bot.invoke(
                SetPrivacy(
                    key = privacy_settings,
                    rules =[]
                )
            )"""
            await q.edit_message_reply_markup(IKM(purchased_kb(data)))
            try:
                c_id = q.message.chat.id
                await q.message.delete()
                if s_type == "document":
                    await bot.send_document(c_id,s_file,caption="Here is your delivery",protect_content=True)
                elif s_type == "video":
                    await bot.send_video(c_id,s_file,caption="Here is your delivery",protect_content=True)
                elif s_type == "photo":
                    await bot.send_photo(c_id,s_file,caption="Here is your delivery",protect_content=True)
                elif s_type == "video_note":
                    await bot.send_video_note(c_id,s_file,caption="Here is your delivery",protect_content=True)
                elif s_type == "animation":
                    await bot.send_animation(c_id,s_file,caption="Here is your delivery",protect_content=True)
                    USERS.update_coin(u_link, deduct=True)
                elif s_type == "text":
                    await bot.send_message(c_id,s_file,protect_content=True,disable_web_page_preview=True,parse_mode=PM.MARKDOWN)
                    USERS.update_coin(u_link, deduct=True)
                elif s_type == "link":
                    invite = await bot.create_chat_invite_link(int(s_file),member_limit=1)
                    await bot.send_message(c_id,invite.invite_link,protect_content=True)
                await q.answer("Successfully pruchased")
                USERS.update_coin(str(u_link), int(s_coin), True)
                return
            except Exception as e:
                await q.message.reply_text("Failed to buy")
                print(e)
                return
        else:
            await q.answer("You don't have enough coin", True)
            return

@bot.on_message(filters.command(["premium"], pre) & filters.private) 
async def premium_channel(c: bot, m: Message):
    if not m.from_user:
        await m.reply_text("Not an user")
        return
    if not PREMIUM_CHANNEL:
        await m.reply_text("Premium channel is not available.")
        return
    u_id = m.from_user.id
    Users = USERS(u_id).get_info()
    if not Users:
        await m.reply_text("Type /link to get registered in my db first")
        return
    u_coin = int(Users["coin"])
    if u_coin >= PREMIUM_COST:
        c_link = (await bot.create_chat_invite_link(int(PREMIUM_CHANNEL), member_limit=1)).invite_link
        join_chat = IKM(
            [[
                InlineKeyboardButton("✨ Click here to join", url=f"{c_link}")
            ]]
        )
        await m.reply_text(f"Here is the invite link for the premium channel:\n[Click Here]({c_link})", reply_markup=join_chat, disable_web_page_preview=True)
        u_link = str(Users["link"])
        USERS.update_coin(str(u_link), int(PREMIUM_COST), True)
        return
    else:
        await m.reply_text(
            f"You Don't have enough {COIN_NAME + ' ' + COIN_EMOJI} to get the link.\nYou need **{PREMIUM_COST - u_coin}** more to get premium channel invite link\n💰 Premium chat cost: {PREMIUM_COST} {COIN_NAME + ' ' + COIN_EMOJI}\n🧿 You have: {u_coin} {COIN_NAME + ' ' + COIN_EMOJI}")
        return

@bot.on_callback_query(filters.regex(r"^premium_link$"), 3)
async def premium_link(c: bot, q: CallbackQuery):
    u_id = q.from_user.id
    Users = USERS(u_id).get_info()
    if not Users:
        await q.message.reply_text("Type /link to get registered in my db first")
        return
    u_coin = int(Users["coin"])
    if u_coin >= PREMIUM_COST:
        c_link = (await bot.create_chat_invite_link(int(PREMIUM_CHANNEL), member_limit=1)).invite_link
        join_chat = IKM(
            [[
                InlineKeyboardButton("✨ Click here to join", url=f"{c_link}")
            ],
            [
                InlineKeyboardButton("⬅️ Back", "back"),
                InlineKeyboardButton("❌ Close", "close")
            ]]
        )
        await q.edit_message_text(f"Here is the invite link for the premium channel:\n[Click Here]({c_link})", reply_markup=join_chat, disable_web_page_preview=True)
        u_link = str(Users["link"])
        USERS.update_coin(str(u_link), int(PREMIUM_COST), True)
        return
    else:
        back_btn = IKM(
            [
                [
                    InlineKeyboardButton("⬅️ Back", "back"),
                    InlineKeyboardButton("❌ Close", "close")
                ]
            ]
        )
        await q.edit_message_text(
            f"You Don't have enough {COIN_NAME + ' ' + COIN_EMOJI} to get the link.\nYou need **{PREMIUM_COST - u_coin}** more to get premium channel invite link\n💰 Premium chat cost: {PREMIUM_COST} {COIN_NAME + ' ' + COIN_EMOJI}\n🧿 You have: {u_coin} {COIN_NAME + ' ' + COIN_EMOJI}", reply_markup=back_btn)
        return

@bot.on_callback_query(filters.regex(r"^call_(.*)$") | filters.regex(r"^rmcall_(.*)$"), 4)
async def buy_menu(c: bot, q: CallbackQuery):
    if q.message.chat.type != CT.PRIVATE:
        return
    Stuff = STUFF()
    split = q.data.split("_",1)
    rsplit = q.data.split("/",1)
    ftype = split[-1].split("/")[0]
    data = rsplit[-1]
    name = str(data).replace("_", " ")
    file = Stuff.get_file_info(name,ftype)
    if not file:
        name = str(data).replace(" ", "_")
        file = Stuff.get_file_info(name,ftype)
        if not file:
            dev = (await bot.get_users(DEV)).username
            await q.edit_message_text(f"Error occured\nreport it to {dev}")
            return
    f_name = file["name"].lower().capitalize()
    amount = file["ncoin"]
    f_category = file["type"]
    txt = f"""
Name : {f_name}
CATEGORY : {f_category}
Amount : {amount}
    """
    key = purchase_kb(q.data.split("_",1)[-1], ftype)
    if split[0] == "rmcall":
        key = remove_kb(q.data.split("_",1)[-1], ftype)
    await q.edit_message_text(txt, reply_markup=key)
    return
