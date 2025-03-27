import logging
import aiohttp
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from transformers import pipeline

# Replace with your VirusTotal API Key
API_KEY = "294d0056ec536a7e173b5d341300bb39c454d70706179c0d75cfaef8256b08f7"
BASE_URL = "https://www.virustotal.com/api/v3/urls/"

# Load Fake News Detection Model
fake_news_detector = pipeline("text-classification", model="jy46604790/Fake-News-Bert-Detect")

# Confidence threshold for fake news detection
FAKE_NEWS_THRESHOLD = 0.7  # Messages with confidence below this are flagged as fake

# Function to encode URL for VirusTotal
def encode_url(url):
    import base64
    return base64.urlsafe_b64encode(url.encode()).decode().strip("=")

# Function to check if a URL is safe asynchronously
async def check_url(url):
    """Check the URL using VirusTotal API."""
    url_id = encode_url(url)
    headers = {"x-apikey": API_KEY}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL + url_id, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                malicious = any(engine['category'] == 'malicious' for engine in data['data']['attributes']['last_analysis_results'].values())

                return f"🚨 URL {url} is flagged as malicious!" if malicious else f"✅ URL {url} is safe."
            else:
                return f"Error: {response.status}, Unable to scan the URL."

async def start(update: Update, context: CallbackContext):
    """Start command response."""
    await update.message.reply_text("🤖 Hello! Send a message, and I'll check for fake news or phishing links.")

def contains_url(text):
    """Check if the message contains a URL."""
    return bool(re.search(r'(https?://[^\s]+|www\.[^\s]+)', text))

async def check_message(update: Update, context: CallbackContext):
    """Handle messages containing URLs or check for fake news."""
    text = update.message.text

    if contains_url(text):
        urls = re.findall(r'(https?://[^\s]+|www\.[^\s]+)', text)
        for url in urls:
            response_message = await check_url(url)
            await update.message.reply_text(response_message)
    else:
        # Check for Fake News
        prediction = fake_news_detector(text)[0]
        label = prediction['label']
        score = prediction['score']

        # Only warn if confidence is below the threshold
        if label == "FAKE" and score < FAKE_NEWS_THRESHOLD:
            await update.message.reply_text(f"⚠️ This message **may be fake news**! (Confidence: {score:.2f})")

def main():
    """Main function to start the bot."""
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

    # Your bot's API token
    TOKEN = "7610781631:AAEcq8UXmGxmQJPNEWYz8gih9V4cSmclcgE"
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_message))

    app.run_polling()

if __name__ == "__main__":
    main()
