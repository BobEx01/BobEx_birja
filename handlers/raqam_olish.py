from database import cursor, conn
from config import RAQAM_NARX
import datetime
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

async def raqam_olish_handler(update, context):
    query = update.callback_query
    await query.answer()

    data = query.data.split('_')
    elon_turi = data[0]  # yuk yoki shofyor
    elon_id = int(data[-1])
    user_id = query.from_user.id

    # Foydalanuvchi balansini tekshirish
    cursor.execute('SELECT balans FROM foydalanuvchilar WHERE user_id=?', (user_id,))
    result = cursor.fetchone()

    if not result or result[0] < RAQAM_NARX:
        await query.edit_message_text(
            f"❌ Balansingiz yetarli emas. Raqam olish uchun {RAQAM_NARX} so‘m kerak.\n\n"
            "💳 Balansingizni to‘ldiring: /hisobim"
        )
        return

    # Raqam olish
    telefon = ''
    elon_egasi = None
    if elon_turi == 'yuk':
        cursor.execute('SELECT telefon, user_id FROM yuk_elonlar WHERE id=?', (elon_id,))
    else:
        cursor.execute('SELECT telefon, user_id FROM shofyor_elonlar WHERE id=?', (elon_id,))

    tel_result = cursor.fetchone()
    if tel_result:
        telefon = tel_result[0]
        elon_egasi = tel_result[1]

    if not telefon:
        await query.edit_message_text("❌ Kechirasiz, telefon raqami topilmadi.")
        return

    # Balansdan yechish
    cursor.execute('UPDATE foydalanuvchilar SET balans = balans - ? WHERE user_id=?',
                   (RAQAM_NARX, user_id))
    
    # Logga yozish
    cursor.execute('''
    INSERT INTO raqamlar_olingan (user_id, elon_id, elon_turi, sanasi)
    VALUES (?, ?, ?, ?)
    ''', (user_id, elon_id, elon_turi, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    # KORILGAN +1
    if elon_turi == 'yuk':
        cursor.execute('UPDATE yuk_elonlar SET korilgan = korilgan + 1, raqam_olingan = raqam_olingan + 1 WHERE id=?', (elon_id,))
    else:
        cursor.execute('UPDATE shofyor_elonlar SET korilgan = korilgan + 1, raqam_olingan = raqam_olingan + 1 WHERE id=?', (elon_id,))

    conn.commit()

    await query.edit_message_text(
        f"📞 Telefon raqam: {telefon}\n\n"
        "✅ Raqam muvaffaqiyatli olindi!"
    )

    # ELON EGASIGA OG'OHLANTIRISH VA O‘CHIRISH/QOLDIRISH TUGMALARI
    if elon_egasi:
        if elon_turi == 'yuk':
            tugmalar = InlineKeyboardMarkup([
                [InlineKeyboardButton("❌ E'lonni o‘chirish", callback_data=f"yuk_ochir_{elon_id}")],
                [InlineKeyboardButton("✅ E'lonni qoldirish", callback_data=f"yuk_qoldir_{elon_id}")]
            ])
        else:  # shofyor
            tugmalar = InlineKeyboardMarkup([
                [InlineKeyboardButton("❌ E'lonni o‘chirish", callback_data=f"ochir_shofyor_{elon_id}")],
                [InlineKeyboardButton("✅ E'lonni qoldirish", callback_data=f"uzaytir_shofyor_{elon_id}")]
            ])

        try:
            await context.bot.send_message(
                chat_id=elon_egasi,
                text=(
                    f"📢 Sizning e’loningiz bo‘yicha raqamingiz olindi!\n"
                    f"🆔 E'lon ID: {elon_id}\n"
                    f"📞 Sizning raqamingiz: {telefon}\n\n"
                    "👇 Quyidagi tugmalar orqali e'loningizni boshqarishingiz mumkin."
                ),
                reply_markup=tugmalar
            )
        except Exception as e:
            print(f"Elon egasiga xabar yuborishda xato: {e}")
