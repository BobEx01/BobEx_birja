from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database import cursor, conn, foydalanuvchilar_soni  # foydalanuvchilar_soni ni ham chaqirdik
from config import ADMIN_ID

BONUS_MIQDORI = 2000  # Referal orqali bonus miqdori


# === Asosiy menyu ===
def asosiy_menu():
    keyboard = [
        ["🚛 Yuk uchun e'lon berish", "🚚 Shofyor e'lon berish"],
        ["📦 Yuk e'lonlarini ko‘rish", "🚚 Shofyor e'lonlarini ko‘rish"],
        ["📊 Mening hisobim", "Hisobni to‘ldirish"],
        ["🎁 Paketlar", "🗂 E'lonlarim"],
        ["💸 Pul ishlash"],
        ["📣 Admin xabar"],
        ["📊 Foydalanuvchilar soni"] if ADMIN_ID else []  # faqat admin ko‘rsin
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# === Referal bonus berish funksiyasi ===
async def bonus_berish(referal_id: int, context):
    try:
        cursor.execute("UPDATE foydalanuvchilar SET balans = balans + ? WHERE user_id = ?", (BONUS_MIQDORI, referal_id))
        conn.commit()
        await context.bot.send_message(
            chat_id=int(referal_id),
            text=f"🎉 Tabriklaymiz! Siz referal orqali yangi foydalanuvchini taklif qildingiz va {BONUS_MIQDORI} so‘m bonus oldingiz."
        )
    except Exception as e:
        print(f"Referal bonus yuborishda xato: {e}")


# === /start komandasi uchun funksiya ===
async def boshlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    username = user.username or ""

    # Foydalanuvchini bazaga qo‘shish
    cursor.execute("INSERT OR IGNORE INTO foydalanuvchilar (user_id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()

    # Referal ID ni tekshirish
    if context.args:
        referal_id = context.args[0]
        if referal_id != str(user_id):
            cursor.execute("SELECT referal_id FROM foydalanuvchilar WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()
            if result and (result[0] == 0 or result[0] is None):
                cursor.execute("UPDATE foydalanuvchilar SET referal_id = ? WHERE user_id = ?", (referal_id, user_id))
                conn.commit()
                await bonus_berish(int(referal_id), context)

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


# === Foydalanuvchilar sonini ko‘rsatish komandasi ===
async def foydalanuvchilar_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == ADMIN_ID:
        soni = foydalanuvchilar_soni()
        await update.message.reply_text(f"📊 Umumiy foydalanuvchilar soni: {soni}")
    else:
        await update.message.reply_text("❌ Siz admin emassiz.")
