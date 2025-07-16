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
    hisob_tolidirish, 
    paketlar, 
    premium_vip, 
    yuk_elon, 
    yuk_korish, 
    shofyor_elon, 
    shofyor_korish, 
    raqam_olish,
    admin_xabar
)

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

app = Application.builder().token(TOKEN).build()

# --- START komandasi ---
app.add_handler(CommandHandler('start', start.boshlash))
app.add_handler(CommandHandler('boshlash', start.boshlash))

# --- HISOBIM ---
app.add_handler(MessageHandler(filters.Regex("^💳 Hisobim$"), hisobim.hisobim_handler))

# --- HISOBNI TO‘LDIRISH ---
app.add_handler(ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^Hisobni to‘ldirish$"), hisob_tolidirish.hisobni_tolidirish_start)],
    states={
        hisob_tolidirish.TOLOV_MIqdori: [MessageHandler(filters.TEXT & ~filters.COMMAND, hisob_tolidirish.tolov_miqdori_qabul)],
        hisob_tolidirish.TOLOV_CHEK: [MessageHandler(filters.PHOTO, hisob_tolidirish.tolov_chek_qabul)]
    },
    fallbacks=[MessageHandler(filters.Regex("^⬅️ Orqaga$"), hisob_tolidirish.ortga_qaytish)]
))

app.add_handler(MessageHandler(filters.Regex(r'^/tasdiqla_'), hisob_tolidirish.admin_tasdiqlash))

# --- PAKETLAR ---
app.add_handler(MessageHandler(filters.Regex("^🎁 Paketlar$"), paketlar.paketlar_handler))
app.add_handler(CommandHandler('paket_ol', paketlar.paket_ol))

# --- PREMIUM/VIP ---
app.add_handler(CommandHandler('premium', premium_vip.premium_elon))
app.add_handler(CommandHandler('vip', premium_vip.vip_aktiv))

# --- YUK ELON ---
yuk_elon_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^🚛 Yuk uchun e'lon berish$"), yuk_elon.yuk_elon_start)],
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
    entry_points=[MessageHandler(filters.Regex("^🚚 Shofyor e'lon berish$"), shofyor_elon.shofyor_elon_start)],
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

# --- E'LON KO‘RISH ---
app.add_handler(MessageHandler(filters.Regex("^📦 Yuk e'lonlarini ko‘rish$"), yuk_korish.yuk_korish))
app.add_handler(MessageHandler(filters.Regex("^🚚 Shofyor e'lonlarini ko‘rish$"), shofyor_korish.shofyor_korish))

# --- RAQAM OLISH CALLBACK ---
app.add_handler(CallbackQueryHandler(raqam_olish.raqam_olish_handler, pattern='^(yuk_raqam_|shofyor_raqam_)'))# --- ADMIN XABAR ---
app.add_handler(MessageHandler(filters.Regex("^📣 Admin xabar$"), admin_xabar.admin_xabar_handler))# --- START LOG ---
print("🤖 BobEx Bot to‘liq ishga tushdi...")

app.run_polling()
