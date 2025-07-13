# ruby-worker-bot/handlers.py
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from telegram.constants import ParseMode
import logging

from config import FILE_DATA, DELETE_DELAY
from database import verify_and_delete_token

logger = logging.getLogger(__name__)

async def send_file(user_id: int, file_key: str, context: ContextTypes.DEFAULT_TYPE):
    """फाइल भेजता है और डिलीट का काम शेड्यूल करता है।"""
    if file_key in FILE_DATA:
        file_info = FILE_DATA[file_key]
        caption = file_info.get("caption", "")
        file_id = file_info.get("id")
        
        try:
            video_message = await context.bot.send_video(chat_id=user_id, video=file_id, caption=caption, parse_mode=ParseMode.HTML)
            await context.bot.send_message(chat_id=user_id, text="This media message will be deleted after 15 minutes.")
            
            # ऑटो-डिलीट का लॉजिक यहाँ जोड़ना होगा (Phase 2 में)
            logger.info(f"Sent file '{file_key}' to user {user_id}")
        except Exception as e:
            logger.error(f"Error sending file {file_key}: {e}")
            await context.bot.send_message(chat_id=user_id, text="Sorry, an error occurred.")
    else:
        await context.bot.send_message(chat_id=user_id, text="File not found in config.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not context.args:
        await update.message.reply_text("I am a worker bot. Please get a link from the main bot.")
        return

    secure_token = context.args[0]
    file_key = verify_and_delete_token(secure_token, user.id)
    
    if file_key:
        await send_file(user.id, file_key, context)
    else:
        await update.message.reply_text("This link is invalid, expired, or not for you. Please get a new link.")

def setup_handlers(application):
    application.add_handler(CommandHandler("start", start))