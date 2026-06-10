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

# Создаем папки для сохранения файлов, если их еще нет
VOICES_DIR = "voices"
VIDEOS_DIR = "video_notes"
os.makedirs(VOICES_DIR, exist_ok=True)
os.makedirs(VIDEOS_DIR, exist_ok=True)


@dp.message()
async def echp(message: Message):
    # Генерация базовой части имени файла (дата_время_id)
    time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    user_id = message.from_user.id

    # 1. Обработка голосового сообщения
    if message.voice:
        file_name = f"voice_{time_str}_{user_id}.ogg"
        file_path = os.path.join(VOICES_DIR, file_name)
        
        file_info = await bot.get_file(message.voice.file_id)
        await bot.download_file(file_info.file_path, file_path)
        print(f"Голосовое сохранено: {file_path}")

    # 2. Обработка видеосообщения (кружка)
    elif message.video_note:
        file_name = f"video_{time_str}_{user_id}.mp4"
        file_path = os.path.join(VIDEOS_DIR, file_name)
        
        file_info = await bot.get_file(message.video_note.file_id)
        await bot.download_file(file_info.file_path, file_path)
        print(f"Видеосообщение сохранено: {file_path}")

    # Бот дублирует сообщение обратно в чат
    await message.send_copy(chat_id=message.from_user.id)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
