from database import cursor, conn
from datetime import datetime, timedelta
from config import PAKET_10_NARX, VIP_NARX, ADMIN_ID
from keyboards.menu import main_menu as asosiy_menu

async def paketlar_handler(update, context):
    text = (
        "🎟 <b>Paketlar va Aksiyalar:</b>\n\n"
        "1️⃣ 10 ta raqam olish paketi - 186,000 so‘m (33% chegirma)\n"
        "2️⃣ Har juma kuni - <b>50% chegirma</b> barcha funksiyalar uchun!\n"
        "3️⃣ VIP tarif - 1,000,000 so‘m (30 kun davomida barcha xizmatlar bepul)\n\n"
        "🔹 Paket olish uchun: /paket_ol\n"
        "🔹 VIP paket olish uchun: /vip_paket_ol\n"
        "🔹 Statistika: /paket_stat"
    )
    await update.message.reply_text(text, parse_mode='HTML')


async def paket_ol(update, context):
    user_id = update.message.from_user.id
    cursor.execute("SELECT balans FROM foydalanuvchilar WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    if not result or result[0] < PAKET_10_NARX:
        await update.message.reply_text(
            f"❌ Balansingiz yetarli emas. 10 ta paket uchun {PAKET_10_NARX} so‘m kerak.\n"
            "💳 Balansni to‘ldiring: /hisobim"
        )
        return

    cursor.execute("""
        UPDATE foydalanuvchilar 
        SET balans = balans - ?, sarflangan = sarflangan + ?, paket_soni = paket_soni + 10
        WHERE user_id = ?
    """, (PAKET_10_NARX, PAKET_10_NARX, user_id))
    conn.commit()

    await update.message.reply_text(
        "✅ 10 ta raqam olish paketi muvaffaqiyatli sotib olindi!\n"
        "Endi balansdan yechmasdan 10 ta raqam olishingiz mumkin."
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📦 User {user_id} 10 ta raqam olish paketini sotib oldi."
    )


async def vip_paket_ol(update, context):
    user_id = update.message.from_user.id
    cursor.execute("SELECT balans FROM foydalanuvchilar WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    if not result:
        await update.message.reply_text("❌ Balansingiz topilmadi. Avval ro‘yxatdan o‘ting /start")
        return

    balans = result[0]
    if balans < VIP_NARX:
        await update.message.reply_text(
            f"❌ VIP paket uchun balans yetarli emas. Kerakli summa: {VIP_NARX} so‘m.\n"
            "💳 Hisobni to‘ldiring: /hisobim"
        )
        return

    vip_oxirgi = datetime.now() + timedelta(days=30)
    cursor.execute("""
        UPDATE foydalanuvchilar 
        SET balans = balans - ?, sarflangan = sarflangan + ?, vip_oxirgi = ?
        WHERE user_id = ?
    """, (VIP_NARX, VIP_NARX, vip_oxirgi.strftime('%Y-%m-%d'), user_id))
    conn.commit()

    await update.message.reply_text(
        f"🎉 Tabriklaymiz! VIP paket faollashtirildi.\n"
        f"📅 Amal qilish muddati: {vip_oxirgi.strftime('%Y-%m-%d')}\n",
        reply_markup=asosiy_menu()
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"👑 User {user_id} VIP paket sotib oldi. Muddati: {vip_oxirgi.strftime('%Y-%m-%d')}."
    )


async def paket_stat(update, context):
    user_id = update.message.from_user.id
    cursor.execute("""
        SELECT balans, paket_soni, vip_oxirgi 
        FROM foydalanuvchilar 
        WHERE user_id = ?
    """, (user_id,))
    result = cursor.fetchone()

    if not result:
        await update.message.reply_text("❌ Statistika topilmadi. Avval ro‘yxatdan o‘ting /start")
        return

    balans, paket_soni, vip_oxirgi = result
    vip_status = "❌ Yo‘q"
    if vip_oxirgi:
        today = datetime.now().date()
        vip_date = datetime.strptime(vip_oxirgi, '%Y-%m-%d').date()
        if vip_date >= today:
            vip_status = f"✅ {vip_oxirgi} gacha faollikda"

    text = (
        f"📊 <b>Statistika:</b>\n\n"
        f"💰 <b>Balans:</b> {balans} so‘m\n"
        f"🎟 <b>Qolgan paketlar:</b> {paket_soni} ta\n"
        f"👑 <b>VIP holat:</b> {vip_status}"
    )
    await update.message.reply_text(text, parse_mode='HTML')
