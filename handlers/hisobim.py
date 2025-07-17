from telegram import Update
from telegram.ext import ContextTypes
from database import cursor, conn
from handlers.start import asosiy_menu

BONUS_MIqdori = 50000

async def hisobim_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    cursor.execute("SELECT balans, bonus_berildi, paket_soni, toldirilgan, vip_oxirgi, sarflangan FROM foydalanuvchilar WHERE user_id = ?", (user_id,))
    user_data = cursor.fetchone()

    if user_data:
        balans, bonus_berildi, paket_soni, toldirilgan, vip_oxirgi, sarflangan = user_data

        if not bonus_berildi:
            balans += BONUS_MIqdori
            cursor.execute("UPDATE foydalanuvchilar SET balans = ?, bonus_berildi = 1 WHERE user_id = ?", (balans, user_id))
            conn.commit()
    else:
        balans = BONUS_MIqdori
        paket_soni = 0
        toldirilgan = 0
        vip_oxirgi = 'Yo‘q'
        sarflangan = 0
        cursor.execute(
            "INSERT INTO foydalanuvchilar (user_id, balans, bonus_berildi, paket_soni, toldirilgan, vip_oxirgi, sarflangan) "
            "VALUES (?, ?, 1, ?, ?, ?, ?)",
            (user_id, balans, paket_soni, toldirilgan, vip_oxirgi, sarflangan)
        )
        conn.commit()

    vip_muddat = vip_oxirgi if vip_oxirgi else "Yo‘q"

    text = (
        f"📊 *Hisobingiz haqida ma'lumot:*\n\n"
        f"🆔 Foydalanuvchi ID: `{user_id}`\n"
        f"💰 Balans: *{balans} so'm*\n"
        f"🎟 Qolgan paketlar soni: {paket_soni} ta\n"
        f"👑 VIP paket muddati: {vip_muddat}\n"
        f"➕ To‘ldirilgan summa: {toldirilgan} so'm\n"
        f"📈 Umumiy sarflangan: {sarflangan} so'm\n"
        f"🎉 Bonus: {BONUS_MIqdori} so'm (faqat bir marta beriladi)\n\n"
        "_Balans faqat xizmatlar uchun sarflanadi va qaytarilmaydi._"
    )

    await update.message.reply_text(text, parse_mode='Markdown', reply_markup=asosiy_menu())
