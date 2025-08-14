from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from database import init_db, close_db, get_all_codes
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

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

async def on_startup(_):
    await init_db()

async def on_shutdown(_):
    await close_db()

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
