# handlers/shofyor_elon.py

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from database import cursor, conn
from handlers.utils import back_button
import datetime

user_data = {}

async def shofyor_elon_start(update, context):
    await update.message.reply_text(
        "Viloyatni tanlang:",
        reply_markup=viloyatlar_keyboard()
    )
    return "viloyat"

def viloyatlar_keyboard():
    viloyatlar = ["Toshkent", "Andijon", "Farg'ona", "Namangan",
                  "Samarqand", "Buxoro", "Navoiy", "Qashqadaryo",
                  "Surxondaryo", "Jizzax", "Sirdaryo", "Xorazm", "Qoraqalpog'iston"]
    keyboard = [[viloyat] for viloyat in viloyatlar]
    keyboard.append(["⬅️ Orqaga"])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def viloyat_qabul(update, context):
    user_data['viloyat'] = update.message.text
    await update.message.reply_text(
        "Tumaningizni kiriting:",
        reply_markup=back_button()
    )
    return "tuman"

async def tuman_qabul(update, context):
    user_data['tuman'] = update.message.text
    await update.message.reply_text(
        "Qanday mashinangiz bor? (Yuk sig‘imi, turi)"
    )
    return "mashina"

async def mashina_qabul(update, context):
    user_data['mashina'] = update.message.text
    await update.message.reply_text(
        "Mashina sig‘imini kiriting (kg yoki tonna):"
    )
    return "sigim"

async def sigim_qabul(update, context):
    user_data['sigim'] = update.message.text
    await update.message.reply_text(
        "Narxingizni kiriting (so‘m):"
    )
    return "narx"

async def narx_qabul(update, context):
    user_data['narx'] = int(update.message.text)
    await update.message.reply_text(
        "Telefon raqamingizni yozing:"
    )
    return "telefon"

async def telefon_qabul(update, context):
    user_data['telefon'] = update.message.text
    user_data['user_id'] = update.message.from_user.id
    user_data['sanasi'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Bazaga saqlash
    cursor.execute('''
    INSERT INTO shofyor_elonlar (user_id, viloyat, tuman, mashina, sigim, narx, telefon, sanasi)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_data['user_id'], user_data['viloyat'], user_data['tuman'],
        user_data['mashina'], user_data['sigim'], user_data['narx'],
        user_data['telefon'], user_data['sanasi']
    ))
    conn.commit()

    await update.message.reply_text(
        "✅ Shofyor e’loningiz muvaffaqiyatli joylandi!",
        reply_markup=ReplyKeyboardRemove()
    )
    return -1  # Conversation end
