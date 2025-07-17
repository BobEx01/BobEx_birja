import sqlite3

conn = sqlite3.connect('bobex.db', check_same_thread=False)
cursor = conn.cursor()

# --- Foydalanuvchilar jadvali ---
cursor.execute('''
CREATE TABLE IF NOT EXISTS foydalanuvchilar (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    balans INTEGER DEFAULT 0,
    bonus_berildi BOOLEAN DEFAULT 0,
    paketlar TEXT DEFAULT 'Yo‘q',
    toldirilgan INTEGER DEFAULT 0
)
''')

# --- Yuk e'lonlar ---
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
    sanasi TEXT
)
''')

# --- Shofyor e'lonlar ---
cursor.execute('''
CREATE TABLE IF NOT EXISTS shofyor_elonlar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    viloyat TEXT,
    tuman TEXT,
    mashina TEXT,
    sigim TEXT,
    narx INTEGER,
    telefon TEXT,
    premium BOOLEAN DEFAULT 0,
    sanasi TEXT
)
''')

# --- Olingan raqamlar ---
cursor.execute('''
CREATE TABLE IF NOT EXISTS raqamlar_olingan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    elon_id INTEGER,
    elon_turi TEXT,
    sanasi TEXT
)
''')

# --- Tolov loglari ---
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
