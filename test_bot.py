import os
from dotenv import load_dotenv
from aiogram import Bot
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)