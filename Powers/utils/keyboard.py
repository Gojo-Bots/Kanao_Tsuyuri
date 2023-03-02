from pykeyboard import InlineButton as ib
from pykeyboard import InlineKeyboard as ikb
from pyrogram.types import InlineKeyboardButton as KB, InlineKeyboardMarkup as IKM

from KeysSecret import *
from Powers.database.stuffs import STUFF

stuff = STUFF()


yes_no = [[
    KB("Yes", "new_yus"),
    KB("No", "new_noi")
]]

def arranger_kb(values):
    cmds = sorted(list(values))
    kb = [cmd.lower() for cmd in cmds]
    return [kb[i : i + 3] for i in range(0, len(kb), 3)]

def initial_kb_gen(text, value, type="callback_data"):
    return KB(text, **{type: value})

def initial_kb():
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
                        initial_kb_gen(str(j).replace("_", " ").capitalize(), f"buy_{str(j).lower()}")
                        )
                elif not j.split("_"):
                    line.append(initial_kb_gen(str(j).capitalize(), f"buy_{str(j).lower()}"))
            key.append(line)     
    key.extend([
        [
            KB("Premium Channel", "premium_link")
        ],
        [
            KB("Close", "close")
        ]
        ])
    return IKM(key)

def stuff_kb(needed: str):
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
                        initial_kb_gen(str(j).capitalize(), f"call_file_{str(j).lower().replace(' ', '_')}")
                    )
                elif not j.split(None):
                    line.append(
                        initial_kb_gen(str(j).capitalize(), f"call_{str(j).lower()}")
                    )
            media_kb.append(line)
        media_kb.extend(
            [[
            KB("Back", "back"),
            KB("Close", "close")
            ]]
        )
        return True, IKM(media_kb)
    else:
        media_kb = [
            [
                KB("Back", "back"), # This back will genrate initial menu
                KB("Close", "close")
            ]
            ]
        return False, IKM(media_kb)

def purchase_kb():
    purchase = ikb()
    purchase.row(
        ib("Purchase", "purchase")
    )
    purchase.row(
        ib("Close", "close"),
        ib("Back", "bback") #This back will genrate the buy menu again
    )
    return purchase

purchased = [
    [
        KB("Back", "bback")
    ],
    [
        KB("Close", "close")
    ]
]
