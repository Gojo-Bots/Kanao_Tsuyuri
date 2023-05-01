from KeysSecret import COIN_EMOJI, COIN_MESSAGE, COIN_NAME, NUMBER_MESSAGE

help_txt = f"""
Type /link in the chat to get invite link of the chat.
Per join with you link will reward you some coin, which will further used to buy stuffs.

Note that every /link will command will update the link you have created before in db
and the user joined by that link will not considered as any base to give reward to you

/mylink : To get previous genrated link of the chat by you.

/profile <user id | username> : To get you information.

/owners : Get info of owners

/premium: To get link of premium channel. Works only in private chat

/buy : To buy stuffs. Works only in private chat

/typecat : To get list of all existing categories

/donate <reply to user> <amount> : Give the given amount to the user which is replied to. Taxes are set to 25%

**YOU WILL GET {COIN_MESSAGE} {COIN_NAME + " " + COIN_EMOJI} WHEN YOU SEND {NUMBER_MESSAGE} IN THE CHAT**

**OWNER ONLY**
/addfile : To add file

/rmfile

/rmcat <category name> : Remove the given category

/addcat <name of CATEGORY should be str | pass nothing> : Add a new CATEGORY

/addowner <reply to user or his id> : Add user to owner list (Only be in list until the bot restarts)

/rmowner <reply to user or his id> : Remove user to owner list (Only be in list until the bot restarts)

/broadcast : Just type broadcast in reply to message to broadcast the message | or just type broadcast (Meant to be used in ib of bot)

/forward : Same method to use as broadcast and same function too but send message with a forward tag

/gift <user_id> <amount> : Give coin to user if you are replying to user don't pass user_id else the coin will be given to passed user not the tagged one.

/giftall <amount> : Give coin to all current users

/save : Save all the collection in a temp collection

/setvalue <user_id | reply to user> <amount> : To set value of user

/compensate : Give the coins to all the users saved in temp collection

**DEVS ONLY**
/update <old key>|<new key> : Change the key name through out the database. Use at your own risk.

/updatedb <new key> : Insert a new key in all the collections. Use at your own risk.

**NOTE**: Your info will be stored in database when you type /link in the group

**IF YOU USE `/save` AND DELETE ALL COLLECTIONS THEN MAKE SURE TO TELL THE USERS TO GENRATE NEW LINK. OTHERWISE `/compensate` WILL NOT WORK**

**db** standas for **DataBase**
"""