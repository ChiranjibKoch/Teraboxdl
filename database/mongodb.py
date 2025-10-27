from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
from config import Config


class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(Config.MONGODB_URI)
        self.db = self.client[Config.DATABASE_NAME]
        self.users = self.db.users
        self.usage = self.db.usage
        
    async def add_user(self, user_id: int, username: str = None, first_name: str = None):
        """Add a new user to the database"""
        user_data = {
            "user_id": user_id,
            "username": username,
            "first_name": first_name,
            "subscription_type": Config.SUBSCRIPTION_FREE,
            "subscription_expiry": None,
            "joined_date": datetime.now(),
            "last_used": datetime.now()
        }
        
        existing_user = await self.users.find_one({"user_id": user_id})
        if not existing_user:
            await self.users.insert_one(user_data)
            return True
        return False
    
    async def get_user(self, user_id: int):
        """Get user information"""
        return await self.users.find_one({"user_id": user_id})
    
    async def update_user_subscription(self, user_id: int, subscription_type: str, days: int = None):
        """Update user subscription type"""
        update_data = {
            "subscription_type": subscription_type,
            "last_used": datetime.now()
        }
        
        if days and subscription_type == Config.SUBSCRIPTION_PREMIUM:
            update_data["subscription_expiry"] = datetime.now() + timedelta(days=days)
        else:
            update_data["subscription_expiry"] = None
            
        await self.users.update_one(
            {"user_id": user_id},
            {"$set": update_data}
        )
    
    async def check_subscription_expired(self, user_id: int):
        """Check if premium subscription has expired"""
        user = await self.get_user(user_id)
        if not user:
            return True
            
        if user.get("subscription_type") == Config.SUBSCRIPTION_PREMIUM:
            expiry = user.get("subscription_expiry")
            if expiry and expiry < datetime.now():
                # Downgrade to free
                await self.update_user_subscription(user_id, Config.SUBSCRIPTION_FREE)
                return True
            return False
        return False
    
    async def get_daily_usage(self, user_id: int):
        """Get today's usage count for a user"""
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        count = await self.usage.count_documents({
            "user_id": user_id,
            "timestamp": {"$gte": today_start}
        })
        return count
    
    async def add_usage(self, user_id: int, link: str):
        """Record a download request"""
        usage_data = {
            "user_id": user_id,
            "link": link,
            "timestamp": datetime.now()
        }
        await self.usage.insert_one(usage_data)
        
        # Update last used time
        await self.users.update_one(
            {"user_id": user_id},
            {"$set": {"last_used": datetime.now()}}
        )
    
    async def can_use_bot(self, user_id: int):
        """Check if user can make a download request"""
        user = await self.get_user(user_id)
        if not user:
            return False, 0, 0
        
        # Check if subscription expired
        await self.check_subscription_expired(user_id)
        user = await self.get_user(user_id)  # Refresh user data
        
        subscription_type = user.get("subscription_type", Config.SUBSCRIPTION_FREE)
        daily_usage = await self.get_daily_usage(user_id)
        
        if subscription_type == Config.SUBSCRIPTION_PREMIUM:
            limit = Config.PREMIUM_DAILY_LIMIT
        else:
            limit = Config.FREE_DAILY_LIMIT
        
        can_use = daily_usage < limit
        return can_use, daily_usage, limit
    
    async def get_all_users(self):
        """Get all users (for admin purposes)"""
        cursor = self.users.find({})
        users = await cursor.to_list(length=None)
        return users
    
    async def get_user_count(self):
        """Get total user count"""
        return await self.users.count_documents({})
