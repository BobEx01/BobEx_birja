import logging
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters
)

from config import BOT_TOKEN
from database import init_db

# Barcha handlers import
from handlers import (
    start,
    hisobim,
    hisob_tolidirish,
    paketlar,
    vip_super_xizmat,
    yuk_elon,
    yuk_korish,
    shofyor_elon,
    shofyor_korish,
    raqam_olish,
    admin_xabar,
    elonlarim,
    pul_ishlash,
    bonus_va_promo
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    # Bazani ishga tayyorlash
    init_db()

    app = Application.builder().token(BOT_TOKEN).build()

    # --- START ---
    app.add_handler(CommandHandler('start', start.boshlash))
    app.add_handler(CommandHandler('boshlash', start.boshlash))
    app.add_handler(CommandHandler('foydalanuvchilar', start.foydalanuvchilar_cmd))
    app.add_handler(MessageHandler(filters.Regex("^📊 Foydalanuvchilar soni$"), start.foydalanuvchilar_cmd))

    # --- MENING HISOBIM ---
    app.add_handler(MessageHandler(filters.Regex("^📊 Mening hisobim$"), hisobim.hisobim_handler))

    # --- HISOB TO‘LDIRISH ---
    hisob_tolidirish_conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^Hisobni to‘ldirish$"), hisob_tolidirish.hisobni_tolidirish_start)],
        states={
            hisob_tolidirish.TOLOV_MIqdori: [MessageHandler(filters.TEXT & ~filters.COMMAND, hisob_tolidirish.tolov_miqdori_qabul)],
            hisob_tolidirish.TOLOV_CHEK: [MessageHandler(filters.PHOTO, hisob_tolidirish.tolov_chek_qabul)]
        },
        fallbacks=[MessageHandler(filters.Regex("^⬅️ Orqaga$"), hisob_tolidirish.ortga_qaytish)]
    )
    app.add_handler(hisob_tolidirish_conv)
    app.add_handler(MessageHandler(filters.Regex(r'^/tasdiqla_'), hisob_tolidirish.admin_tasdiqlash))

    # --- PAKETLAR ---
    app.add_handler(MessageHandler(filters.Regex("^🎁 Paketlar$"), paketlar.paketlar_handler))
    app.add_handler(CommandHandler('paket_ol', paketlar.paket_ol))
    app.add_handler(CommandHandler('vip_paket_ol', paketlar.vip_paket_ol))
    app.add_handler(CommandHandler('paket_stat', paketlar.paket_stat))

    # --- BONUS VA PROMO ---
    app.add_handler(CommandHandler('elon_bonus', bonus_va_promo.elon_bonus_taklif))

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

    # --- SHOFYOR ELON ---
    shofyor_elon_conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^🚚 Shofyor e'lon berish$"), shofyor_elon.shofyor_elon_start)],
        states={
            "viloyat": [MessageHandler(filters.TEXT & ~filters.COMMAND, shofyor_elon.viloyat_qabul)],
            "tuman": [MessageHandler(filters.TEXT & ~filters.COMMAND, shofyor_elon.tuman_qabul)],
            "mashina": [MessageHandler(filters.TEXT & ~filters.COMMAND, shofyor_elon.mashina_qabul)],
            "sigim": [MessageHandler(filters.TEXT & ~filters.COMMAND, shofyor_elon.sigim_qabul)],"narx": [MessageHandler(filters.TEXT & ~filters.COMMAND, shofyor_elon.narx_qabul)],
            "telefon": [MessageHandler(filters.TEXT & ~filters.COMMAND, shofyor_elon.telefon_qabul)],
        },
        fallbacks=[]
    )
    app.add_handler(shofyor_elon_conv)

    # --- E'LON KO‘RISH ---
    app.add_handler(MessageHandler(filters.Regex("^📦 Yuk e'lonlarini ko‘rish$"), yuk_korish.yuk_korish))
    app.add_handler(MessageHandler(filters.Regex("^🚚 Shofyor e'lonlarini ko‘rish$"), shofyor_korish.shofyor_korish))

    app.add_handler(CallbackQueryHandler(yuk_korish.tumanlar_korish, pattern='^viloyat_'))
    app.add_handler(CallbackQueryHandler(yuk_korish.elonlar_korish, pattern='^tuman_'))
    app.add_handler(CallbackQueryHandler(yuk_korish.orqaga_viloyatlar, pattern='^orqaga_viloyatlar$'))
    app.add_handler(CallbackQueryHandler(yuk_korish.orqaga_tumanlar, pattern='^orqaga_tumanlar_'))

    app.add_handler(CallbackQueryHandler(shofyor_korish.shofyor_tumanlar, pattern='^shof_vil_'))
    app.add_handler(CallbackQueryHandler(shofyor_korish.shofyor_elonlar, pattern='^shof_tum_'))
    app.add_handler(CallbackQueryHandler(shofyor_korish.orqaga_viloyatlar_shofyor, pattern='^orqaga_viloyatlar_shofyor$'))
    app.add_handler(CallbackQueryHandler(shofyor_korish.orqaga_tumanlar_shofyor, pattern='^orqaga_tumanlar_shofyor_'))

    # --- RAQAM OLISH ---
    app.add_handler(CallbackQueryHandler(raqam_olish.raqam_olish_handler, pattern='^(yuk_raqam_|shofyor_raqam_)'))

    # --- VIP/SUPER CALLBACKS ---
    app.add_handler(CallbackQueryHandler(vip_super_xizmat.vip_aktiv_callback, pattern='^vip_elon_'))
    app.add_handler(CallbackQueryHandler(vip_super_xizmat.super_aktiv_callback, pattern='^super_elon_'))
    app.add_handler(CallbackQueryHandler(vip_super_xizmat.handle_vip_super_tolov, pattern='^(vip_tolov|super_tolov)$'))

    # --- YUK UZAYTIRISH/OCHIRISH ---
    app.add_handler(CallbackQueryHandler(yuk_elon.yuk_ochir_qoldir_callback, pattern='^(yuk_ochir|yuk_qoldir)_'))

    # --- SHOFYOR UZAYTIRISH/OCHIRISH ---
    app.add_handler(CallbackQueryHandler(shofyor_elon.uzaytirish_callback, pattern='^uzaytir_shofyor_'))
    app.add_handler(CallbackQueryHandler(shofyor_elon.ochirish_callback, pattern='^ochir_shofyor_'))

    # --- ADMIN XABAR ---
    app.add_handler(MessageHandler(filters.Regex("^📣 Admin xabar$"), admin_xabar.admin_xabar_handler))

    # --- ELONLARIM ---
    app.add_handler(MessageHandler(filters.Regex("^🗂 E'lonlarim$"), elonlarim.elonlarim_handler))

    # --- PUL ISHLASH ---
    app.add_handler(MessageHandler(filters.Regex("^💸 Pul ishlash$"), pul_ishlash.pul_ishlash_handler))

    print("🤖 BobEx Bot to‘liq ishga tushdi...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN ENV o‘zgaruvchisi topilmadi. Railway Variables ga BOT_TOKEN qo‘shing.")
    main()
