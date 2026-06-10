import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import Message 
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message()
async def echp(message):
    await message.send_copy(chat_id=message.from_user.id)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        import asyncio
        asyncio.run(main())
    except KeyboardInterrupt:
        pass