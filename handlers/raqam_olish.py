from database import cursor, conn
from config import RAQAM_NARX
import datetime

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
    if elon_turi == 'yuk':
        cursor.execute('SELECT telefon FROM yuk_elonlar WHERE id=?', (elon_id,))
    else:
        cursor.execute('SELECT telefon FROM shofyor_elonlar WHERE id=?', (elon_id,))

    tel_result = cursor.fetchone()
    if tel_result:
        telefon = tel_result[0]

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

    # KORILGAN SONINI +1 QILISH
    if elon_turi == 'yuk':
        cursor.execute('UPDATE yuk_elonlar SET korilgan = korilgan + 1 WHERE id=?', (elon_id,))
    else:
        cursor.execute('UPDATE shofyor_elonlar SET korilgan = korilgan + 1 WHERE id=?', (elon_id,))

    conn.commit()

    await query.edit_message_text(
        f"📞 Telefon raqam: {telefon}\n\n"
        "✅ Raqam muvaffaqiyatli olindi!"
    )
