# database.py
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

db_pool = None

async def init_db():
    global db_pool
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is missing!")

    db_pool = await asyncpg.create_pool(dsn=database_url)
    print("✅ Connected to PostgreSQL")

    # Jadval yaratish (agar mavjud bo‘lmasa)
    async with db_pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS kino_codes (
                code TEXT PRIMARY KEY,
                title TEXT,
                channel TEXT,
                message_id INTEGER,
                post_count INTEGER
            );
        """)

async def close_db():
    global db_pool
    if db_pool:
        await db_pool.close()
        print("❌ DB connection closed")


@dp.message_handler(commands=["codes"])
async def list_codes(message: types.Message):
    codes = await get_all_codes()
    if not codes:
        await message.answer("📭 Hozircha hech qanday kod yo‘q.")
        return

    text = "📋 Kodlar ro‘yxati:\n\n"
    for c in codes:
        text += f"{c['code']} — {c['title']}\n"

    await message.answer(text)

