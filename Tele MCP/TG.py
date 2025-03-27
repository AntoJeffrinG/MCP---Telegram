import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import logging

# Bot Token (Replace with your own)
TOKEN = "8124218696:AAGQBq1KzgcqC63bJodz9JMDLu_9TFjbzQA"

# Initialize bot & dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Logging
logging.basicConfig(level=logging.INFO)

# Admin ID (Replace with your own Telegram ID)
ADMIN_ID = "2034271211"

# Locations Dictionary
locations = {
    "Sathyabama University": (12.87049, 80.21983),
    "Current loc": (12.87103, 80.21700),
    "St. Joseph's": (13.0109, 80.2331),
    "Bengaluru": (12.9716, 77.5946),
    "Mumbai": (19.0760, 72.8777)
}

# Track the selected location
selected_location = None

# Keyboards
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Switch to Admin Panel")],
        [KeyboardButton(text="Share Location", request_location=True)]
    ], resize_keyboard=True
)

admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Choose Location")],
        [KeyboardButton(text="Exit Admin Panel")]
    ], resize_keyboard=True
)

# Admin Location Selection Keyboard (Includes Exit Button)
def location_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=label)] for label in locations.keys()] + [[KeyboardButton(text="Exit Admin Panel")]],
        resize_keyboard=True
    )

# Start Command
@dp.message(lambda message: message.text == "/start")
async def start(message: types.Message):
    await message.answer("Welcome! Select an option:", reply_markup=main_kb)

# Admin Authentication
@dp.message(lambda message: message.text == "Switch to Admin Panel")
async def admin_login(message: types.Message):
    if str(message.from_user.id) == ADMIN_ID:
        await message.answer("✅ Admin access granted!", reply_markup=admin_kb)
    else:
        await message.answer("❌ You are not authorized!")

# Exit Admin Panel (Works at Any Point)
@dp.message(lambda message: message.text == "Exit Admin Panel")
async def exit_admin(message: types.Message):
    await message.answer("Exited Admin Panel.", reply_markup=main_kb)

# Choose Location (Admin)
@dp.message(lambda message: message.text == "Choose Location")
async def choose_location(message: types.Message):
    if str(message.from_user.id) != ADMIN_ID:
        await message.answer("❌ You are not authorized!")
        return
    await message.answer("Select a location:", reply_markup=location_kb())

# Handle Location Selection & Update Selected Location
@dp.message(lambda message: message.text in locations.keys())
async def location_selected(message: types.Message):
    global selected_location
    selected_location = message.text
    await message.answer(f"✅ Access location updated to: {selected_location}\n\nYou can exit the admin panel anytime.", reply_markup=admin_kb)

# Handle User Location & Verify Based on Selected Location
@dp.message(lambda message: message.location is not None)
async def verify_location(message: types.Message):
    global selected_location

    if not selected_location:
        await message.answer("⚠️ No location has been set! Please wait for the admin to select a location.")
        return

    user_lat, user_lon = message.location.latitude, message.location.longitude
    target_lat, target_lon = locations[selected_location]

    if abs(user_lat - target_lat) < 0.1 and abs(user_lon - target_lon) < 0.1:  # Approximate match
        await message.answer(f"✅ You are in {selected_location}. Access granted!")
    else:
        await message.answer("❌ Access denied! You are not in the authorized location.")

# Run Bot
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
