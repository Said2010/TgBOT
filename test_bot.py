import os
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import Message 

load_dotenv()

TOKEN = os.getenv("BTOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

VOICES_DIR = "zvoices"
VIDEOS_DIR = "zvideo_notes"
TEXTS_DIR = "ztexts"

os.makedirs(VOICES_DIR, exist_ok=True)
os.makedirs(VIDEOS_DIR, exist_ok=True)
os.makedirs(TEXTS_DIR, exist_ok=True)


@dp.message()
async def echp(message: Message):
    time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    user_id = message.from_user.id
    text_content = message.text or message.caption

    try:
        if text_content and not message.voice and not message.video_note:
            file_name = f"text_{time_str}_{user_id}.txt"
            file_path = os.path.join(TEXTS_DIR, file_name)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text_content)
                
            print(f"✅ Saved text: {file_path}")

        elif message.voice:
            file_name = f"voice_{time_str}_{user_id}.ogg"
            file_path = os.path.join(VOICES_DIR, file_name)
            
            file_info = await bot.get_file(message.voice.file_id)
            await bot.download_file(file_info.file_path, file_path)
            print(f"✅ Saved voice: {file_path}")

        elif message.video_note:
            file_name = f"video_{time_str}_{user_id}.mp4"
            file_path = os.path.join(VIDEOS_DIR, file_name)
            
            file_info = await bot.get_file(message.video_note.file_id)
            await bot.download_file(file_info.file_path, file_path)
            print(f"✅ Saved video note: {file_path}")

    except Exception as e:
        print(f"❌ Error: {e}")

    # Возвращаем повтор сообщений в чат
    await message.send_copy(chat_id=message.from_user.id)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
