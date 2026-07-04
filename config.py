import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Bot Configuration
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    
    # MongoDB
    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("DB_NAME", "pikachu_protection")
    
    # Owner
    OWNER_ID = 7790607144
    OWNER_NAME = "⏤͟͞ 𝐂𝐑𝐀𝐙𝐘 𝐁𝐎𝐘 ᭄࿐"
    OWNER_USERNAME = "@CrazyyCore"
    
    # Bot Info
    BOT_NAME = "── ᴘɪᴋᴀᴄʜᴜ ✗ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ ──"
    BOT_USERNAME = "@Pikachu_Protection_Robot"
    
    # Premium Users
    PREMIUM_USERS = [7790607144]
    
    # Protection Settings
    MAX_WARNINGS = 3
    MUTE_DURATION = 300
    FLOOD_LIMIT = 5
    LOG_CHANNEL = "-1003983202182"
