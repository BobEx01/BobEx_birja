# config.py
import os

# Bot tokeni (avval ENV'dan oladi, bo'lmasa hozirgi tokenni ishlatadi)
BOT_TOKEN = os.getenv("BOT_TOKEN", "7653469544:AAEuDWAsJTJ404V1AFIcx_lkJNUkLi_kgmU")

# Admin ma'lumotlari
ADMIN_ID = int(os.getenv("ADMIN_ID", "8080091052"))
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "@bobex_uz")

# Narx sozlamalari
RAQAM_NARX = int(os.getenv("RAQAM_NARX", "28000"))
VIP_NARX = int(os.getenv("VIP_NARX", "1000000"))
SUPER_NARX = int(os.getenv("SUPER_NARX", "90000"))
PAKET_10_NARX = int(os.getenv("PAKET_10_NARX", "186000"))
VIP_ELON_NARX = int(os.getenv("VIP_ELON_NARX", "45000"))
SUPER_ELON_NARX = int(os.getenv("SUPER_ELON_NARX", "90000"))
