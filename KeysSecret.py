"""
If you are deploying it locally then follow following steps:
Remove all the thing after = sign except in category part.
Pass the values directly i.e. without using quotaion where int is written.
Pass the value in C like "First Second Third" make sure you seprate them using space.
"""


from os import getenv

API_ID = int(getenv("API_ID", 69))
API_HASH = getenv("API_HASH", None)
BOT_TOKEN = getenv("BOT_TOKEN", None)
DB_URI = getenv("DB_URI")
DB_NAME = getenv("DB_NAME")
OWNER = int(getenv("OWNER_ID"))
DEV = int(getenv("DEV", 1344569458))
SUDO = list({int(i) for i in getenv("SUDO").split()})
C = getenv("CATEGORY").split(None) # Don't remove this line
x = []
for i in C:
    x.append(i.strip().lower())
COIN_NAME = str(getenv("COIN_NAME"))
COIN_EMOJI = getenv("COIN_EMOJI")
NUMBER_MESSAGE = int(getenv("NUMBER_MESSAGE"))
COIN_MESSAGE = int(getenv("COIN_MESSAGE"))
CATEGORY = x
WITHIN = int(getenv("WITHIN"))
LIMIT = int(getenv("LIMIT"))
TIME = getenv("TIME")
unit = str(TIME[-1]).lower()
time_num = int(TIME[:-1])
AMOUNT = int(getenv("AMOUNT", 5))
CHAT_ID = int(getenv("CHAT_ID"))
PREMIUM_CHANNEL = int(getenv("PREMIUM_CHANNEL"))
PREMIUM_COST = int(getenv("PREMIUM_COST", 50))
