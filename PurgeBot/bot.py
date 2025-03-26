import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from toxicity_detector import is_toxic  
from img_detection import is_abusive_image 
from config import TOKEN


logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

user_strikes = {}
MAX_STRIKES = 3

async def warn_or_ban(update: Update, context: CallbackContext, is_image=False, is_video=False) -> None:
    """Warns or bans a user based on offenses."""
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    user = update.message.from_user
    username = user.username if user.username else user.first_name if user.first_name else "UnknownUser"


    user_strikes[user_id] = user_strikes.get(user_id, 0) + 1


    await update.message.delete()


    warning_message = ""
    if user_strikes[user_id] == 1:
        warning_message = f"⚠️ Warning, @{username}! Your {'video' if is_video else 'image' if is_image else 'message'} contained inappropriate content."
    elif user_strikes[user_id] == 2:
        warning_message = f"🚨 Final warning, @{username}! One more offense and you'll be banned."
    elif user_strikes[user_id] >= MAX_STRIKES:
        await context.bot.ban_chat_member(chat_id, user_id)
        warning_message = f"🚫 User @{username} has been banned for repeated violations."
        del user_strikes[user_id] 

    if warning_message:
        await context.bot.send_message(chat_id=chat_id, text=warning_message)

async def message_handler(update: Update, context: CallbackContext) -> None:
    """Checks text messages for toxicity."""
    text = update.message.text
    if is_toxic(text):
        await warn_or_ban(update, context)

async def image_handler(update: Update, context: CallbackContext) -> None:
    """Checks images for abusive content."""
    photo = update.message.photo[-1] 
    file = await context.bot.get_file(photo.file_id)
    file_path = "temp.jpg"
    
    await file.download_to_drive(file_path)

    if is_abusive_image(file_path):
        await warn_or_ban(update, context, is_image=True)

async def start(update: Update, context: CallbackContext) -> None:
    """Handles the /start command."""
    await update.message.reply_text("🤖 Hello! I am an AI-powered moderation bot. I monitor messages, images, and videos for inappropriate content.")

def main():
    """Run the bot using Application (for v20+)."""
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    app.add_handler(MessageHandler(filters.PHOTO, image_handler))
    app.add_handler(MessageHandler(filters.VIDEO, video_handler))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
