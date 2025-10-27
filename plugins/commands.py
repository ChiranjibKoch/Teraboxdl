from pyrogram import Client, filters
from pyrogram.types import Message
from database import Database
from helpers import check_force_sub

db = Database()


@Client.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    """Handle /start command"""
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    
    # Check force subscription
    is_subscribed, join_button = await check_force_sub(client, user_id)
    if not is_subscribed:
        await message.reply_text(
            "⚠️ **You must join our channel to use this bot!**\n\n"
            "Please join the channel and click 'Try Again' button.",
            reply_markup=join_button
        )
        return
    
    # Add user to database
    await db.add_user(user_id, username, first_name)
    
    # Get user info
    user = await db.get_user(user_id)
    subscription_type = user.get("subscription_type", "free")
    
    welcome_text = f"""
👋 **Welcome {first_name}!**

🤖 I'm a Terabox Download Bot. Send me a Terabox link and I'll help you download it!

📊 **Your Subscription:** {subscription_type.upper()}
📥 **Daily Limit:** {"3 downloads" if subscription_type == "free" else "100 downloads"}

**Available Commands:**
/start - Start the bot
/help - Get help
/download <link> - Download from Terabox
/status - Check your subscription status
/upgrade - Upgrade to premium (contact admin)

💡 **How to use:**
Simply send a Terabox link or use /download command with the link.
"""
    
    await message.reply_text(welcome_text)


@Client.on_message(filters.command("help") & filters.private)
async def help_command(client: Client, message: Message):
    """Handle /help command"""
    user_id = message.from_user.id
    
    # Check force subscription
    is_subscribed, join_button = await check_force_sub(client, user_id)
    if not is_subscribed:
        await message.reply_text(
            "⚠️ **You must join our channel to use this bot!**\n\n"
            "Please join the channel and click 'Try Again' button.",
            reply_markup=join_button
        )
        return
    
    help_text = """
📖 **How to Use This Bot**

**For Free Users:**
• Get 3 downloads per day
• Send Terabox link directly or use /download command

**For Premium Users:**
• Get 100 downloads per day
• Priority support
• Contact admin for upgrade

**Commands:**
/start - Start the bot
/help - Show this help message
/download <link> - Download from Terabox
/status - Check your subscription status
/upgrade - Information about premium subscription

**Example:**
Send: `https://terabox.com/s/1DSPC_UmN4ALi3pD_eoFa_Q`
or
Command: `/download https://terabox.com/s/1DSPC_UmN4ALi3pD_eoFa_Q`

Need help? Contact admin!
"""
    
    await message.reply_text(help_text)


@Client.on_message(filters.command("status") & filters.private)
async def status_command(client: Client, message: Message):
    """Handle /status command"""
    user_id = message.from_user.id
    
    # Check force subscription
    is_subscribed, join_button = await check_force_sub(client, user_id)
    if not is_subscribed:
        await message.reply_text(
            "⚠️ **You must join our channel to use this bot!**\n\n"
            "Please join the channel and click 'Try Again' button.",
            reply_markup=join_button
        )
        return
    
    # Get user info
    user = await db.get_user(user_id)
    if not user:
        await message.reply_text("❌ User not found. Please use /start first.")
        return
    
    subscription_type = user.get("subscription_type", "free")
    daily_usage = await db.get_daily_usage(user_id)
    
    from config import Config
    if subscription_type == Config.SUBSCRIPTION_PREMIUM:
        limit = Config.PREMIUM_DAILY_LIMIT
        expiry = user.get("subscription_expiry")
        expiry_text = f"📅 **Expiry:** {expiry.strftime('%Y-%m-%d')}" if expiry else "📅 **Expiry:** Never"
    else:
        limit = Config.FREE_DAILY_LIMIT
        expiry_text = ""
    
    status_text = f"""
📊 **Your Subscription Status**

👤 **User ID:** `{user_id}`
💳 **Subscription:** {subscription_type.upper()}
{expiry_text}

📈 **Usage Today:** {daily_usage}/{limit}
📥 **Remaining:** {limit - daily_usage}

🔄 **Last Used:** {user.get('last_used', 'Never').strftime('%Y-%m-%d %H:%M:%S') if user.get('last_used') else 'Never'}
"""
    
    await message.reply_text(status_text)


@Client.on_message(filters.command("upgrade") & filters.private)
async def upgrade_command(client: Client, message: Message):
    """Handle /upgrade command"""
    user_id = message.from_user.id
    
    # Check force subscription
    is_subscribed, join_button = await check_force_sub(client, user_id)
    if not is_subscribed:
        await message.reply_text(
            "⚠️ **You must join our channel to use this bot!**\n\n"
            "Please join the channel and click 'Try Again' button.",
            reply_markup=join_button
        )
        return
    
    upgrade_text = """
⭐ **Upgrade to Premium**

**Premium Benefits:**
• 100 downloads per day (vs 3 for free)
• Priority support
• Faster processing
• No ads

**Pricing:**
Contact admin for pricing and payment details.

📧 **Contact Admin:** Use /start and message admin for subscription.

💡 Once you've paid, send your payment proof to admin with your user ID: `{}`
""".format(user_id)
    
    await message.reply_text(upgrade_text)
