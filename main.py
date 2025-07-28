from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackQueryHandler
import yuk_elon
import shofyor_elon
import yuk_korish
import shofyor_korish
import raqam_olish
import vip_super_xizmat
import admin_xabar
import elonlarim
import pul_ishlash

TOKEN = "7653469544:AAEuDWAsJTJ404V1AFIcx_lkJNUkLi_kgmU"

def main():
    app = Application.builder().token(TOKEN).build()

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
    app.run_polling()

if __name__ == "__main__":
    main()
