# handlers/utils.py

from telegram import ReplyKeyboardMarkup

def back_button():
    keyboard = [["⬅️ Orqaga"]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
