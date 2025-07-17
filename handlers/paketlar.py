from database import cursor, conn
from datetime import datetime, timedelta
from config import VIP_NARX
from handlers.start import asosiy_menu

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

    # VIP paket faollashtirish va balansdan yechish
    vip_muddati = datetime.now() + timedelta(days=30)
    cursor.execute("""
        UPDATE foydalanuvchilar 
        SET balans = balans - ?, vip_muddati = ?
        WHERE user_id = ?
    """, (VIP_NARX, vip_muddati.strftime('%Y-%m-%d'), user_id))
    conn.commit()

    await update.message.reply_text(
        f"🎉 Tabriklaymiz! VIP paket faollashtirildi.\n"
        f"📅 Amal qilish muddati: {vip_muddati.strftime('%Y-%m-%d')}\n"
        f"🏠 Asosiy menyu:", reply_markup=asosiy_menu()
    )

    # Adminni xabardor qilish
    ADMIN_ID = 8080091052
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"👑 Foydalanuvchi {user_id} VIP paket sotib oldi. VIP muddati: {vip_muddati.strftime('%Y-%m-%d')}."
    )


async def paket_stat(update, context):
    user_id = update.message.from_user.id
    cursor.execute("""
        SELECT balans, paket_soni, vip_muddati 
        FROM foydalanuvchilar 
        WHERE user_id = ?
    """, (user_id,))
    result = cursor.fetchone()

    if not result:
        await update.message.reply_text("❌ Statistika topilmadi. Avval ro‘yxatdan o‘ting /start")
        return

    balans, paket_soni, vip_muddati = result
    vip_status = "❌ Yo‘q"
    if vip_muddati:
        today = datetime.now().date()
        vip_date = datetime.strptime(vip_muddati, '%Y-%m-%d').date()
        if vip_date >= today:
            vip_status = f"✅ {vip_muddati} gacha faollikda"

    text = (
        f"📊 <b>Statistika:</b>\n\n"
        f"💰 <b>Balans:</b> {balans} so‘m\n"
        f"🎟 <b>Qolgan paketlar:</b> {paket_soni} ta\n"
        f"👑 <b>VIP holat:</b> {vip_status}"
    )
    await update.message.reply_text(text, parse_mode='HTML')
