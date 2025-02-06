import os
import yaml
import random
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from datetime import datetime, timedelta

from post_creating import generate_post

CONFIG_FILE = "config.yaml"

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


def load_channels_and_themes():
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return data

def save_channels_and_themes(data):
    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        yaml.safe_dump(data, file, allow_unicode=True)

async def post_to_channel(channel_id, theme):
    post_content = await generate_post(theme)
    await bot.send_message(chat_id=channel_id, text=post_content)

async def schedule_posts():
    now = datetime.now()
    start_time = now.replace(hour=8, minute=0, second=0, microsecond=0)
    end_time = now.replace(hour=23, minute=0, second=0, microsecond=0)

    if now < start_time:
        await asyncio.sleep((start_time - now).total_seconds())

    while True:
        current_time = datetime.now()
        if current_time > end_time:
            next_start_time = (current_time + timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)
            await asyncio.sleep((next_start_time - current_time).total_seconds())
        else:
            channels_and_themes = load_channels_and_themes()
            if not channels_and_themes:
                await bot.send_message(chat_id=OWNER_ID, text="Темы для постов закончились. Пожалуйста, добавьте новые темы.")
                await asyncio.sleep(60 * 60)
                continue

            for channel_id, themes in list(channels_and_themes.items()):
                if themes:
                    theme = random.choice(themes)
                    await post_to_channel(channel_id, theme)
                    themes.remove(theme)
            save_channels_and_themes(channels_and_themes)

            wait_time = random.uniform(3 * 60 * 60, 5.55 * 60 * 60)
            await asyncio.sleep(wait_time)

async def main():
    print("Бот запущен и готов к работе!")
    asyncio.create_task(schedule_posts())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())