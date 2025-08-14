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

async def get_all_codes():
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("SELECT code, title FROM kino_codes")
        return [{"code": row["code"], "title": row["title"]} for row in rows]

