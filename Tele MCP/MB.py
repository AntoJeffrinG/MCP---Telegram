import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties

# ✅ Replace with your actual bot token and admin ID
BOT_TOKEN = "8101041284:AAFrV9x1PvCA4m6iepBk4iLACj-ZJcsPhVM"
ADMIN_ID = 2034271211  # Replace with your actual Telegram ID

# ✅ Initialize Bot and Dispatcher
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# ✅ Security Questions for User Verification
security_questions = {
    "What is 2 + 2?": "4",
    "What is the capital of France?": "Paris",
    "Which planet is known as the Red Planet?": "Mars"
}

user_reputation = {}

# ✅ Keyboards
main_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Request Chat Access")]],
    resize_keyboard=True
)

admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="View Users"), KeyboardButton(text="Ban User")],
        [KeyboardButton(text="Unban User"), KeyboardButton(text="Exit Admin Panel")]
    ],
    resize_keyboard=True
)

# ✅ /start Command Handler
@dp.message(Command("start"))
async def start_command(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Request Chat Access", callback_data="request_access")]
        ]
    )
    await message.answer("Welcome! Click the button below to request access.", reply_markup=keyboard)

# ✅ Handle User Access Request
@dp.callback_query(lambda c: c.data == "request_access")
async def request_access(callback: CallbackQuery):
    question = list(security_questions.keys())[0]
    user_reputation[callback.from_user.id] = {"question": question, "attempts": 0}
    await callback.message.answer(f"🛡 Security Question:\n<b>{question}</b>", reply_markup=ReplyKeyboardRemove())
    await callback.answer()

# ✅ Handle User Responses to Security Questions
@dp.message()
async def validate_answer(message: Message):
    user_id = message.from_user.id
    if user_id in user_reputation and "question" in user_reputation[user_id]:
        question = user_reputation[user_id]["question"]
        correct_answer = security_questions[question]

        if message.text.strip().lower() == correct_answer.lower():
            await message.answer("✅ Correct! You are now allowed to chat.", reply_markup=main_kb)
            del user_reputation[user_id]
        else:
            user_reputation[user_id]["attempts"] += 1
            if user_reputation[user_id]["attempts"] >= 3:
                await message.answer("❌ Too many incorrect attempts. You are banned.")
                await bot.ban_chat_member(chat_id=message.chat.id, user_id=user_id)
            else:
                await message.answer("❌ Incorrect. Try again.")

# ✅ Admin Panel Access
@dp.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("🔧 Welcome to the Admin Panel!", reply_markup=admin_kb)
    else:
        await message.answer("❌ You are not authorized to access this panel.")

# ✅ Admin Commands
@dp.message(lambda message: message.text == "View Users")
async def view_users(message: Message):
    if message.from_user.id == ADMIN_ID:
        user_list = "\n".join([str(uid) for uid in user_reputation.keys()]) or "No active users."
        await message.answer(f"📋 Active Users:\n{user_list}")

@dp.message(lambda message: message.text == "Ban User")
async def ban_user(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("Send the User ID to ban.")

        @dp.message()
        async def ban_selected_user(msg: Message):
            try:
                user_id = int(msg.text)
                await bot.ban_chat_member(chat_id=msg.chat.id, user_id=user_id)
                await msg.answer(f"🚫 User {user_id} has been banned.")
            except ValueError:
                await msg.answer("❌ Invalid ID. Try again.")

@dp.message(lambda message: message.text == "Unban User")
async def unban_user(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("Send the User ID to unban.")

        @dp.message()
        async def unban_selected_user(msg: Message):
            try:
                user_id = int(msg.text)
                await bot.unban_chat_member(chat_id=msg.chat.id, user_id=user_id)
                await msg.answer(f"✅ User {user_id} has been unbanned.")
            except ValueError:
                await msg.answer("❌ Invalid ID. Try again.")

@dp.message(lambda message: message.text == "Exit Admin Panel")
async def exit_admin_panel(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("🔙 Exited Admin Panel.", reply_markup=main_kb)

# ✅ Run the Bot
async def main():
    print("🤖 Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
