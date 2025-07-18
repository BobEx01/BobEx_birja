from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database import cursor, conn

# Asosiy menyu funksiyasi
def asosiy_menu():
    keyboard = [
        ["🚛 Yuk uchun e'lon berish", "🚚 Shofyor e'lon berish"],
        ["📦 Yuk e'lonlarini ko‘rish", "🚚 Shofyor e'lonlarini ko‘rish"],
        ["📊 Mening hisobim", "Hisobni to‘ldirish"],
        ["🎁 Paketlar", "🗂 E'lonlarim"],
        ["💸 Pul ishlash"],
        ["📣 Admin xabar"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# /start komandasi uchun funksiya
async def boshlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id

    # REFERAL orqali kirgan bo‘lsa, referal_id saqlash
    if context.args:
        referal_id = context.args[0]
        if referal_id != str(user_id):  # O'zini referal qilmang
            cursor.execute("SELECT referal_id FROM foydalanuvchilar WHERE user_id = ?", (user_id,))
            existing = cursor.fetchone()
            if existing is None:
                cursor.execute(
                    "INSERT INTO foydalanuvchilar (user_id, referal_id, balans, bonus_berildi, paket_soni, toldirilgan, vip_oxirgi, sarflangan) "
                    "VALUES (?, ?, 0, 0, 0, 0, '', 0)",
                    (user_id, referal_id)
                )
            elif existing[0] == 0:
                cursor.execute("UPDATE foydalanuvchilar SET referal_id = ? WHERE user_id = ?", (referal_id, user_id))
            conn.commit()

    await update.message.reply_text(
        f"👋 Assalomu alaykum, BobEx botiga xush kelibsiz, {user.first_name}!\n\n"
        "Quyidagi menyulardan birini tanlang:\n\n"
        "🚛 Yuk uchun e'lon berish\n"
        "🚚 Shofyor e'lon berish\n"
        "📦 Yuk e'lonlarini ko‘rish\n"
        "🚚 Shofyor e'lonlarini ko‘rish\n"
        "📊 Mening hisobim — balans va hisob to‘ldirish\n"
        "Hisobni to‘ldirish — balansni to‘ldiring\n"
        "🎁 Paketlar — VIP tarif va bonus paketlar\n"
        "🗂 E'lonlarim — o'zingiz bergan e'lonlarni ko‘rish\n"
        "💸 Pul ishlash — do‘stlaringizni taklif qilib bonus oling\n"
        "📣 Admin xabar — admin bilan bog‘lanish",
        reply_markup=asosiy_menu()
    )
