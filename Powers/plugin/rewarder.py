from pyrogram.types import CallbackQuery, InlineKeyboardButton
from pyrogram.enums import ChatType as CT
"""from pyrogram.raw.functions.account import SetPrivacy
from pyrogram.raw.types import InputPrivacyValueDisallowContacts as IPVDC"""
from pyrogram.types import InlineKeyboardMarkup as IKM

from Powers import *
from Powers.database.stuffs import STUFF
from Powers.database.user_info import USERS
from Powers.utils.keyboard import *



@bot.on_message(filters.command(["myreward", "reward", "buy"], pre) & filters.private)
async def rewards(c: bot, m: Message):
    txt = "What you want to buy"
    await m.reply_text(txt, reply_markup=initial_kb())
    return

@bot.on_callback_query(filters.regex("^buy_"), 0)
async def initial_call(c: bot, q: CallbackQuery):
    if q.message.chat.type != CT.PRIVATE:
        return
    call = str(q.data).split("_")[1]
    try:
        is_present, key = stuff_kb(call)
        if is_present:
            await q.edit_message_text(
                f"What you want to buy in {call.capitalize()} section", 
                reply_markup=key)
            await q.answer("Buy menu")   
            return
        else:
            await q.edit_message_text(
                f"Nothing to buy here.", 
                reply_markup=key)
            await q.answer("Buy menu")
            return
    except Exception as e:
        await q.message.reply_text(f"Failed to make keyboard. Or edit Message due to\n{e}")
        print(e)
        return


@bot.on_callback_query(group=1)
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
    if call == "back":
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
    if call == "bback":
        try:
            caption = q.message.text.split(None)
            for i in caption:
                if i.lower() in CATEGORY:
                    need = i.lower()
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
@bot.on_callback_query(filters.regex("^want_"),group=4)
async def initial_call(c: bot, q: CallbackQuery):
    if q.message.chat.type != CT.PRIVATE:
        return
    Stuff = STUFF()
    data = q.data.split("_",1)[-1]
    name = str(data).replace("_", " ")
    if True:
        User = USERS(q.from_user.id)
        user = User.get_info()
        if not user:
            await q.edit_message_text("You don't have any link genrated. Type /link first")
            return
        u_link = str(user["link"])
        u_coin = int(user["coin"])
        s_coin = int(Stuff.get_amount(name))
        s_file = str(Stuff.get_file_link(name)[0])
        s_type = str(Stuff.get_file_link(name)[1])
        if u_coin >= s_coin:
            """privacy_settings = IPVDC()
            await bot.invoke(
                SetPrivacy(
                    key = privacy_settings,
                    rules =[]
                )
            )"""
            await q.edit_message_reply_markup(IKM(purchased))
            try:
                if s_type == "document":
                    await q.message.reply_document(s_file, caption="Here is your delivery")
                elif s_type == "video":
                    await q.message.reply_video(s_file, caption="Here is your delivery")
                elif s_type == "photo":
                    await q.message.reply_photo(s_file, caption="Here is your delivery")
                elif s_type == "video_note":
                    await q.message.reply_video_note(s_file, caption="Here is your delivery")
                elif s_type == "animation":
                    await q.message.reply_animation(s_file, caption="Here is your delivery")
                    USERS.update_coin(u_link, deduct=True)
                await q.answer("Successfully pruchased")
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
    u_id = m.from_user.id
    Users = USERS(u_id).get_info()
    u_coin = int(Users["coin"])
    if u_coin >= PREMIUM_COST:
        c_link = (await bot.create_chat_invite_link(int(PREMIUM_CHANNEL), member_limit=1)).invite_link
        join_chat = IKM(
            [[
                InlineKeyboardButton("Click here to join", url=f"{c_link}")
            ]]
        )
        await m.reply_text(f"Here is the invite link for the premium channel:\n[Click Here]({c_link})", reply_markup=join_chat, disable_web_page_preview=True)
        return
    else:
        await m.reply_text(
            f"You Don't have enough coin to get the link.\nYou need **{PREMIUM_COST - u_coin}** more to get premium channel invite link\n💰 Premium chat cost: {PREMIUM_COST}\n🧿 You have: {u_coin}")
        return

@bot.on_callback_query(filters.regex("^premium_link$"), 3)
async def premium_link(c: bot, q: CallbackQuery):
    u_id = q.from_user.id
    Users = USERS(u_id).get_info()
    u_coin = int(Users["coin"])
    if u_coin >= PREMIUM_COST:
        c_link = (await bot.create_chat_invite_link(int(PREMIUM_CHANNEL), member_limit=1)).invite_link
        join_chat = IKM(
            [[
                InlineKeyboardButton("Click here to join", url=f"{c_link}")
            ],
            [
                InlineKeyboardButton("Back", "back"),
                InlineKeyboardButton("Close", "close")
            ]]
        )
        await q.edit_message_text(f"Here is the invite link for the premium channel:\n[Click Here]({c_link})", reply_markup=join_chat, disable_web_page_preview=True)
        return
    else:
        back_btn = IKM(
            [
                [
                    InlineKeyboardButton("Back", "back"),
                    InlineKeyboardButton("Close", "close")
                ]
            ]
        )
        await q.edit_message_text(
            f"You Don't have enough coin to get the link.\nYou need **{PREMIUM_COST - u_coin}** more to get premium channel invite link\n💰 Premium chat cost: {PREMIUM_COST}\n🧿 You have: {u_coin}", reply_markup=back_btn)
        return

@bot.on_callback_query(filters.regex("^call_"), 2)
async def buy_menu(c: bot, q: CallbackQuery):
    if q.message.chat.type != CT.PRIVATE:
        return
    Stuff = STUFF()
    data = q.data.split("_",1)[-1]
    name = str(data).replace("_", " ")
    file = Stuff.get_file_info(name)
    f_name = file["name"].lower().capitalize()
    amount = file["ncoin"]
    f_category = file["type"]
    txt = f"""
Name : {f_name}
CATEGORY : {f_category}
Amount : {amount}
    """
    key = purchase_kb(data)
    await q.edit_message_text(txt, reply_markup=key)
    return
