# https://t.me/ultroid_official



import os
import logging
from logging.handlers import RotatingFileHandler

TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
APP_ID = int(os.environ.get("APP_ID", "24955235"))
API_HASH = os.environ.get("API_HASH", "f317b3f7bbe390346d8b46868cff0de8")


OWNER = os.environ.get("OWNER", "i_am_yamraj") #Owner username
OWNER_ID = int(os.environ.get("OWNER_ID", "1837294444")) #Owner user id
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://Cluster0:Cluster0@cluster0.c07xkuf.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.environ.get("DATABASE_NAME", "Cluser10")

CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002004278204")) #database save channel id 
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "-1002049574995"))
FORCE_SUB_CHANNEL2 = int(os.environ.get("FORCE_SUB_CHANNEL2", "-1002097822007"))
FORCE_SUB_CHANNEL3 = int(os.environ.get("FORCE_SUB_CHANNEL3", "-1001940737153"))
FORCE_SUB_CHANNEL4 = int(os.environ.get("FORCE_SUB_CHANNEL4", "-1002134495794"))

#Shortner (token system) 

SHORTLINK_URL = os.environ.get("SHORTLINK_URL", "adrinolinks.in") 
SHORTLINK_API = os.environ.get("SHORTLINK_API", "5883bbd80da73ef7908bf7922c3aa8050586588d")
VERIFY_EXPIRE = int(os.environ.get('VERIFY_EXPIRE', 86400)) # Add time in seconds
IS_VERIFY = os.environ.get("IS_VERIFY", "True")
TUT_VID = os.environ.get("TUT_VID", "https://t.me/HTDTeraBox/6")

# ignore this one
SECONDS = int(os.getenv("SECONDS", "200")) # auto delete in seconds



PORT = os.environ.get("PORT", "8080")
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))




START_MSG = os.environ.get("START_MESSAGE", "Hello {first}\n\nI can store private files in Specified Channel and other users can access it from special link. Owner @NeonGhost_Networks")

try:
    ADMINS=[6020516635]
    for x in (os.environ.get("ADMINS", "1837294444").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")


FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "Hello {first}\n\n<b>You need to join in my Channel/Group to use me\n\nKindly Please join Channel</b>\n After Joining All channels Please click on Try Again ")

CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", "@NeonGhost_Networks") # remove None and fo this ->: "here come your txt" also with this " " 

PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "True") == "True" else False

DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "❌Don't send me messages directly I'm only File Share bot !"

ADMINS.append(OWNER_ID)
ADMINS.append(6695586027)

LOG_FILE_NAME = "uxblogs.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
   





# https://t.me/ultroid_official
