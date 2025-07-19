import sqlite3

conn = sqlite3.connect('bobex.db', check_same_thread=False)
cursor = conn.cursor()

# --- Jadval yaratishlar ---
cursor.execute('''
CREATE TABLE IF NOT EXISTS foydalanuvchilar (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    balans INTEGER DEFAULT 0,
    bonus_berildi BOOLEAN DEFAULT 0,
    paket_soni INTEGER DEFAULT 0,
    vip_oxirgi TEXT DEFAULT 'Yo‘q',
    sarflangan INTEGER DEFAULT 0,
    paketlar TEXT DEFAULT 'Yo‘q',
    toldirilgan INTEGER DEFAULT 0
)
''')

# --- referal_id ustuni mavjudligini tekshirish va yo‘q bo‘lsa qo‘shish ---
cursor.execute("PRAGMA table_info(foydalanuvchilar)")
ustunlar = [row[1] for row in cursor.fetchall()]
if 'referal_id' not in ustunlar:
    cursor.execute('ALTER TABLE foydalanuvchilar ADD COLUMN referal_id INTEGER DEFAULT 0')
    conn.commit()


cursor.execute('''
CREATE TABLE IF NOT EXISTS yuk_elonlar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    viloyat TEXT,
    tuman TEXT,
    qayerdan TEXT,
    qayerga TEXT,
    ogirlik TEXT,
    mashina TEXT,
    narx INTEGER,
    telefon TEXT,
    premium BOOLEAN DEFAULT 0,
    sanasi TEXT,
    muddat TEXT,
    korilgan INTEGER DEFAULT 0,
    raqam_olingan INTEGER DEFAULT 0
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS shofyor_elonlar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    viloyat TEXT,
    tuman TEXT,
    qayerdan TEXT,
    qayerga TEXT,
    ism TEXT,
    mashina TEXT,
    sigim TEXT,
    narx INTEGER,
    telefon TEXT,
    premium BOOLEAN DEFAULT 0,
    sanasi TEXT,
    muddat TEXT,
    korilgan INTEGER DEFAULT 0,
    raqam_olingan INTEGER DEFAULT 0
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS raqamlar_olingan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    elon_id INTEGER,
    elon_turi TEXT,
    sanasi TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS tolov_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    summa INTEGER,
    sana TEXT,
    izoh TEXT
)
''')

conn.commit()


# === Funksiyalar ===

def foydalanuvchi_qoshish(user_id: int, username: str):
    cursor.execute("INSERT OR IGNORE INTO foydalanuvchilar (user_id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()

def balans_oshirish(user_id: int, miqdor: int):
    cursor.execute("UPDATE foydalanuvchilar SET balans = balans + ? WHERE user_id = ?", (miqdor, user_id))
    conn.commit()

def balans_olish(user_id: int):
    cursor.execute("SELECT balans FROM foydalanuvchilar WHERE user_id = ?", (user_id,))
    natija = cursor.fetchone()
    return natija[0] if natija else 0

def raqam_olingan_qoshish(user_id: int, elon_id: int, elon_turi: str, sanasi: str):
    cursor.execute('''
    INSERT INTO raqamlar_olingan (user_id, elon_id, elon_turi, sanasi) VALUES (?, ?, ?, ?)
    ''', (user_id, elon_id, elon_turi, sanasi))
    conn.commit()

def raqam_olingan_soni_yuk(elon_id: int):
    cursor.execute("UPDATE yuk_elonlar SET raqam_olingan = raqam_olingan + 1 WHERE id = ?", (elon_id,))
    conn.commit()

def raqam_olingan_soni_shofyor(elon_id: int):
    cursor.execute("UPDATE shofyor_elonlar SET raqam_olingan = raqam_olingan + 1 WHERE id = ?", (elon_id,))
    conn.commit()

def elon_korilgan_yuk(elon_id: int):
    cursor.execute("UPDATE yuk_elonlar SET korilgan = korilgan + 1 WHERE id = ?", (elon_id,))
    conn.commit()

def elon_korilgan_shofyor(elon_id: int):
    cursor.execute("UPDATE shofyor_elonlar SET korilgan = korilgan + 1 WHERE id = ?", (elon_id,))
    conn.commit()

def foydalanuvchi_mavjudmi(user_id: int):
    cursor.execute("SELECT 1 FROM foydalanuvchilar WHERE user_id = ?", (user_id,))
    return cursor.fetchone() is not None

def tolov_log_qoshish(user_id: int, summa: int, sana: str, izoh: str):
    cursor.execute('''
    INSERT INTO tolov_log (user_id, summa, sana, izoh) VALUES (?, ?, ?, ?)
    ''', (user_id, summa, sana, izoh))
    conn.commit()


# === YANGI: FOYDALANUVCHILAR SONI FUNKSIYASI ===

def foydalanuvchilar_soni():
    cursor.execute("SELECT COUNT(*) FROM foydalanuvchilar")
    natija = cursor.fetchone()return natija[0] if natija else 0
