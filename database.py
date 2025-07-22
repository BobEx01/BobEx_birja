import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL")  # Railway Variables dan olinadi

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# --- Jadval yaratishlar ---
cursor.execute('''
CREATE TABLE IF NOT EXISTS foydalanuvchilar (
    user_id BIGINT PRIMARY KEY,
    username TEXT,
    balans INTEGER DEFAULT 0,
    bonus_berildi BOOLEAN DEFAULT FALSE,
    paket_soni INTEGER DEFAULT 0,
    vip_oxirgi TEXT DEFAULT 'Yo‘q',
    sarflangan INTEGER DEFAULT 0,
    paketlar TEXT DEFAULT 'Yo‘q',
    toldirilgan INTEGER DEFAULT 0,
    referal_id BIGINT DEFAULT 0
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS yuk_elonlar (
    id SERIAL PRIMARY KEY,
    user_id BIGINT,
    viloyat TEXT,
    tuman TEXT,
    qayerdan TEXT,
    qayerga TEXT,
    ogirlik TEXT,
    mashina TEXT,
    narx INTEGER,
    telefon TEXT,
    premium BOOLEAN DEFAULT FALSE,
    sanasi TEXT,
    muddat TEXT,
    korilgan INTEGER DEFAULT 0,
    raqam_olingan INTEGER DEFAULT 0
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS shofyor_elonlar (
    id SERIAL PRIMARY KEY,
    user_id BIGINT,
    viloyat TEXT,
    tuman TEXT,
    qayerdan TEXT,
    qayerga TEXT,
    ism TEXT,
    mashina TEXT,
    sigim TEXT,
    narx INTEGER,
    telefon TEXT,
    premium BOOLEAN DEFAULT FALSE,
    sanasi TEXT,
    muddat TEXT,
    korilgan INTEGER DEFAULT 0,
    raqam_olingan INTEGER DEFAULT 0
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS raqamlar_olingan (
    id SERIAL PRIMARY KEY,
    user_id BIGINT,
    elon_id INTEGER,
    elon_turi TEXT,
    sanasi TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS tolov_log (
    id SERIAL PRIMARY KEY,
    user_id BIGINT,
    summa INTEGER,
    sana TEXT,
    izoh TEXT
)
''')

conn.commit()

# === FUNKSIYALAR ===

def foydalanuvchi_qoshish(user_id: int, username: str):
    cursor.execute("INSERT INTO foydalanuvchilar (user_id, username) VALUES (%s, %s) ON CONFLICT (user_id) DO NOTHING", (user_id, username))
    conn.commit()

def balans_oshirish(user_id: int, miqdor: int):
    cursor.execute("UPDATE foydalanuvchilar SET balans = balans + %s WHERE user_id = %s", (miqdor, user_id))
    conn.commit()

def balans_olish(user_id: int):
    cursor.execute("SELECT balans FROM foydalanuvchilar WHERE user_id = %s", (user_id,))
    natija = cursor.fetchone()
    return natija[0] if natija else 0

def raqam_olingan_qoshish(user_id: int, elon_id: int, elon_turi: str, sanasi: str):
    cursor.execute('''
    INSERT INTO raqamlar_olingan (user_id, elon_id, elon_turi, sanasi) VALUES (%s, %s, %s, %s)
    ''', (user_id, elon_id, elon_turi, sanasi))
    conn.commit()

def raqam_olingan_soni_yuk(elon_id: int):
    cursor.execute("UPDATE yuk_elonlar SET raqam_olingan = raqam_olingan + 1 WHERE id = %s", (elon_id,))
    conn.commit()

def raqam_olingan_soni_shofyor(elon_id: int):
    cursor.execute("UPDATE shofyor_elonlar SET raqam_olingan = raqam_olingan + 1 WHERE id = %s", (elon_id,))
    conn.commit()

def elon_korilgan_yuk(elon_id: int):
    cursor.execute("UPDATE yuk_elonlar SET korilgan = korilgan + 1 WHERE id = %s", (elon_id,))
    conn.commit()

def elon_korilgan_shofyor(elon_id: int):
    cursor.execute("UPDATE shofyor_elonlar SET korilgan = korilgan + 1 WHERE id = %s", (elon_id,))
    conn.commit()

def foydalanuvchi_mavjudmi(user_id: int):
    cursor.execute("SELECT 1 FROM foydalanuvchilar WHERE user_id = %s", (user_id,))
    return cursor.fetchone() is not None

def tolov_log_qoshish(user_id: int, summa: int, sana: str, izoh: str):
    cursor.execute('''
    INSERT INTO tolov_log (user_id, summa, sana, izoh) VALUES (%s, %s, %s, %s)
    ''', (user_id, summa, sana, izoh))
    conn.commit()

def foydalanuvchilar_soni():
    cursor.execute("SELECT COUNT(*) FROM foydalanuvchilar")
    natija = cursor.fetchone()
    return natija[0] if natija else 0
