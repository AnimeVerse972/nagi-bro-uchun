# main.py
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

from database import init_db, close_db, get_all_codes

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is missing!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


# === Start komandasi ===
@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await message.answer("Salom! Kodlar ro‘yxatini olish uchun /codes ni bosing.")


# === Kodlar ro‘yxatini ko‘rsatish (oddiy format) ===
@dp.message_handler(commands=["codes"])
async def show_codes(message: types.Message):
    codes = await get_all_codes()

    if not codes:
        await message.answer("📭 Hozircha hech qanday kod mavjud emas.")
        return

    text_lines = [f"{c['code']} — {c['title']}" for c in codes]
    await message.answer("\n".join(text_lines))


# === Botni ishga tushirish ===
async def on_startup(dp):
    await init_db()
    print("Bot ishga tushdi!")


async def on_shutdown(dp):
    await close_db()
    print("Bot to‘xtadi!")


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
