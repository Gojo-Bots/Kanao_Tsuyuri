from pyrogram.types import CallbackQuery
from pyrogram.types import InlineKeyboardMarkup as IKM

from Chimku import *
from Chimku.database.stuffs import STUFF
from Chimku.database.user_info import USERS
from Chimku.utils.keyboard import *

Stuff = STUFF()

@bot.on_message(filters.command(["myreward", "reward", "buy"], pre))
async def rewards(c: bot, m: Message):
    txt = "What you want to buy"
    await m.reply_text(txt, reply_markup=IKM(initial))
    return

@bot.on_callback_query(filters.private)
async def initial_call(c: bot, q: CallbackQuery):
    call = str(q.data)
    try:
        is_present, key = stuff_kb(call)
        if is_present:
            await q.edit_message_text(
                f"Want you want to buy in {call.capitalize()} section", 
                reply_markup=key)
            await q.answer("Buy menu")   
            return
        elif not is_present:
            await q.edit_message_text(
                f"Nothing to buy here.", 
                reply_markup=key)
            await q.answer("Buy menu")
            return
    except Exception as e:
        await q.message.reply_text("Failed to make keyboard. Or edit Message")
        return
    if call == "close":
        try:
            await q.answer("Closing")
            await q.message.delete()
            return
        except Exception as e:
            await q.message.reply_text("Failed to close menu")
            return
    if call == "back":
        try:
            await q.edit_message_text(
                "What you want to buy",
                reply_markup=IKM(initial)
            )
            await q.answer("Initial menu")
            return
        except Exception as e:
            await q.message.reply_text("Failed to change the menu")
            return
    if call == "bback":
        try:
            caption = q.message.text.split(None)
            for i in caption:
                if i.lower in ["flamingo", "vistas", "grammar", "other"]:
                    need = i.lower()
            is_present, key = stuff_kb(need)
            if is_present:
                await q.edit_message_text(
                    f"Want you want to buy in {need} section",
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
        except Exception:
            await q.message.reply_text("Failed to change the menu")
            return
    if call == "purchase":
        User = USERS(q.from_user.id)
        user = User.get_info()
        u_link = str(user["link"])
        u_coin = int(user["coin"])
        caption = q.message.text.split(":")
        name = caption[1].trip().split("\n")[0]
        s_coin = int(Stuff.get_amount(name))
        s_link = str(Stuff.get_file_link(name))
        if u_coin >= s_coin:
            await q.edit_message_reply_markup(IKM(purchased))
            try:
                edit = await q.message.reply_document(s_link)
                USERS.update_coin(u_link, deduct=s_coin)
                await q.answer("Successfully pruchased")
                await edit.reply_text("Here is your delivery.")
                return
            except Exception:
                await q.message.reply_text("Failed to buy")
                return
        else:
            await q.answer("You don't have enough coin", True)
            return

    


@bot.on_callback_query(filters.regex("^call_") & filters.private)
async def buy_menu(c: bot, q: CallbackQuery):
    data = q.data.split("_", 1)[1]
    name = str(data).replace("_", " ")
    file = Stuff.get_file_info(name)
    f_name = file["name"]
    amount = file["ncoin"]
    f_category = file["type"]
    txt = f"""
    Name : {f_name}
    Category : {f_category}
    Amount : {amount}
    """
    key = purchase_kb()
    await q.edit_message_text(txt, reply_markup=key)
    return