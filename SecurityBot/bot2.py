from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext

# Replace this with your actual bot token from BotFather
TOKEN = "8081022784:AAEFOH7KMxCQJOik0oMr95vUqEs2oUWC8Gw"

# Define fake news dictionary
fake_news_samples = {
    "earth will be hit by an asteroid next week": "Fake News",
    "drinking coffee increases lifespan by 50 years": "Fake News"
}

# Define response logic
async def check_fake_news(update: Update, context: CallbackContext):
    text = update.message.text.lower()

    if text in fake_news_samples:
        response = fake_news_samples[text]
        await update.message.reply_text(response)

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! Send me a news headline to check if it's fake.")

def main():
    app = Application.builder().token(TOKEN).build()

    # Only respond if the exact message matches one of the fake news samples
    pattern = "|".join(fake_news_samples.keys())  # Create regex pattern from dictionary keys
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(f"^{pattern}$"), check_fake_news))

    print("✅ The bot is running...")  # Message when bot starts

    app.run_polling()

if __name__ == "__main__":
    main()
