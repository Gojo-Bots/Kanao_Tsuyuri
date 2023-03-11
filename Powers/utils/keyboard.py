from pyrogram.types import InlineKeyboardButton as KB, InlineKeyboardMarkup as IKM

from KeysSecret import *
from Powers.database.stuffs import STUFF

stuff = STUFF()


yes_no = [[
    KB("✅ Yes", "new_yus"),
    KB("🚫 No", "new_noi")
]]
def help_kb(owner_username):
    help_kb = [
        [
            KB("📚 Help", "help")
        ],
        [
            KB("👑 Owner", url = f"https://{owner_username}.t.me/"),
            KB("⚡️ Powered By", url = "https://gojo_bots_network.t.me")
        ],

    ]
    return IKM(help_kb)

def arranger_kb(values):
    cmds = sorted(list(values))
    kb = [cmd.lower() for cmd in cmds]
    return [kb[i : i + 3] for i in range(0, len(kb), 3)]

def initial_kb_gen(text, value, type="callback_data"):
    return KB(text, **{type: value})

def initial_kb(remove: bool = False):
    Category = CATEGORY
    for i in list(stuff.file_sorted()):
        Category.append(i)
    rows = arranger_kb(set(Category))
    key = []
    if Category:
        for i in rows:
            line = []
            for j in i:
                if j.split("_"):
                    line.append(
                        initial_kb_gen(str(j).replace("_", " ").capitalize(), f"{'buy' if not remove else 'rmbuy'}_{str(j).lower()}")
                        )
                elif not j.split("_"):
                    line.append(initial_kb_gen(str(j).capitalize(), f"{'buy' if not remove else 'rmbuy'}_{str(j).lower()}"))
            key.append(line)
    if not remove:
        key.extend([
            [
                KB("❤️‍🔥 Premium Channel", "premium_link")
            ],
            [
                KB("❌ Close", "close")
            ]
            ])
    return IKM(key)

def stuff_kb(needed: str, remove: bool = False):
    req = needed.lower()
    files = STUFF().get_files(req)
    if files:
        media_kb = []
        x = arranger_kb(list(files))
        for i in x:
            line = []
            for j in i:
                if j.split(None):
                    line.append(
                        initial_kb_gen(str(j).capitalize(), f"{'call' if not remove else 'rmcall'}_{str(j).lower().replace(' ', '_')}")
                    )
                elif not j.split(None):
                    line.append(
                        initial_kb_gen(str(j).capitalize(), f"{'call' if not remove else 'rmcall'}_{str(j).lower()}")
                    )
            media_kb.append(line)
        media_kb.extend(
            [[
            KB("⬅️ Back", f"{'back' if not remove else 'rmback'}"),
            KB("❌ Close", "close")
            ]]
        )
        return True, IKM(media_kb)
    else:
        media_kb = [
            [
                KB("⬅️ Back", f"{'back' if not remove else 'rmback'}"), # This back will genrate initial menu
                KB("❌ Close", "close")
            ]
            ]
        return False, IKM(media_kb)

def purchase_kb(name):
    purchase = [
        [KB("💠 Purchase", f"want_{name}")],
        [KB("❌ Close", "close"),
        KB("⬅️ Back", "bback")] #This back will genrate the buy menu again
        ]
    return IKM(purchase)

def remove_kb(name):
    purchase = [
        [KB("🗑 Remove", f"rmwant_{name}")],
        [KB("⬅️ Back", "rmbback"),KB("❌ Close", "close")] #This back will genrate the buy menu again
        ]
    return IKM(purchase)

purchased = [
    [
        KB("⬅️ Back", "bback"),
        KB("❌ Close", "close")
    ]
]
