import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")

RAQAM_NARX = int(os.getenv("RAQAM_NARX"))
VIP_NARX = int(os.getenv("VIP_NARX"))
SUPER_NARX = int(os.getenv("SUPER_NARX"))
PAKET_10_NARX = int(os.getenv("PAKET_10_NARX"))
VIP_ELON_NARX = int(os.getenv("VIP_ELON_NARX"))
SUPER_ELON_NARX = int(os.getenv("SUPER_ELON_NARX"))
