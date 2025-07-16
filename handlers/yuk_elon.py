# handlers/yuk_elon.py

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

# States
VILOYAT, TUMAN, QAYERDAN, QAYERGA, OGIRLIK, MASHINA, NARX, TELEFON, TASDIQ = range(9)

# E'lon ma'lumotlarini vaqtinchalik saqlash uchun dict
user_data = {}

async def yuk_elon_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Viloyatni kiriting:")
    return VILOYAT

async def viloyat_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['viloyat'] = update.message.text
    await update.message.reply_text("Tumaningizni kiriting:")
    return TUMAN

async def tuman_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['tuman'] = update.message.text
    await update.message.reply_text("Qayerdan yuk ketmoqda?")
    return QAYERDAN

async def qayerdan_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['qayerdan'] = update.message.text
    await update.message.reply_text("Qayerga bormoqda?")
    return QAYERGA

async def qayerga_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['qayerga'] = update.message.text
    await update.message.reply_text("Yuk og‘irligini kiriting (kg yoki tonna):")
    return OGIRLIK

async def ogirlik_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['ogirlik'] = update.message.text
    await update.message.reply_text("Mashina turini kiriting:")
    return MASHINA

async def mashina_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['mashina'] = update.message.text
    await update.message.reply_text("Narxni kiriting (so‘m):")
    return NARX

async def narx_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['narx'] = update.message.text
    await update.message.reply_text("Telefon raqamingizni yuboring:")
    return TELEFON

async def telefon_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['telefon'] = update.message.text

    elon_matni = (
        f"📦 <b>Yuk e'loni:</b>\n"
        f"🏙 Viloyat: {context.user_data['viloyat']}\n"
        f"📍 Tuman: {context.user_data['tuman']}\n"
        f"🚚 Qayerdan: {context.user_data['qayerdan']}\n"
        f"📌 Qayerga: {context.user_data['qayerga']}\n"
        f"⚖️ Og‘irlik: {context.user_data['ogirlik']}\n"
        f"🚛 Mashina: {context.user_data['mashina']}\n"
        f"💰 Narx: {context.user_data['narx']}\n"
        f"📞 Telefon: {context.user_data['telefon']}"
    )

    buttons = [
        [InlineKeyboardButton("✅ Tasdiqlash", callback_data='tasdiq')],
        [InlineKeyboardButton("❌ Bekor qilish", callback_data='bekor')]
    ]
    await update.message.reply_text(elon_matni, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(buttons))
    return TASDIQ


async def tasdiq_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'tasdiq':
        await query.edit_message_text("✅ E'loningiz muvaffaqiyatli saqlandi.")
        # TODO: Bu yerda elonni bazaga saqlash kodini yozish mumkin
    else:
        await query.edit_message_text("❌ E'lon bekor qilindi.")

    return ConversationHandler.END
