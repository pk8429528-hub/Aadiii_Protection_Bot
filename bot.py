#!/usr/bin/env python3
"""
ᴘɪᴋᴀᴄʜᴜ ✗ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ ʙᴏᴛ - ᴘʀᴇᴍɪᴜᴍ ɢʀᴏᴜᴘ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ ʙᴏᴛ
"""

import os
import sys
import asyncio
import logging
from datetime import datetime
from flask import Flask
import threading

# ────═◈═─ FIX FOR PTB VERSION COMPATIBILITY ─═◈═────
import telegram.ext._updater
if not hasattr(telegram.ext._updater.Updater, '_Updater__polling_cleanup_cb'):
    # Monkey patch the missing attribute
    class PatchedUpdater(telegram.ext.Updater):
        pass
    telegram.ext.Updater = PatchedUpdater
# ──────────────────────────────────────────────────

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)

from config import Config
from database import Database

# ────═◈═─ FLASK WEB SERVER FOR RENDER ─═◈═────
app = Flask(__name__)

@app.route('/')
def home():
    return "⚡ Pikachu Protection Bot is running!"

@app.route('/health')
def health():
    return "OK", 200

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False)

threading.Thread(target=run_web, daemon=True).start()
print("🌐 Web server started for Render port binding")
# ──────────────────────────────────────────────────

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize database
db = Database()

# Custom print with premium style
def premium_print(message, symbol="⚡"):
    """Premium styled print message"""
    border = "═" * 50
    timestamp = datetime.now().strftime("%H:%M:%S")
    styled_msg = f"""
╔{border}╗
║  {symbol} [{timestamp}] {message}
╚{border}╝
"""
    print(styled_msg)

class PikachuProtectionBot:
    def __init__(self):
        self.app = None
        
        # Premium startup message
        premium_print(f"ʙᴏᴛ ɪɴɪᴛɪᴀʟɪᴢɪɴɢ: {Config.BOT_NAME}", "🚀")
        premium_print(f"ᴏᴡɴᴇʀ: {Config.OWNER_NAME}", "👑")
        premium_print(f"ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇs: ʟᴏᴀᴅᴇᴅ", "💎")
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        await db.add_user(user.id, user.username, user.first_name)
        
        is_premium = user.id in Config.PREMIUM_USERS or user.id in Config.OWNER_ID
        
        welcome_text = f"""
╔═══════════════════════════════════════╗
║     ⚡ ᴘɪᴋᴀᴄʜᴜ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ ʙᴏᴛ ⚡     ║
╚═══════════════════════════════════════╝

────═◈═─ ✧◈✧ ─═◈═────
  🤖 ɴᴀᴍᴇ: {Config.BOT_NAME}  
  📌 ɪᴅ: {Config.BOT_USERNAME} 
  👑 ᴏᴡɴᴇʀ: {Config.OWNER_NAME} 
  📞 ᴄᴏɴᴛᴀᴄᴛ: {Config.OWNER_USERNAME} 
────═◈═─ ✧◈✧ ─═◈═────

✨ **ᴡᴇʟᴄᴏᴍᴇ {user.first_name}!** ✨

ɪ ᴀᴍ ᴀ ᴘᴏᴡᴇʀғᴜʟ ɢʀᴏᴜᴘ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ ʙᴏᴛ 
ᴡɪᴛʜ ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇs ᴀɴᴅ ᴀᴅᴠᴀɴᴄᴇᴅ ᴍᴏᴅᴇʀᴀᴛɪᴏɴ.

💎 **ᴘʀᴇᴍɪᴜᴍ sᴛᴀᴛᴜs:** {'✅ ᴀᴄᴛɪᴠᴇ' if is_premium else '❌ ɪɴᴀᴄᴛɪᴠᴇ'}

📌 **ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴍᴀᴋᴇ ᴍᴇ ᴀᴅᴍɪɴ!**

ᴜsᴇ /help ᴛᴏ sᴇᴇ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs.
"""
        await update.message.reply_text(
            welcome_text,
            parse_mode="Markdown"
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = f"""
📖 **ᴄᴏᴍᴍᴀɴᴅ ʟɪsᴛ** 📖

╔═══════════════════════════╗

**👑 ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs:**

╰┈➤ /warn @username - ᴡᴀʀɴ ᴜsᴇʀ  
╰┈➤ /warns @username - ᴄʜᴇᴄᴋ ᴡᴀʀɴs  
╰┈➤ /resetwarns @username - ʀᴇsᴇᴛ ᴡᴀʀɴs  
╰┈➤ /mute @username - ᴍᴜᴛᴇ ᴜsᴇʀ  
╰┈➤ /unmute @username - ᴜɴᴍᴜᴛᴇ ᴜsᴇʀ  
╰┈➤ /kick @username - ᴋɪᴄᴋ ᴜsᴇʀ  
╰┈➤ /ban @username - ʙᴀɴ ᴜsᴇʀ  
╰┈➤ /unban @username - ᴜɴʙᴀɴ ᴜsᴇʀ  

**📊 ɢᴇɴᴇʀᴀʟ ᴄᴏᴍᴍᴀɴᴅs:**

╰┈➤ /start - sᴛᴀʀᴛ ʙᴏᴛ  
╰┈➤ /help - ɢᴇᴛ ʜᴇʟᴘ  
╰┈➤ /about - ᴀʙᴏᴜᴛ ʙᴏᴛ  

**💎 ᴘʀᴇᴍɪᴜᴍ ᴄᴏᴍᴍᴀɴᴅs:**

╰┈➤ /premium - ᴄʜᴇᴄᴋ ᴘʀᴇᴍɪᴜᴍ  

╚═══════════════════════════╝

🔥 ᴘᴏᴡᴇʀᴇᴅ ʙʏ {Config.BOT_NAME}
"""
        await update.message.reply_text(
            help_text,
            parse_mode="Markdown"
        )
    
    async def about_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /about command"""
        about_text = f"""
⚡ **ᴀʙᴏᴜᴛ {Config.BOT_NAME}** ⚡

────═◈═─ ✧◈✧ ─═◈═────
  🤖 ɴᴀᴍᴇ: {Config.BOT_NAME}  
  📌 ɪᴅ: {Config.BOT_USERNAME} 
  👑 ᴏᴡɴᴇʀ: {Config.OWNER_NAME} 
  📞 ᴄᴏɴᴛᴀᴄᴛ: {Config.OWNER_USERNAME} 
────═◈═─ ✧◈✧ ─═◈═────
✦•·································•✦

💫 **ᴅᴇsᴄʀɪᴘᴛɪᴏɴ:**
ᴀ ᴘᴏᴡᴇʀғᴜʟ ɢʀᴏᴜᴘ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ ʙᴏᴛ ᴡɪᴛʜ 
ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇs ᴀɴᴅ ᴀᴅᴠᴀɴᴄᴇᴅ ᴍᴏᴅᴇʀᴀᴛɪᴏɴ.

⚙️ **ғᴇᴀᴛᴜʀᴇs:**
╰┈➤ ᴀɴᴛɪ-sᴘᴀᴍ
╰┈➤ ᴀɴᴛɪ-ʟɪɴᴋ
╰┈➤ ᴡᴀʀɴ sʏsᴛᴇᴍ
╰┈➤ ᴍᴜᴛᴇ/ᴜɴᴍᴜᴛᴇ
╰┈➤ ʙᴀɴ/ᴋɪᴄᴋ
╰┈➤ ᴡᴇʟᴄᴏᴍᴇ/ɢᴏᴏᴅʙʏᴇ
╰┈➤ ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇs

📢 **ᴠᴇʀsɪᴏɴ:** 2.0.0
🔰 **sᴛᴀᴛᴜs:** ᴀᴄᴛɪᴠᴇ

✦•·································•✦
ᴘᴏᴡᴇʀᴇᴅ ʙʏ {Config.OWNER_NAME}
🙏 ᴊᴀʏ sʜʀᴇᴇ ʀᴀᴍ 🙏
"""
        await update.message.reply_text(
            about_text,
            parse_mode="Markdown"
        )
    
    async def premium_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /premium command"""
        user = update.effective_user
        is_premium = user.id in Config.PREMIUM_USERS or user.id in Config.OWNER_ID
        
        if is_premium:
            text = f"""
💎 **ᴘʀᴇᴍɪᴜᴍ sᴛᴀᴛᴜs** 💎

✅ **ʏᴏᴜ ᴀʀᴇ ᴀ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀ!**

**ᴜɴʟᴏᴄᴋᴇᴅ ғᴇᴀᴛᴜʀᴇs:**
╰┈➤ ᴀɴᴛɪ-ᴄʀᴀsʜ
╰┈➤ ᴀᴅᴠᴀɴᴄᴇᴅ ᴀɴᴛɪ-sᴘᴀᴍ
╰┈➤ ᴄᴜsᴛᴏᴍ ᴡᴇʟᴄᴏᴍᴇ ɢɪғ
╰┈➤ ᴘʀɪᴠᴀᴛᴇ ʟᴏɢs
╰┈➤ 24/7 sᴜᴘᴘᴏʀᴛ

✨ ᴛʜᴀɴᴋs ғᴏʀ ʙᴇɪɴɢ ᴘʀᴇᴍɪᴜᴍ!
"""
        else:
            text = f"""
💎 **ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ** 💎

**ᴜɴʟᴏᴄᴋ ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇs:**
╰┈➤ ᴀɴᴛɪ-ᴄʀᴀsʜ
╰┈➤ ᴀᴅᴠᴀɴᴄᴇᴅ ᴀɴᴛɪ-sᴘᴀᴍ
╰┈➤ ᴄᴜsᴛᴏᴍ ᴡᴇʟᴄᴏᴍᴇ ɢɪғ
╰┈➤ ᴘʀɪᴠᴀᴛᴇ ʟᴏɢs
╰┈➤ 24/7 sᴜᴘᴘᴏʀᴛ

**ᴘʀɪᴄᴇ:** $5/ᴍᴏɴᴛʜ

ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ ᴛᴏ ʙᴜʏ:
📞 {Config.OWNER_USERNAME}
"""
        await update.message.reply_text(
            text,
            parse_mode="Markdown"
        )
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Update {update} caused error {context.error}")
        
        try:
            if update and update.effective_chat:
                await context.bot.send_message(
                    update.effective_chat.id,
                    "❌ **ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ!**\n"
                    f"ᴇʀʀᴏʀ: `{str(context.error)[:100]}`",
                    parse_mode="Markdown"
                )
        except:
            pass
    
    def run(self):
        """Run the bot"""
        try:
            # Create application
            self.app = Application.builder().token(Config.BOT_TOKEN).build()
            
            # Add command handlers
            self.app.add_handler(CommandHandler("start", self.start))
            self.app.add_handler(CommandHandler("help", self.help_command))
            self.app.add_handler(CommandHandler("about", self.about_command))
            self.app.add_handler(CommandHandler("premium", self.premium_command))
            
            # Add error handler
            self.app.add_error_handler(self.error_handler)
            
            # Premium startup messages
            premium_print(f"ʙᴏᴛ {Config.BOT_NAME} ɪs ɴᴏᴡ ʀᴜɴɴɪɴɢ!", "⚡")
            premium_print(f"ᴏᴡɴᴇʀ: {Config.OWNER_NAME}", "👑")
            
            # Run the bot
            self.app.run_polling()
            
        except Exception as e:
            premium_print(f"ᴇʀʀᴏʀ: {str(e)}", "❌")
            sys.exit(1)

if __name__ == "__main__":
    # Check for required configurations
    if not Config.BOT_TOKEN:
        premium_print("ʙᴏᴛ ᴛᴏᴋᴇɴ ɴᴏᴛ ғᴏᴜɴᴅ! ᴘʟᴇᴀsᴇ sᴇᴛ ʙᴏᴛ_ᴛᴏᴋᴇɴ ɪɴ .ᴇɴᴠ ғɪʟᴇ", "❌")
        sys.exit(1)
    
    # Start the bot
    bot = PikachuProtectionBot()
    bot.run()
