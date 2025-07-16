from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from database import cursor, conn

ADMIN_ID = 8080091052

# 1️⃣ Hisobim Menyusi
async def hisob_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    cursor.execute("SELECT balans FROM foydalanuvchilar WHERE user_id=?", (user_id,))
    balans = cursor.fetchone()
    balans = balans[0] if balans else 0

    text = f"""
💳 Hisobingiz: {balans} so'm

Hisobingizni to‘ldirish uchun quyidagilarni bajaring:

🔷 To'lov tizimi: Humo[Card]
Hamyon: 5614 6822 1820 6250
ID: {user_id}
Karta egasi: Muhammadbobur.A

🔹 Minimal: 10,000 so'm
🔹 Maksimal: 10,000,000 so'm

Hisobni to‘ldirish tartibi:
1️⃣ Istalgan miqdorda to‘lov qiling
2️⃣ «✅ To‘lov qildim» tugmasini bosing
3️⃣ To‘lov chekini rasm qilib yuboring
4️⃣ Admin tasdiqlaydi

⚠️ To‘lovingiz 15-500 daqiqa ichida ko‘rib chiqiladi. Pul faqat xizmat uchun sarflanadi.
"""

    buttons = [[InlineKeyboardButton("✅ To‘lov qildim", callback_data='tolov_qildim')]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))


# 2️⃣ To‘lov Qildim Callback
async def tolov_qildim_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    context.user_data['tolov_kutilmoqda'] = True
    await query.message.reply_text("📸 To‘lov chekini rasm shaklida yuboring.")


# 3️⃣ Chek Qabul qilish va Adminga Xabar
async def chek_qabul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('tolov_kutilmoqda'):
        if update.message.photo:
            user_id = update.message.from_user.id
            await context.bot.send_photo(
                chat_id=ADMIN_ID,
                photo=update.message.photo[-1].file_id,
                caption=f"🧾 Yangi To‘lov Cheki!\n\nFoydalanuvchi ID: {user_id}\nIsm: {update.message.from_user.full_name}\n\nBalansini tekshiring va qo‘shing."
            )
            await update.message.reply_text("✅ To‘lovingiz admin tomonidan tekshiriladi. Balansingiz to‘ldirilgach, xabar olasiz.")
            context.user_data['tolov_kutilmoqda'] = False
        else:
            await update.message.reply_text("❗️ Iltimos, to‘lov chekini rasm shaklida yuboring.")


# 4️⃣ Admin Balans Qo‘shish
async def balans_qoshish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Bu buyruq faqat admin uchun!")
        return

    try:
        args = context.args
        user_id = int(args[0])
        summa = int(args[1])

        cursor.execute("UPDATE foydalanuvchilar SET balans = balans + ? WHERE user_id=?", (summa, user_id))
        conn.commit()

        await update.message.reply_text(f"✅ {user_id} foydalanuvchining balansiga {summa} so‘m qo‘shildi.")
        await context.bot.send_message(chat_id=user_id, text=f"💳 Hisobingiz {summa} so‘mga to‘ldirildi!")
    except:
        await update.message.reply_text("❗️ Foydalanish: /balans_qoshish <user_id> <summa>")
