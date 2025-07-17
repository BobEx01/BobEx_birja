from database import cursor, conn
from config import PREMIUM_ELON_NARX, VIP_NARX, ADMIN_ID
from datetime import datetime, timedelta
from handlers.start import asosiy_menu

async def premium_elon(update, context):
    user_id = update.message.from_user.id

    cursor.execute('SELECT balans FROM foydalanuvchilar WHERE user_id=?', (user_id,))
    result = cursor.fetchone()
    if not result or result[0] < PREMIUM_ELON_NARX:
        await update.message.reply_text(
            f"❌ Balansingiz yetarli emas. Premium e’lon uchun {PREMIUM_ELON_NARX} so‘m kerak.\n"
            "💳 Balansni to‘ldiring: /hisobim"
        )
        return

    cursor.execute('UPDATE foydalanuvchilar SET balans = balans - ?, sarflangan = sarflangan + ? WHERE user_id=?',
                   (PREMIUM_ELON_NARX, PREMIUM_ELON_NARX, user_id))
    conn.commit()

    await update.message.reply_text(
        "✅ Premium e’lon muvaffaqiyatli faollashtirildi!\n"
        "Endi e’loningiz ro‘yxatda yuqorida chiqadi."
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📣 Foydalanuvchi {user_id} premium e’lon faollashtirdi.\n💰 {PREMIUM_ELON_NARX} so‘m balansidan yechildi."
    )


async def vip_aktiv(update, context):
    user_id = update.message.from_user.id
    cursor.execute('SELECT balans FROM foydalanuvchilar WHERE user_id=?', (user_id,))
    result = cursor.fetchone()

    if not result or result[0] < VIP_NARX:
        await update.message.reply_text(
            f"❌ Balansingiz yetarli emas. VIP olish uchun {VIP_NARX} so‘m kerak.\n"
            "💳 Balansni to‘ldiring: /hisobim"
        )
        return

    vip_muddati = datetime.now() + timedelta(days=30)
    cursor.execute('UPDATE foydalanuvchilar SET balans = balans - ?, sarflangan = sarflangan + ?, vip_oxirgi = ? WHERE user_id=?',
                   (VIP_NARX, VIP_NARX, vip_muddati.strftime('%Y-%m-%d'), user_id))
    conn.commit()

    await update.message.reply_text(
        f"👑 VIP statusingiz faollashtirildi!\n📅 Amal qilish muddati: {vip_muddati.strftime('%Y-%m-%d')}",
        reply_markup=asosiy_menu()
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"👑 Foydalanuvchi {user_id} VIP paket sotib oldi. Amal qilish muddati: {vip_muddati.strftime('%Y-%m-%d')}."
    )
