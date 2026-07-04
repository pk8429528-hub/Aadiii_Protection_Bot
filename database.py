from pymongo import MongoClient
from config import Config
import datetime

class Database:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_URI)
        self.db = self.client[Config.DB_NAME]
        
        # Collections
        self.users = self.db.users
        self.groups = self.db.groups
        self.warnings = self.db.warnings
        self.mutes = self.db.mutes
        self.settings = self.db.settings
        self.premium = self.db.premium
    
    # ────═◈═─ USER METHODS ─═◈═────
    async def add_user(self, user_id, username=None, first_name=None):
        if not self.users.find_one({"user_id": user_id}):
            return self.users.insert_one({
                "user_id": user_id,
                "username": username,
                "first_name": first_name,
                "joined_date": datetime.datetime.now()
            })
    
    async def get_user(self, user_id):
        return self.users.find_one({"user_id": user_id})
    
    # ────═◈═─ GROUP METHODS ─═◈═────
    async def add_group(self, group_id, title):
        if not self.groups.find_one({"group_id": group_id}):
            return self.groups.insert_one({
                "group_id": group_id,
                "title": title,
                "added_date": datetime.datetime.now()
            })
    
    async def get_group(self, group_id):
        return self.groups.find_one({"group_id": group_id})
    
    # ────═◈═─ WARNING METHODS ─═◈═────
    async def add_warning(self, user_id, group_id, reason, admin_id):
        return self.warnings.insert_one({
            "user_id": user_id,
            "group_id": group_id,
            "reason": reason,
            "admin_id": admin_id,
            "date": datetime.datetime.now()
        })
    
    async def get_warnings(self, user_id, group_id):
        return list(self.warnings.find({
            "user_id": user_id,
            "group_id": group_id
        }))
    
    async def clear_warnings(self, user_id, group_id):
        return self.warnings.delete_many({
            "user_id": user_id,
            "group_id": group_id
        })
    
    # ────═◈═─ MUTE METHODS ─═◈═────
    async def add_mute(self, user_id, group_id, duration, reason, admin_id):
        mute_until = datetime.datetime.now() + datetime.timedelta(seconds=duration)
        return self.mutes.insert_one({
            "user_id": user_id,
            "group_id": group_id,
            "duration": duration,
            "reason": reason,
            "admin_id": admin_id,
            "mute_until": mute_until,
            "mute_date": datetime.datetime.now()
        })
    
    async def get_mute(self, user_id, group_id):
        return self.mutes.find_one({
            "user_id": user_id,
            "group_id": group_id
        })
    
    async def remove_mute(self, user_id, group_id):
        return self.mutes.delete_one({
            "user_id": user_id,
            "group_id": group_id
        })
    
    # ────═◈═─ SETTINGS METHODS ─═◈═────
    async def get_settings(self, group_id):
        settings = self.settings.find_one({"group_id": group_id})
        if not settings:
            settings = {
                "group_id": group_id,
                "welcome": True,
                "goodbye": True,
                "antispam": True,
                "antilink": False,
                "anti18": True,
                "warn_limit": 3,
                "mute_duration": 300,
                "approved_users": [],
                "custom_welcome": None,
                "custom_goodbye": None
            }
            self.settings.insert_one(settings)
        return settings
    
    async def update_settings(self, group_id, key, value):
        return self.settings.update_one(
            {"group_id": group_id},
            {"$set": {key: value}},
            upsert=True
        )
    
    # ────═◈═─ CUSTOM WELCOME/GIODBYE METHODS ─═◈═────
    async def set_custom_welcome(self, group_id, message):
        return self.settings.update_one(
            {"group_id": group_id},
            {"$set": {"custom_welcome": message}},
            upsert=True
        )
    
    async def get_custom_welcome(self, group_id):
        settings = self.settings.find_one({"group_id": group_id})
        return settings.get("custom_welcome") if settings else None
    
    async def set_custom_goodbye(self, group_id, message):
        return self.settings.update_one(
            {"group_id": group_id},
            {"$set": {"custom_goodbye": message}},
            upsert=True
        )
    
    async def get_custom_goodbye(self, group_id):
        settings = self.settings.find_one({"group_id": group_id})
        return settings.get("custom_goodbye") if settings else None
    
    # ────═◈═─ APPROVE/UNAPPROVE METHODS ─═◈═────
    async def approve_user(self, user_id, group_id):
        return self.settings.update_one(
            {"group_id": group_id},
            {"$addToSet": {"approved_users": user_id}},
            upsert=True
        )
    
    async def unapprove_user(self, user_id, group_id):
        return self.settings.update_one(
            {"group_id": group_id},
            {"$pull": {"approved_users": user_id}}
        )
    
    async def is_approved(self, user_id, group_id):
        settings = self.settings.find_one({"group_id": group_id})
        if settings and "approved_users" in settings:
            return user_id in settings["approved_users"]
        return False
    
    # ────═◈═─ PREMIUM METHODS ─═◈═────
    async def check_premium(self, user_id):
        premium = self.premium.find_one({"user_id": user_id})
        if premium and premium.get("expiry_date"):
            if premium["expiry_date"] > datetime.datetime.now():
                return True
            else:
                self.premium.delete_one({"user_id": user_id})
        return False
    
    async def add_premium(self, user_id, days=30):
        expiry = datetime.datetime.now() + datetime.timedelta(days=days)
        return self.premium.update_one(
            {"user_id": user_id},
            {"$set": {
                "user_id": user_id,
                "expiry_date": expiry,
                "added_date": datetime.datetime.now()
            }},
            upsert=True
        )
