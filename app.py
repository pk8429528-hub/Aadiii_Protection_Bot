import os
import threading
import time
from flask import Flask
from bot import PikachuProtectionBot
from datetime import datetime
import sys

# Color codes for terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

app = Flask(__name__)

# Premium styled print function with colors
def premium_print(message, symbol="⚡", color=Colors.CYAN):
    """Premium styled print message with colors and animations"""
    border = "═" * 60
    timestamp = datetime.now().strftime("%H:%M:%S")
    styled_msg = f"""
{Colors.BOLD}{color}╔{border}╗{Colors.END}
{Colors.BOLD}{color}║  {symbol} [{timestamp}] {message}{Colors.END}
{Colors.BOLD}{color}╚{border}╝{Colors.END}
"""
    print(styled_msg)

# Loading animation
def loading_animation(text, duration=2):
    """Display loading animation"""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    
    i = 0
    while time.time() < end_time:
        frame = frames[i % len(frames)]
        sys.stdout.write(f"\r{Colors.CYAN}{frame} {text}...{Colors.END}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write("\r" + " " * 50 + "\r")
    sys.stdout.flush()

@app.route('/')
def index():
    return """🤖 Pikachu Protection Bot is running!
    
    ⚡ Status: Online
    💎 Version: 2.0.0
    👑 Owner: Crazy Boy
    """

@app.route('/health')
def health():
    return "OK"

@app.route('/status')
def status():
    return {
        "status": "online",
        "bot": "Pikachu Protection",
        "version": "2.0.0",
        "owner": "Crazy Boy"
    }

def run_bot():
    """Starts the Telegram bot in a separate thread"""
    premium_print("🚀 ɪɴɪᴛɪᴀʟɪᴢɪɴɢ ᴘɪᴋᴀᴄʜᴜ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ ʙᴏᴛ...", "⚡", Colors.GREEN)
    loading_animation("ʟᴏᴀᴅɪɴɢ ᴍᴏᴅᴜʟᴇs", 2)
    
    premium_print("📦 ᴍᴏᴅᴜʟᴇs ʟᴏᴀᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!", "✅", Colors.GREEN)
    premium_print("🔗 ᴄᴏɴɴᴇᴄᴛɪɴɢ ᴛᴏ ᴅᴀᴛᴀʙᴀsᴇ...", "🍃", Colors.BLUE)
    loading_animation("ᴇsᴛᴀʙʟɪsʜɪɴɢ ᴄᴏɴɴᴇᴄᴛɪᴏɴ", 1.5)
    
    premium_print("✅ ᴅᴀᴛᴀʙᴀsᴇ ᴄᴏɴɴᴇᴄᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!", "✅", Colors.GREEN)
    premium_print("🌟 ʙᴏᴛ ɪs ɴᴏᴡ ᴏɴʟɪɴᴇ!", "🌟", Colors.YELLOW)
    premium_print(f"🤖 ʙᴏᴛ ɴᴀᴍᴇ: ᴘɪᴋᴀᴄʜᴜ ✗ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ", "💎", Colors.CYAN)
    premium_print(f"👑 ᴏᴡɴᴇʀ: ⏤͟͞ 𝐂𝐑𝐀𝐙𝐘 𝐁𝐎𝐘 ᭄࿐", "👑", Colors.RED)
    premium_print("📢 ᴊᴏɪɴ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ: @CrazyyCore", "💬", Colors.BLUE)
    
    bot = PikachuProtectionBot()
    bot.run()

if __name__ == "__main__":
    # Show startup banner
    print(f"""
{Colors.BOLD}{Colors.CYAN}╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║     ⚡⚡⚡ ᴘɪᴋᴀᴄʜᴜ ✗ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ ʙᴏᴛ ⚡⚡⚡                 ║
║     💎💎💎 ᴅᴇᴘʟᴏʏɪɴɢ ᴏɴ ʀᴇɴᴅᴇʀ 💎💎💎                       ║
║     🚀🚀🚀 ᴘʀᴇᴍɪᴜᴍ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ ᴀᴄᴛɪᴠᴀᴛᴇᴅ 🚀🚀🚀              ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝{Colors.END}
    """)
    
    # Run the bot in a background thread
    premium_print("🔄 sᴛᴀʀᴛɪɴɢ ʙᴏᴛ ᴛʜʀᴇᴀᴅ...", "🔄", Colors.YELLOW)
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Start the Flask server to keep Render happy
    port = int(os.environ.get("PORT", 10000))
    premium_print(f"🌐 sᴛᴀʀᴛɪɴɢ ғʟᴀsᴋ sᴇʀᴠᴇʀ ᴏɴ ᴘᴏʀᴛ {port}...", "🌐", Colors.CYAN)
    
    time.sleep(0.5)
    premium_print("✅ sᴇʀᴠᴇʀ ɪs ʀᴜɴɴɪɴɢ!", "✅", Colors.GREEN)
    
    print(f"""
{Colors.BOLD}{Colors.GREEN}╔════════════════════════════════════════════════════════════════╗
║                                                                
║  🎯 ᴘɪᴋᴀᴄʜᴜ ɪs ʀᴇᴀᴅʏ ᴛᴏ ᴘʀᴏᴛᴇᴄᴛ ʏᴏᴜʀ ɢʀᴏᴜᴘ!             
║  🤖 ʙᴏᴛ: @Pikachu_Protection_Robot                           
║  👑 ᴏᴡɴᴇʀ: @CrazyyCore                                       
║  📢 ɢʀᴏᴜᴘ: https://t.me/+Fgx6_JRTLkFjMjE1                    
║                                                                
╚════════════════════════════════════════════════════════════════╝{Colors.END}
    """)
    
    premium_print("⚡ ᴘɪᴋᴀᴄʜᴜ ɪs ʀᴇᴀᴅʏ ᴛᴏ ᴘʀᴏᴛᴇᴄᴛ!", "⚡", Colors.YELLOW)
    
    app.run(host="0.0.0.0", port=port)
