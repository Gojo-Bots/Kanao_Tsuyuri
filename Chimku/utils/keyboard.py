from pyrogram.types import InlineKeyboardButton as KB

from Chimku.database.stuffs import STUFF

stuff = STUFF()

initial = [
    [
        KB("Flamingo", "flamingo"),
        KB("Vistas", "vistas")
    ],
    [
        KB("Grammar", "grammar"),
        KB("Others", "other")
    ]
]

