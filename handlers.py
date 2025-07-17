# ruby-worker-bot/handlers.py
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from telegram.constants import ParseMode
import logging
from config import FILE_DATA
from database import verify_and_delete_token

logger = logging.getLogger(__name__)

async def send_file(user_id, file_key, context):
    if file_key in FILE_DATA:
        file_info = FILE_DATA[file_key]
        try:
            await context.bot.send_video(chat_id=user_id, video=file_info["id"], caption=file_info["caption"], parse_mode=ParseMode.HTML)
            await context.bot.send_message(chat_id=user_id, text="This media will be deleted after 15 minutes.")
        except Exception as e: logger.error(f"Error sending file {file_key}: {e}")
    else: await context.bot.send_message(chat_id=user_id, text="File not found.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not context.args: await update.message.reply_text("I am a worker bot. Get a link from the main bot."); return
    token = context.args[0]
    file_key = verify_and_delete_token(token, user.id)
    if file_key: await send_file(user.id, file_key, context)
    else: await update.message.reply_text("Link is invalid or expired.")

def setup_handlers(application):
    application.add_handler(CommandHandler("start", start))
