# ruby-worker-bot/main.py
import os, logging
from threading import Thread
from flask import Flask
from telegram.ext import Application
from dotenv import load_dotenv
from handlers import setup_handlers

load_dotenv()
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
TOKEN = os.environ.get("WORKER_BOT_TOKEN") # <-- ध्यान दें: WORKER_BOT_TOKEN

app = Flask('')
@app.route('/')
def home(): return "Ruby Worker Bot is alive!"
def run_flask(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
def keep_alive(): Thread(target=run_flask).start()

def main():
    if not TOKEN: logger.critical("WORKER_BOT_TOKEN not set!"); return
    application = Application.builder().token(TOKEN).build()
    setup_handlers(application)
    keep_alive()
    logger.info("Ruby Worker Bot is polling!")
    application.run_polling()

# यह थ्रेड Gunicorn द्वारा चलाए जाने पर बॉट को शुरू करेगा
bot_thread = Thread(target=main)
bot_thread.start()

# लोकल टेस्टिंग के लिए, अगर आप सीधे python main.py चलाते हैं
if __name__ == '__main__':
    # Gunicorn इस हिस्से को नज़रअंदाज़ कर देगा
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
