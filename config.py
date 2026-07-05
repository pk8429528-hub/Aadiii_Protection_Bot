import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # ────═◈═─ BOT CONFIGURATION ─═◈═────
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    
    # ────═◈═─ MONGODB ─═◈═────
    MONGO_URI = os.getenv("MONGO_URI", "")
    DB_NAME = os.getenv("DB_NAME", "aadiii_protection")
    
    # ────═◈═─ OWNER ─═◈═────
    OWNER_ID = int(os.getenv("OWNER_ID", "7619471041"))
    OWNER_NAME = os.getenv("OWNER_NAME", "⏤͟͞ 𝚨 ⋏ 𝛛 ᰻ -")
    OWNER_USERNAME = os.getenv("OWNER_USERNAME", "@your_aadiii")
    
    # ────═◈═─ BOT INFO ─═◈═────
    BOT_NAME = os.getenv("BOT_NAME", "༒ ᴘɪᴋᴀᴄʜᴜᴜ ༒")
    BOT_USERNAME = os.getenv("BOT_USERNAME", "@aadiiiprotectionbot")
    
    # ────═◈═─ PREMIUM USERS ─═◈═────
    PREMIUM_USERS = [int(id.strip()) for id in os.getenv("PREMIUM_USERS", "7619471041").split(",") if id.strip()]
    
    # ────═◈═─ PROTECTION SETTINGS ─═◈═────
    MAX_WARNINGS = int(os.getenv("MAX_WARNINGS", "3"))
    MUTE_DURATION = int(os.getenv("MUTE_DURATION", "300"))
    FLOOD_LIMIT = int(os.getenv("FLOOD_LIMIT", "5"))
    LOG_CHANNEL = os.getenv("LOG_CHANNEL", "-1004293212612")
