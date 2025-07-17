# handlers/paketlar.py

from database import cursor, conn
from config import PAKET_10_NARX, VIP_NARX, ADMIN_ID
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes


async def paketlar_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🎟 <b>Paketlar va Aksiyalar:</b>\n\n"
        "1️⃣ 10 ta raqam olish paketi - 186,000 so‘m (33% chegirma)\n"
        "2️⃣ Har juma kuni - <b>50% chegirma</b> barcha funksiyalar uchun!\n"
        "3️⃣ VIP tarif - 1,000,000 so‘m (30 kun davomida barcha xizmatlar bepul)\n\n"
        "Paket sotib olish uchun: /paket_ol\n"
        "VIP tarif sotib olish uchun: /vip_paket_ol\n"
        "📊 Statistikani ko‘rish: /paket_stat"
    )
    await update.message.reply_text(text, parse_mode='HTML')


async def paket_ol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    cursor.execute('SELECT balans, paketlar FROM foydalanuvchilar WHERE user_id=?', (user_id,))
    result = cursor.fetchone()

    if not result:
        await update.message.reply_text("❌ Foydalanuvchi topilmadi.")
        return

    balans, paketlar = result
    narx = PAKET_10_NARX

    # Agar bugun juma bo‘lsa, 50% chegirma
    if datetime.now().weekday() == 4:
        narx = narx // 2

    if balans < narx:
        await update.message.reply_text(
            f"❌ Balansingiz yetarli emas. Paket narxi: {narx} so‘m.\n"
            "💳 Hisobni to‘ldirish: /hisobim"
        )
        return

    # Balansdan yechish va paket qo‘shish
    yangi_paket = int(paketlar) + 10 if paketlar != 'Yo‘q' else 10
    cursor.execute("UPDATE foydalanuvchilar SET balans = balans - ?, paketlar = ? WHERE user_id = ?",
                   (narx, yangi_paket, user_id))
    conn.commit()

    await update.message.reply_text(
        f"✅ 10 ta raqam olish paketi muvaffaqiyatli sotib olindi!\n"
        f"📦 Qolgan paketlaringiz: {yangi_paket} ta."
    )

    # Adminni xabardor qilish
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"🛒 Foydalanuvchi {user_id} {narx} so‘mga 10 ta paket sotib oldi.\n"
             f"Qolgan paketlari: {yangi_paket} ta."
    )


async def vip_paket_ol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    cursor.execute('SELECT balans FROM foydalanuvchilar WHERE user_id=?', (user_id,))
    result = cursor.fetchone()

    if not result:
        await update.message.reply_text("❌ Foydalanuvchi topilmadi.")
        return

    balans = result[0]

    if balans < VIP_NARX:
        await update.message.reply_text(
            f"❌ VIP paket uchun balans yetarli emas. Kerakli summa: {VIP_NARX} so‘m.\n"
            "💳 Hisobni to‘ldirish: /hisobim"
        )
        return

    vip_oxiri = datetime.now() + timedelta(days=30)
    cursor.execute("UPDATE foydalanuvchilar SET balans = balans - ?, vip_oxiri = ? WHERE user_id = ?",
                   (VIP_NARX, vip_oxiri.strftime('%Y-%m-%d'), user_id))
    conn.commit()

    await update.message.reply_text(
        f"✅ VIP tarif muvaffaqiyatli faollashtirildi!\n🗓 Amal qilish muddati: {vip_oxiri.strftime('%Y-%m-%d')} gacha."
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"💎 Foydalanuvchi {user_id} VIP paket sotib oldi.\nAmal qilish muddati: {vip_oxiri.strftime('%Y-%m-%d')}"
    )


async def paket_stat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    cursor.execute('SELECT paketlar, vip_oxiri FROM foydalanuvchilar WHERE user_id=?', (user_id,))
    result = cursor.fetchone()

    if not result:
        await update.message.reply_text("❌ Foydalanuvchi topilmadi.")
        return

    paketlar, vip_oxiri = result
    vip_text = f"🟢 VIP amal qiladi: {vip_oxiri}" if vip_oxiri else "🔴 VIP tarif aktiv emas."
    paket_text = f"📦 Qolgan paketlar soni: {paketlar}" if paketlar != 'Yo‘q' else "📦 Paketlar mavjud emas."

    await update.message.reply_text(
        f"{paket_text}\n{vip_text}"
    )
