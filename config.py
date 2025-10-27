import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram Bot Configuration
    API_ID = int(os.getenv("API_ID", "0"))
    API_HASH = os.getenv("API_HASH", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    
    # MongoDB Configuration
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "terabox_bot")
    
    # Force Subscription
    FORCE_SUB_CHANNEL = int(os.getenv("FORCE_SUB_CHANNEL", "0"))
    
    # Apify Configuration
    APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN", "")
    
    # Admin Configuration
    ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(","))) if os.getenv("ADMIN_IDS") else []
    
    # Subscription Settings
    FREE_DAILY_LIMIT = int(os.getenv("FREE_DAILY_LIMIT", "3"))
    PREMIUM_DAILY_LIMIT = int(os.getenv("PREMIUM_DAILY_LIMIT", "100"))
    
    # User Subscription Types
    SUBSCRIPTION_FREE = "free"
    SUBSCRIPTION_PREMIUM = "premium"
