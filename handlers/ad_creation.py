# handlers/ad_creation.py
from telegram import Update
from telegram.ext import (
    ContextTypes, MessageHandler, ConversationHandler, filters
)
from keyboards.menu import main_menu, ad_type_menu, back_menu
from database import cursor, conn

# Holatlar
SELECT_TYPE = 0
YUK_FROM_REGION, YUK_TO_REGION, YUK_WEIGHT, YUK_CAR, YUK_PRICE, YUK_PHONE, YUK_NOTE, YUK_CONFIRM = range(1, 9)
DRIVER_REGION, DRIVER_FROM, DRIVER_TO, DRIVER_NAME, DRIVER_CAR, DRIVER_CAP, DRIVER_PRICE, DRIVER_PHONE, DRIVER_NOTE, DRIVER_CONFIRM = range(10, 20)

BACK_TXT = "⬅️ Orqaga"
CANCEL_TXT = "❌ Bekor qilish"

# --- Boshlash ---
async def start_ad_creation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("E'lon turini tanlang:", reply_markup=ad_type_menu())
    return SELECT_TYPE

# --- Yuk e'lon jarayoni ---
async def select_yuk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Viloyatni kiriting:", reply_markup=back_menu())
    return YUK_FROM_REGION

async def yuk_from_region(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["viloyat"] = update.message.text
    await update.message.reply_text("Qayerga (viloyat) yuboriladi?", reply_markup=back_menu())
    return YUK_TO_REGION

async def yuk_to_region(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["qayerga"] = update.message.text
    await update.message.reply_text("Yuk og‘irligini kiriting:", reply_markup=back_menu())
    return YUK_WEIGHT

async def yuk_weight(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ogirlik"] = update.message.text
    await update.message.reply_text("Transport turi (mashina) kiriting:", reply_markup=back_menu())
    return YUK_CAR

async def yuk_car(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["mashina"] = update.message.text
    await update.message.reply_text("Narxni kiriting:", reply_markup=back_menu())
    return YUK_PRICE

async def yuk_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["narx"] = update.message.text
    await update.message.reply_text("Telefon raqamingizni kiriting:", reply_markup=back_menu())
    return YUK_PHONE

async def yuk_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["telefon"] = update.message.text
    await update.message.reply_text("Izoh (ixtiyoriy):", reply_markup=back_menu())
    return YUK_NOTE

async def yuk_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["izoh"] = update.message.text
    # Tasdiqlash
    txt = (
        "📦 Yuk e'loni:\n"
        f"Viloyat: {context.user_data['viloyat']}\n"
        f"Qayerga: {context.user_data['qayerga']}\n"
        f"Og‘irlik: {context.user_data['ogirlik']}\n"
        f"Mashina: {context.user_data['mashina']}\n"
        f"Narx: {context.user_data['narx']}\n"
        f"Telefon: {context.user_data['telefon']}\n"
        f"Izoh: {context.user_data['izoh']}\n\n"
        "✅ Tasdiqlaysizmi?"
    )
    await update.message.reply_text(txt, reply_markup=[["✅ Ha", "❌ Yo‘q"]])
    return YUK_CONFIRM

async def yuk_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "✅ Ha":
        user_id = update.effective_user.id
        cursor.execute("""
            INSERT INTO yuk_elonlar
            (user_id, viloyat, qayerga, ogirlik, mashina, narx, telefon, izoh)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            context.user_data['viloyat'],
            context.user_data['qayerga'],
            context.user_data['ogirlik'],
            context.user_data['mashina'],
            context.user_data['narx'],
            context.user_data['telefon'],
            context.user_data['izoh']
        ))
        conn.commit()
        await update.message.reply_text("✅ E'lon qo‘shildi!", reply_markup=main_menu())
    else:
        await update.message.reply_text("❌ Bekor qilindi.", reply_markup=main_menu())
    return ConversationHandler.END# --- Haydovchi e'lon jarayoni ---
async def select_driver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Viloyatni kiriting:", reply_markup=back_menu())
    return DRIVER_REGION

async def driver_region(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["viloyat"] = update.message.text
    await update.message.reply_text("Qayerdan yo‘lga chiqadi?", reply_markup=back_menu())
    return DRIVER_FROM

async def driver_from(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["qayerdan"] = update.message.text
    await update.message.reply_text("Qayerga boradi?", reply_markup=back_menu())
    return DRIVER_TO

async def driver_to(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["qayerga"] = update.message.text
    await update.message.reply_text("Ismingizni kiriting:", reply_markup=back_menu())
    return DRIVER_NAME

async def driver_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ism"] = update.message.text
    await update.message.reply_text("Transport turi (mashina) kiriting:", reply_markup=back_menu())
    return DRIVER_CAR

async def driver_car(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["mashina"] = update.message.text
    await update.message.reply_text("Sig‘imni kiriting:", reply_markup=back_menu())
    return DRIVER_CAP

async def driver_cap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["sigim"] = update.message.text
    await update.message.reply_text("Narxni kiriting:", reply_markup=back_menu())
    return DRIVER_PRICE

async def driver_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["narx"] = update.message.text
    await update.message.reply_text("Telefon raqamingizni kiriting:", reply_markup=back_menu())
    return DRIVER_PHONE

async def driver_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["telefon"] = update.message.text
    await update.message.reply_text("Izoh (ixtiyoriy):", reply_markup=back_menu())
    return DRIVER_NOTE

async def driver_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["izoh"] = update.message.text
    # Tasdiqlash
    txt = (
        "🚖 Haydovchi e'loni:\n"
        f"Viloyat: {context.user_data['viloyat']}\n"
        f"Qayerdan: {context.user_data['qayerdan']}\n"
        f"Qayerga: {context.user_data['qayerga']}\n"
        f"Ism: {context.user_data['ism']}\n"
        f"Mashina: {context.user_data['mashina']}\n"
        f"Sig‘im: {context.user_data['sigim']}\n"
        f"Narx: {context.user_data['narx']}\n"
        f"Telefon: {context.user_data['telefon']}\n"
        f"Izoh: {context.user_data['izoh']}\n\n"
        "✅ Tasdiqlaysizmi?"
    )
    await update.message.reply_text(txt, reply_markup=[["✅ Ha", "❌ Yo‘q"]])
    return DRIVER_CONFIRM

async def driver_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "✅ Ha":
        user_id = update.effective_user.id
        cursor.execute("""
            INSERT INTO shofyor_elonlar
            (user_id, viloyat, qayerdan, qayerga, ism, mashina, sigim, narx, telefon, izoh)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            context.user_data['viloyat'],
            context.user_data['qayerdan'],
            context.user_data['qayerga'],
            context.user_data['ism'],
            context.user_data['mashina'],
            context.user_data['sigim'],
            context.user_data['narx'],
            context.user_data['telefon'],
            context.user_data['izoh']
        ))
        conn.commit()
        await update.message.reply_text("✅ E'lon qo‘shildi!", reply_markup=main_menu())
    else:
        await update.message.reply_text("❌ Bekor qilindi.", reply_markup=main_menu())
    return ConversationHandler.END

# --- Back & Cancel handler ---
async def back_or_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = update.message.textif txt == BACK_TXT:
        await update.message.reply_text("Bosh menyuga qaytdingiz.", reply_markup=main_menu())
    else:
        await update.message.reply_text("Bekor qilindi.", reply_markup=main_menu())
    return ConversationHandler.END

# --- Handler ro'yxatdan o'tkazish ---
def register_ad_creation_handlers(app):
    conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^📢 E'lon berish$"), start_ad_creation)],
        states={
            SELECT_TYPE: [
                MessageHandler(filters.Regex("^🚚 Yuk uchun e'lon$"), select_yuk),
                MessageHandler(filters.Regex("^🚖 Haydovchi e'loni$"), select_driver),
                MessageHandler(filters.Text([BACK_TXT, CANCEL_TXT]), back_or_cancel)
            ],
            # Yuk
            YUK_FROM_REGION: [MessageHandler(filters.TEXT & ~filters.COMMAND, yuk_from_region)],
            YUK_TO_REGION: [MessageHandler(filters.TEXT & ~filters.COMMAND, yuk_to_region)],
            YUK_WEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, yuk_weight)],
            YUK_CAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, yuk_car)],
            YUK_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, yuk_price)],
            YUK_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, yuk_phone)],
            YUK_NOTE: [MessageHandler(filters.TEXT & ~filters.COMMAND, yuk_note)],
            YUK_CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, yuk_confirm)],
            # Driver
            DRIVER_REGION: [MessageHandler(filters.TEXT & ~filters.COMMAND, driver_region)],
            DRIVER_FROM: [MessageHandler(filters.TEXT & ~filters.COMMAND, driver_from)],
            DRIVER_TO: [MessageHandler(filters.TEXT & ~filters.COMMAND, driver_to)],
            DRIVER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, driver_name)],
            DRIVER_CAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, driver_car)],
            DRIVER_CAP: [MessageHandler(filters.TEXT & ~filters.COMMAND, driver_cap)],
            DRIVER_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, driver_price)],
            DRIVER_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, driver_phone)],
            DRIVER_NOTE: [MessageHandler(filters.TEXT & ~filters.COMMAND, driver_note)],
            DRIVER_CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, driver_confirm)],
        },
        fallbacks=[MessageHandler(filters.Text([BACK_TXT, CANCEL_TXT]), back_or_cancel)],
        allow_reentry=True
    )
    app.add_handler(conv)
