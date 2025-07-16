# main.py

import logging
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters
)

from config import TOKEN
from handlers import (
    start, 
    hisobim, 
    paketlar, 
    premium_vip, 
    yuk_elon, 
    yuk_korish, 
    shofyor_elon, 
    shofyor_korish, 
    raqam_olish
)

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Tokeningiz
TOKEN = '7653469544:AAFH4xoRxu8-_nWy0CR1gXA1Nkv1txt3gqc'

# Bot app
app = Application.builder().token(TOKEN).build()

# --- COMMANDS ---
app.add_handler(CommandHandler('start', start.start))
app.add_handler(CommandHandler('hisobim', hisobim.hisobim_handler))
app.add_handler(CommandHandler('paketlar', paketlar.paketlar_handler))
app.add_handler(CommandHandler('paket_ol', paketlar.paket_ol))
app.add_handler(CommandHandler('premium', premium_vip.premium_elon))
app.add_handler(CommandHandler('vip', premium_vip.vip_aktiv))

# --- YUK ELON ---
yuk_elon_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('🚛 Yuk uchun e\'lon berish'), yuk_elon.yuk_elon_start)],
    states={
        "viloyat": [MessageHandler(filters.TEXT & ~filters.COMMAND, yuk_elon.viloyat_qabul)],
        "tuman": [MessageHandler(filters.TEXT & ~filters.COMMAND, yuk_elon.tuman_qabul)],
        "qayerdan": [MessageHandler(filters.TEXT & ~filters.COMMAND, yuk_elon.qayerdan_qabul)],
        "qayerga": [MessageHandler(filters.TEXT & ~filters.COMMAND, yuk_elon.qayerga_qabul)],
        "ogirlik": [MessageHandler(filters.TEXT & ~filters.COMMAND, yuk_elon.ogirlik_qabul)],
        "mashina": [MessageHandler(filters.TEXT & ~filters.COMMAND, yuk_elon.mashina_qabul)],
        "narx": [MessageHandler(filters.TEXT & ~filters.COMMAND, yuk_elon.narx_qabul)],
        "telefon": [MessageHandler(filters.TEXT & ~filters.COMMAND, yuk_elon.telefon_qabul)],
    },
    fallbacks=[]
)
app.add_handler(yuk_elon_conv)

# --- SHOYOR ELON ---
shofyor_elon_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('🚚 Shofyor e\'lon berish'), shofyor_elon.shofyor_elon_start)],
    states={
        "viloyat": [MessageHandler(filters.TEXT & ~filters.COMMAND, shofyor_elon.viloyat_qabul)],
        "tuman": [MessageHandler(filters.TEXT & ~filters.COMMAND, shofyor_elon.tuman_qabul)],
        "mashina": [MessageHandler(filters.TEXT & ~filters.COMMAND, shofyor_elon.mashina_qabul)],
        "sigim": [MessageHandler(filters.TEXT & ~filters.COMMAND, shofyor_elon.sigim_qabul)],
        "narx": [MessageHandler(filters.TEXT & ~filters.COMMAND, shofyor_elon.narx_qabul)],
        "telefon": [MessageHandler(filters.TEXT & ~filters.COMMAND, shofyor_elon.telefon_qabul)],
    },
    fallbacks=[]
)
app.add_handler(shofyor_elon_conv)

# --- KORISH ---
app.add_handler(MessageHandler(filters.Regex('📦 Yuk e\'lonlarini ko‘rish'), yuk_korish.yuk_korish))
app.add_handler(MessageHandler(filters.Regex('🚚 Shofyor e\'lonlarini ko‘rish'), shofyor_korish.shofyor_korish))

# --- RAQAM OLISH CALLBACK ---
app.add_handler(CallbackQueryHandler(raqam_olish.raqam_olish_handler, pattern='^(yuk_raqam_|shofyor_raqam_)'))

# --- BOT START ---
print("🤖 BobEx Bot to‘liq ishga tushdi...")

app.run_polling()
