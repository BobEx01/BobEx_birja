# keyboards/menu.py
from telegram import ReplyKeyboardMarkup

def main_menu():
    """
    Bosh menyu — foydalanuvchi botga kirganda ko‘radi.
    """
    keyboard = [
        ["📢 E'lon berish", "📄 E'lonlarni ko'rish"],
        ["💳 Balans", "ℹ️ Yordam"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def ad_type_menu():
    """
    E'lon turi menyusi — yuk yoki haydovchi e'loni tanlash uchun.
    """
    keyboard = [
        ["🚚 Yuk uchun e'lon", "🚖 Haydovchi e'loni"],
        ["⬅️ Orqaga", "❌ Bekor qilish"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

def back_menu():
    """
    Orqaga yoki bekor qilish menyusi.
    """
    keyboard = [["⬅️ Orqaga", "❌ Bekor qilish"]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
