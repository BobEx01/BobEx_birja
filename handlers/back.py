# handlers/back.py
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from keyboards.menu import main_menu

BACK_TXT = "⬅️ Orqaga"
CANCEL_TXT = "❌ Bekor qilish"

async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Orqaga yoki bekor qilish tugmasi bosilganda bosh menyuga qaytaradi.
    """
    await update.message.reply_text("Bosh menyuga qaytdingiz.", reply_markup=main_menu())

def register_back_handlers(app):
    app.add_handler(MessageHandler(filters.Text([BACK_TXT, CANCEL_TXT]), back_to_menu))
