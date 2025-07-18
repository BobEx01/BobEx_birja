from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
import datetime

# ✅ ASOSIY MENYU - YANGI TALQINDA
def asosiy_menu():
    keyboard = [
        ["🚛 Yuk uchun e’lon berish", "🚚 Shofyor e’lon berish"],
        ["📦 Yuk e’lonlarini ko‘rish", "🚚 Shofyor e’lonlarini ko‘rish"],
        ["📊 Mening hisobim", "💳 Hisobni to‘ldirish"],
        ["🎁 Paketlar"],
        ["📦 E’lonlarim"],
        ["📣 Admin xabar"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# ✅ /start komandasi uchun funksiya
async def boshlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id

    # Bonus berish: agar referal orqali kirgan bo‘lsa
    if context.args:
        referal_id = context.args[0]
        if referal_id != str(user_id):
            await bonus_berish(referal_id, context)

    await update.message.reply_text(
        f"👋 Assalomu alaykum, BobEx botiga xush kelibsiz, {user.first_name}!\n\n"
        "Quyidagi menyulardan birini tanlang:",
        reply_markup=asosiy_menu()
    )


# ✅ Referal orqali kirganlar uchun 2000 so‘m bonus
async def bonus_berish(referal_id, context):
    from database import cursor, conn

    bonus = 2000
    cursor.execute("UPDATE foydalanuvchilar SET balans = balans + ? WHERE user_id = ?", (bonus, referal_id))
    conn.commit()

    try:
        await context.bot.send_message(
            chat_id=int(referal_id),
            text=f"🎉 Tabriklaymiz! Siz referal orqali yangi foydalanuvchini taklif qildingiz va {bonus} so‘m bonus oldingiz."
        )
    except Exception as e:
        print(f"Bonus yuborishda xatolik: {e}")


# ✅ Juma kuni 50% chegirma tekshirish funksiyasi
def chegirma_50_foiz():
    hozir = datetime.datetime.now()
    return hozir.weekday() == 4   # 0=dushanba, ..., 4=juma


# ✅ Hisob to‘ldirishda chegirma hisoblash
def hisob_toldirish_chegirma(narx):
    if chegirma_50_foiz():
        return int(narx / 2)
    return narx
