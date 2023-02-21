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
OWNER_ID = int(getenv("OWNER_ID"))
C = getenv("CATEGORY").split(None) # Don't remove this line
Category = [i.strip().lower() for i in C]
No_cat = int(getenv("NUMBER_CATEGORY", 3))
No_sub_cat = int(getenv("NUMBER_SUBCATEGORY", 3))
AMOUNT = int(getenv("AMOUNT", 5))
CHAT_ID = getenv("CHAT_ID", None)
PREMIUM_CHANNEL = int(getenv("PREMIUM_CHANNEL"))
PREMIUM_COST = int(getenv("PREMIUM_COST", 50))