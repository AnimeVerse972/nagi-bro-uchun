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
async def kodlar(message: types.Message):
    kodlar = await get_all_codes()
    if not kodlar:
        await message.answer("⛔️ Hech qanday kod topilmadi.")
        return

    # Kodlarni raqam bo‘yicha kichikdan kattasiga saralash
    kodlar = sorted(kodlar, key=lambda x: int(x["code"]))

    text = "📄 *Kodlar ro‘yxati:*\n\n"
    for row in kodlar:
        code = row["code"]
        title = row["title"]
        text += f"`{code}` - *{title}*\n"

    await message.answer(text, parse_mode="Markdown")

async def on_startup(_):
    await init_db()

async def on_shutdown(_):
    await close_db()

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
