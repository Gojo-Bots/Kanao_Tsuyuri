help_txt = """
Type /link in the chat to get invite link of the chat.
Per join with you link will reward you some coin, which will further used to buy stuffs.

Note that every /link will command will update the link you have created before in db
and the user joined by that link will not considered as any base to give reward to you

/mylink : To get previous genrated link of the chat by you.

/profile <user id | username> : To get you information.

/owners : Get info of owners

/premium: To get link of premium channel. Works only in private chat

/buy : To buy stuffs. Works only in private chat

**OWNER ONLY**
/addfile : To add file
/rmfile
/addcat <name of CATEGORY should be str | pass nothing> : Add a new CATEGORY
/addowner <reply to user or his id> : Add user to owner list (Only be in list until the bot restarts)
/rmowner <reply to user or his id> : Remove user to owner list (Only be in list until the bot restarts)
/broadcast : Just type broadcast in reply to message to broadcast the message

**NOTE**: Your info will be stored in database when you type /link in the group

**db** standas for **DataBase**
"""