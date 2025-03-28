import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode, ChatType
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties

TOKEN = "7275579353:AAER7dkooGN63a6FsNKU9_M7slknkf5ol78"

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

secret_messages = {}

@dp.message(Command("start"))
async def start_command(message: Message):
    if message.chat.type == ChatType.PRIVATE:
        await message.answer("👋 Welcome! Use /send_secret to store a secret message.")
    else:
        await message.answer("🤖 Hello Group! Use /send_secret and keywords to trigger messages.")

@dp.message(Command("send_secret"))
async def send_secret_command(message: Message):
    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        await message.answer("⚠️ Usage: /send_secret [keyword] [message]")
        return

    keyword, secret_msg = args[1], args[2]
    chat_id = message.chat.id

    if chat_id not in secret_messages:
        secret_messages[chat_id] = {}

    secret_messages[chat_id][keyword] = secret_msg

    await bot.send_message(message.from_user.id, f"✅ Your secret message has been saved with the keyword: {keyword}.")

    try:
        await message.delete()
    except Exception:
        pass

@dp.message()
async def detect_keywords(message: Message):
    chat_id = message.chat.id
    text = message.text.lower()

    if chat_id in secret_messages:
        for keyword, secret_msg in secret_messages[chat_id].items():
            if keyword in text:
                await message.answer(secret_msg)
                break

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
