# database.py — Bobex uchun Postgres DB qatlami (handlers bilan mos)
# Muvofiqlik: python-telegram-bot 20.x
# ENV: DATABASE_URL=postgresql://USER:PASS@HOST:PORT/DBNAME

import os
import re
import psycopg2
from psycopg2 import sql

# --- Ulanish ---
DB_URL = os.getenv("DATABASE_URL", "").strip()
if not DB_URL:
    # Agar ENV yo'q bo'lsa, vaqtincha xatoni aniq ko'rsatamiz
    raise RuntimeError("DATABASE_URL topilmadi. Railway Variables ga DATABASE_URL kiriting.")

conn = psycopg2.connect(DB_URL)
conn.autocommit = False  # commit() larni qo'lda boshqaramiz

# Ichki yagona cursor. Oddiy ketma-ket so'rovlar uchun yetarli.
_raw_cursor = conn.cursor()

# --- SQLite -> Postgres moslashtirish ---
def _adapt_query(sql_text: str) -> str:
    """
    Handlerlardagi eski SQLite yozuvlarini Postgresga moslaydi:
      1) '?' -> '%s'
      2) 'INSERT OR IGNORE INTO foydalanuvchilar' -> 'INSERT INTO ... ON CONFLICT (user_id) DO NOTHING'
    Eslatma: Boshqa jadvallarda 'OR IGNORE' ishlatilsa, alohida qo'shib beraman.
    """
    q = sql_text.replace("?", "%s")

    # Faqat foydalanuvchilar jadvali uchun umumiy migratsiya
    q = re.sub(
        r"INSERT\s+OR\s+IGNORE\s+INTO\s+foydalanuvchilar",
        "INSERT INTO foydalanuvchilar",
        q,
        flags=re.IGNORECASE
    )
    if "INSERT INTO foydalanuvchilar" in q and "ON CONFLICT" not in q:
        q = q + " ON CONFLICT (user_id) DO NOTHING"

    return q

class CursorWrapper:
    """handlers ichida sqlite uslubida yozilgan kodlarni buzmasdan ishlatish uchun o'ram."""
    def execute(self, query, params=None):
        q = _adapt_query(query)
        if params is not None:
            _raw_cursor.execute(q, params)
        else:
            _raw_cursor.execute(q)

    def fetchone(self):
        return _raw_cursor.fetchone()

    def fetchall(self):
        return _raw_cursor.fetchall()

cursor = CursorWrapper()  # handlers import qiladi: cursor
# handlers import qiladi: conn ham kerak (commit uchun)

# --- Jadval yaratish ---
def init_db():
    """
    Dastur startida bir marta chaqiring.
    Barcha jadvallar mavjud bo‘lmasa — yaratadi.
    """
    with conn:
        with conn.cursor() as c:
            # Foydalanuvchilar
            c.execute("""
                CREATE TABLE IF NOT EXISTS foydalanuvchilar (
                    user_id      BIGINT PRIMARY KEY,
                    username     TEXT,
                    first_name   TEXT,
                    balans       INTEGER DEFAULT 0,
                    bonus_berildi BOOLEAN DEFAULT FALSE,
                    paket_soni   INTEGER DEFAULT 0,
                    vip_oxirgi   TEXT DEFAULT 'Yo‘q',
                    sarflangan   INTEGER DEFAULT 0,
                    paketlar     TEXT DEFAULT 'Yo‘q',
                    toldirilgan  INTEGER DEFAULT 0,
                    referal_id   BIGINT DEFAULT 0,
                    created_at   TIMESTAMP DEFAULT NOW()
                );
            """)

            # Yuk e'lonlari
            c.execute("""
                CREATE TABLE IF NOT EXISTS yuk_elonlar (
                    id              SERIAL PRIMARY KEY,
                    user_id         BIGINT REFERENCES foydalanuvchilar(user_id),
                    viloyat         TEXT,
                    tuman           TEXT,
                    qayerdan        TEXT,
                    qayerga         TEXT,
                    ogirlik         TEXT,
                    mashina         TEXT,
                    narx            INTEGER,
                    telefon         TEXT,
                    premium         BOOLEAN DEFAULT FALSE,
                    sanasi          TIMESTAMP DEFAULT NOW(),
                    muddat          TEXT,
                    korilgan        INTEGER DEFAULT 0,
                    raqam_olingan   INTEGER DEFAULT 0,
                    izoh            TEXT
                );
            """)

            # Haydovchi e'lonlari
            c.execute("""
                CREATE TABLE IF NOT EXISTS shofyor_elonlar (
                    id              SERIAL PRIMARY KEY,user_id         BIGINT REFERENCES foydalanuvchilar(user_id),
                    viloyat         TEXT,
                    tuman           TEXT,
                    qayerdan        TEXT,
                    qayerga         TEXT,
                    ism             TEXT,
                    mashina         TEXT,
                    sigim           TEXT,
                    narx            INTEGER,
                    telefon         TEXT,
                    premium         BOOLEAN DEFAULT FALSE,
                    sanasi          TIMESTAMP DEFAULT NOW(),
                    muddat          TEXT,
                    korilgan        INTEGER DEFAULT 0,
                    raqam_olingan   INTEGER DEFAULT 0,
                    izoh            TEXT
                );
            """)

            # Olingan raqamlar logi
            c.execute("""
                CREATE TABLE IF NOT EXISTS raqamlar_olingan (
                    id        SERIAL PRIMARY KEY,
                    user_id   BIGINT,
                    elon_id   INTEGER,
                    elon_turi TEXT,
                    sanasi    TIMESTAMP DEFAULT NOW()
                );
            """)

# --- Qulay yordamchi funksiyalar ---
def foydalanuvchilar_soni() -> int:
    cursor.execute("SELECT COUNT(*) FROM foydalanuvchilar")
    row = cursor.fetchone()
    return int(row[0]) if row else 0

def foydalanuvchi_mavjudmi(user_id: int) -> bool:
    cursor.execute("SELECT 1 FROM foydalanuvchilar WHERE user_id = %s", (user_id,))
    return cursor.fetchone() is not None

def commit():
    """Qo'lda commit qilish kerak bo'lganda."""
    conn.commit()

def rollback():
    """Xatoda ortga qaytarish."""
    conn.rollback()
