from pyrogram import Client, filters
from pyrogram.types import Message
from database import Database
from config import Config

db = Database()


@Client.on_message(filters.command("admin") & filters.private & filters.user(Config.ADMIN_IDS))
async def admin_panel(client: Client, message: Message):
    """Show admin panel"""
    admin_text = """
🛡️ **Admin Panel**

**Available Commands:**
/stats - View bot statistics
/broadcast <message> - Broadcast message to all users
/addpremium <user_id> <days> - Add premium to user
/removepremium <user_id> - Remove premium from user
/userinfo <user_id> - Get user information

Use these commands to manage the bot.
"""
    await message.reply_text(admin_text)


@Client.on_message(filters.command("stats") & filters.private & filters.user(Config.ADMIN_IDS))
async def stats_command(client: Client, message: Message):
    """Show bot statistics"""
    total_users = await db.get_user_count()
    
    # Count premium users
    all_users = await db.get_all_users()
    premium_users = sum(1 for user in all_users if user.get("subscription_type") == Config.SUBSCRIPTION_PREMIUM)
    free_users = total_users - premium_users
    
    stats_text = f"""
📊 **Bot Statistics**

👥 **Total Users:** {total_users}
⭐ **Premium Users:** {premium_users}
🆓 **Free Users:** {free_users}

📈 **Activity:**
Active today: (Coming soon)
Total downloads: (Coming soon)
"""
    
    await message.reply_text(stats_text)


@Client.on_message(filters.command("addpremium") & filters.private & filters.user(Config.ADMIN_IDS))
async def add_premium(client: Client, message: Message):
    """Add premium subscription to a user"""
    if len(message.command) < 3:
        await message.reply_text(
            "❌ **Usage:** `/addpremium <user_id> <days>`\n"
            "Example: `/addpremium 123456789 30`"
        )
        return
    
    try:
        user_id = int(message.command[1])
        days = int(message.command[2])
    except ValueError:
        await message.reply_text("❌ Invalid user_id or days. Both must be numbers.")
        return
    
    # Check if user exists
    user = await db.get_user(user_id)
    if not user:
        await message.reply_text(f"❌ User {user_id} not found in database.")
        return
    
    # Add premium
    await db.update_user_subscription(user_id, Config.SUBSCRIPTION_PREMIUM, days)
    
    await message.reply_text(
        f"✅ **Premium Added!**\n\n"
        f"User ID: `{user_id}`\n"
        f"Duration: {days} days\n"
        f"Subscription: PREMIUM"
    )
    
    # Notify user
    try:
        await client.send_message(
            user_id,
            f"🎉 **Congratulations!**\n\n"
            f"You have been upgraded to **PREMIUM** subscription!\n"
            f"Duration: {days} days\n"
            f"Daily Limit: {Config.PREMIUM_DAILY_LIMIT} downloads\n\n"
            f"Enjoy your premium benefits!"
        )
    except:
        pass


@Client.on_message(filters.command("removepremium") & filters.private & filters.user(Config.ADMIN_IDS))
async def remove_premium(client: Client, message: Message):
    """Remove premium subscription from a user"""
    if len(message.command) < 2:
        await message.reply_text(
            "❌ **Usage:** `/removepremium <user_id>`\n"
            "Example: `/removepremium 123456789`"
        )
        return
    
    try:
        user_id = int(message.command[1])
    except ValueError:
        await message.reply_text("❌ Invalid user_id. Must be a number.")
        return
    
    # Check if user exists
    user = await db.get_user(user_id)
    if not user:
        await message.reply_text(f"❌ User {user_id} not found in database.")
        return
    
    # Remove premium
    await db.update_user_subscription(user_id, Config.SUBSCRIPTION_FREE)
    
    await message.reply_text(
        f"✅ **Premium Removed!**\n\n"
        f"User ID: `{user_id}`\n"
        f"Subscription: FREE"
    )
    
    # Notify user
    try:
        await client.send_message(
            user_id,
            f"📢 **Subscription Update**\n\n"
            f"Your premium subscription has expired or been removed.\n"
            f"You are now on **FREE** plan.\n"
            f"Daily Limit: {Config.FREE_DAILY_LIMIT} downloads\n\n"
            f"Use /upgrade to renew your premium subscription."
        )
    except:
        pass


@Client.on_message(filters.command("userinfo") & filters.private & filters.user(Config.ADMIN_IDS))
async def user_info(client: Client, message: Message):
    """Get user information"""
    if len(message.command) < 2:
        await message.reply_text(
            "❌ **Usage:** `/userinfo <user_id>`\n"
            "Example: `/userinfo 123456789`"
        )
        return
    
    try:
        user_id = int(message.command[1])
    except ValueError:
        await message.reply_text("❌ Invalid user_id. Must be a number.")
        return
    
    # Get user info
    user = await db.get_user(user_id)
    if not user:
        await message.reply_text(f"❌ User {user_id} not found in database.")
        return
    
    daily_usage = await db.get_daily_usage(user_id)
    subscription_type = user.get("subscription_type", "free")
    
    from config import Config
    limit = Config.PREMIUM_DAILY_LIMIT if subscription_type == Config.SUBSCRIPTION_PREMIUM else Config.FREE_DAILY_LIMIT
    
    info_text = f"""
👤 **User Information**

**ID:** `{user_id}`
**Username:** @{user.get('username', 'N/A')}
**Name:** {user.get('first_name', 'N/A')}

**Subscription:** {subscription_type.upper()}
**Expiry:** {user.get('subscription_expiry', 'N/A')}

**Usage Today:** {daily_usage}/{limit}
**Joined:** {user.get('joined_date', 'N/A')}
**Last Used:** {user.get('last_used', 'N/A')}
"""
    
    await message.reply_text(info_text)


@Client.on_message(filters.command("broadcast") & filters.private & filters.user(Config.ADMIN_IDS))
async def broadcast_message(client: Client, message: Message):
    """Broadcast message to all users"""
    if message.reply_to_message:
        broadcast_msg = message.reply_to_message
    elif len(message.command) > 1:
        broadcast_text = message.text.split(None, 1)[1]
        broadcast_msg = await message.reply_text(broadcast_text)
    else:
        await message.reply_text(
            "❌ **Usage:** Reply to a message with `/broadcast` or use `/broadcast <message>`"
        )
        return
    
    users = await db.get_all_users()
    success = 0
    failed = 0
    
    status_msg = await message.reply_text(f"📢 Broadcasting to {len(users)} users...")
    
    for user in users:
        try:
            await broadcast_msg.copy(user["user_id"])
            success += 1
        except:
            failed += 1
    
    await status_msg.edit_text(
        f"✅ **Broadcast Complete!**\n\n"
        f"Success: {success}\n"
        f"Failed: {failed}\n"
        f"Total: {len(users)}"
    )
