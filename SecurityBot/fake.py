import os
import requests
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TELEGRAM_BOT_TOKEN = "8081022784:AAEFOH7KMxCQJOik0oMr95vUqEs2oUWC8Gw"
RAPIDAPI_KEY = "fa49d03b99mshb9b1176d92d30dfp1e013ajsn276dc79afd9b"

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

FAKE_NEWS_API_URL = "https://fake-news-detection1.p.rapidapi.com/api/v1"

def check_fake_news(text):
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "fake-news-detection1.p.rapidapi.com"
    }
    payload = {"text": text}
    
    try:
        response = requests.post(FAKE_NEWS_API_URL, json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result.get("prediction", "Unknown")
        else:
            return "Error"
    except Exception as e:
        logging.error(f"API Error: {e}")
        return "Error"

@dp.message_handler(content_types=types.ContentType.TEXT)
async def monitor_messages(message: types.Message):
    text = message.text
    result = check_fake_news(text)
    
    if result == "Fake":
        await message.reply("⚠️ This message is flagged as potentially fake news!")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
