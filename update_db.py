import sqlite3

conn = sqlite3.connect('bobex.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute("ALTER TABLE foydalanuvchilar ADD COLUMN paket_soni INTEGER DEFAULT 0")
cursor.execute("ALTER TABLE foydalanuvchilar ADD COLUMN vip_oxirgi TEXT DEFAULT 'Yo‘q'")
cursor.execute("ALTER TABLE foydalanuvchilar ADD COLUMN sarflangan INTEGER DEFAULT 0")

conn.commit()
print("✅ Ustunlar muvaffaqiyatli qo‘shildi!")
