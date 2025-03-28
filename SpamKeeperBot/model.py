import logging
from transformers import pipeline
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

spam_classifier = pipeline("text-classification", model="mrm8488/bert-tiny-finetuned-sms-spam-detection")

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

spam_samples = {
    "win a free iphone now!": "Spam",
    "you have been selected for a lottery! claim now": "Spam",
    "click this link to get a special discount!": "Spam",
    "earn $1000 per day from home": "Spam"
}

def is_spam(text):
    if text.lower() in spam_samples:
        return True
    
    prediction = spam_classifier(text)[0]
    score = prediction["score"]
    logging.info(f"🔍 Spam Check: '{text}' → Score: {score}")
    return score > 0.9

async def warn_user(update: Update, context: CallbackContext):
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
                await context.bot.send_message(chat_id, f"⚠️ @{user.username}, your message was flagged as spam and removed!")
            except Exception as e:
                logging.error(f"❌ Failed to delete message: {e}")
        else:
            logging.info(f"✅ Message from @{user.username} is clean.")

async def start(update: Update, context: CallbackContext):
    logging.info("✅ Start command received")
    await update.message.reply_text("Hello! I'm a spam detection bot. I'll remove spam messages and warn users.")

def main():
    TOKEN = "7738885490:AAHcfaS4I404PYaNPRh_4GNUdry-Fx9q8xs"
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, warn_user))
    logging.info("🚀 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
