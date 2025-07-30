import asyncpg

DB_URL = "postgresql://postgres:GyfySBHYtMgPaAGvMhkxAkONuhanoMtT@postgres.railway.internal:5432/railway"

class Database:
    def __init__(self):
        self.pool = None

    async def init(self):
        self.pool = await asyncpg.create_pool(DB_URL)
        await self.create_tables()

    async def create_tables(self):
        async with self.pool.acquire() as conn:
            await conn.execute('''
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
                );
            ''')

            await conn.execute('''
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
                );
            ''')

            await conn.execute('''
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
                );
            ''')

            await conn.execute('''
                CREATE TABLE IF NOT EXISTS raqamlar_olingan (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT,
                    elon_id INTEGER,
                    elon_turi TEXT,
                    sanasi TEXT
                );
            ''')

            await conn.execute('''
                CREATE TABLE IF NOT EXISTS tolov_log (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT,
                    summa INTEGER,
                    sana TEXT,
                    izoh TEXT
                );
            ''')

    async def foydalanuvchi_qoshish(self, user_id, username):
        async with self.pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO foydalanuvchilar (user_id, username)
                VALUES ($1, $2) ON CONFLICT (user_id) DO NOTHING
            ''', user_id, username)

    async def foydalanuvchi_mavjudmi(self, user_id):
        async with self.pool.acquire() as conn:
            result = await conn.fetchrow("SELECT 1 FROM foydalanuvchilar WHERE user_id = $1", user_id)
            return result is not None

    async def foydalanuvchilar_soni(self):
        async with self.pool.acquire() as conn:
            return await conn.fetchval("SELECT COUNT(*) FROM foydalanuvchilar")

    async def balans_oshirish(self, user_id, miqdor):
        async with self.pool.acquire() as conn:
            await conn.execute(
                "UPDATE foydalanuvchilar SET balans = balans + $1 WHERE user_id = $2",
                miqdor, user_id
            )

    async def balans_olish(self, user_id):
        async with self.pool.acquire() as conn:
            result = await conn.fetchrow(
                "SELECT balans FROM foydalanuvchilar WHERE user_id = $1",
                user_id
            )
            return result["balans"] if result else 0

    async def tolov_log_qoshish(self, user_id, summa, sana, izoh):
        async with self.pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO tolov_log (user_id, summa, sana, izoh)
                VALUES ($1, $2, $3, $4)
            ''', user_id, summa, sana, izoh)

    async def raqam_olingan_qoshish(self, user_id, elon_id, elon_turi, sanasi):
        async with self.pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO raqamlar_olingan (user_id, elon_id, elon_turi, sanasi)
                VALUES ($1, $2, $3, $4)
            ''', user_id, elon_id, elon_turi, sanasi)

    async def raqam_olingan_soni_yuk(self, elon_id):
        async with self.pool.acquire() as conn:
            await conn.execute(
                "UPDATE yuk_elonlar SET raqam_olingan = raqam_olingan + 1 WHERE id = $1",
                elon_id
            )

    async def raqam_olingan_soni_shofyor(self, elon_id):
        async with self.pool.acquire() as conn:
            await conn.execute(
                "UPDATE shofyor_elonlar SET raqam_olingan = raqam_olingan + 1 WHERE id = $1",
                elon_id
            )

    async def elon_korilgan_yuk(self, elon_id):
        async with self.pool.acquire() as conn:
            await conn.execute(
                "UPDATE yuk_elonlar SET korilgan = korilgan + 1 WHERE id = $1",
                elon_id
            )

    async def elon_korilgan_shofyor(self, elon_id):
        async with self.pool.acquire() as conn:
            await conn.execute(
                "UPDATE shofyor_elonlar SET korilgan = korilgan + 1 WHERE id = $1",
                elon_id
            )


# Ishga tushurish
db = Database()

async def db_start():
    await db.init()
