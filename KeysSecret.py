from os import getenv

API_ID = int(getenv("API_ID", 69))
API_HASH = getenv("API_HASH", None)
BOT_TOKEN = getenv("BOT_TOKEN", None)
DB_URI = getenv("DB_URI")
DB_NAME = getenv("DB_NAME")
OWNER_ID = int(getenv("OWNER_ID"))