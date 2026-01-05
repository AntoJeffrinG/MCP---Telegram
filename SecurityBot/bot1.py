
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext

# Replace this with your actual bot token from BotFather
TOKEN = "BotTOkenHere"

# Define response logic
async def check_url(update: Update, context: CallbackContext):
    text = update.message.text.lower().strip()

    if text == "https://www.google.co.in":
        response = "Safe"
    elif text == "https://paypal.com.verify-account.xyz/login":
        response = "Not Safe"
    else:
        return  # Ignore other messages

    await update.message.reply_text(response)

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! Send me a URL to check.")

def main():
    app = Application.builder().token(TOKEN).build()

    # Corrected regex with raw string
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^https://www\.google\.co\.in$|^https://paypal\.com\.verify-account\.xyz/login$"), check_url))

    print("✅ The bot is running...")  # Message when bot starts

    app.run_polling()

if __name__ == "__main__":
    main()
