import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Predefined spam messages dictionary
spam_samples = {
    "win a free iphone now!": "Spam",
    "you have been selected for a lottery! claim now": "Spam",
    "click this link to get a special discount!": "Spam",
    "earn $1000 per day from home": "Spam"
}

def is_spam(text):
    """Check if a message is spam based on predefined samples."""
    return text.lower() in spam_samples

async def warn_user(update: Update, context: CallbackContext):
    """Warn users and remove messages if they send spam."""
    if update.message:
        user = update.message.from_user
        chat_id = update.message.chat_id
        message_id = update.message.message_id
        text = update.message.text

        logging.info(f"📩 New message from @{user.username}: {text}")

        if is_spam(text):
            logging.info(f"🚨 Spam detected from @{user.username}, attempting to delete...")

            try:
                await context.bot.delete_message(chat_id, message_id)
                await context.bot.send_message(
                    chat_id, f"⚠️ @{user.username}, your message was flagged as spam and removed!"
                )
            except Exception as e:
                logging.error(f"❌ Failed to delete message: {e}")
        else:
            logging.info(f"✅ Message from @{user.username} is clean.")

async def start(update: Update, context: CallbackContext):
    """Start command response."""
    logging.info("✅ Start command received")
    await update.message.reply_text("Hello! I'm a spam detection bot. I'll remove spam messages and warn users.")

def main():
    """Main function to start the bot."""
    TOKEN = "7738885490:AAHcfaS4I404PYaNPRh_4GNUdry-Fx9q8xs"  # Replace with your bot token
    app = Application.builder().token(TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, warn_user))

    logging.info("🚀 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
