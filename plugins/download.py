from pyrogram import Client, filters
from pyrogram.types import Message
from database import Database
from helpers import check_force_sub, TeraboxDownloader
import re

db = Database()
downloader = TeraboxDownloader()

# Terabox URL pattern
TERABOX_PATTERN = re.compile(r'https?://(?:www\.)?terabox\.com/s/[a-zA-Z0-9_-]+')


async def process_download(client: Client, message: Message, url: str):
    """Process a Terabox download request"""
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
    
    # Check user limits
    can_use, daily_usage, limit = await db.can_use_bot(user_id)
    
    if not can_use:
        await message.reply_text(
            f"❌ **Daily Limit Reached!**\n\n"
            f"You have used {daily_usage}/{limit} downloads today.\n"
            f"Please try again tomorrow or upgrade to premium for more downloads.\n\n"
            f"Use /upgrade to learn more about premium subscription."
        )
        return
    
    # Validate URL
    if not TERABOX_PATTERN.match(url):
        await message.reply_text(
            "❌ **Invalid Terabox URL!**\n\n"
            "Please provide a valid Terabox link.\n"
            "Example: `https://terabox.com/s/1DSPC_UmN4ALi3pD_eoFa_Q`"
        )
        return
    
    # Send processing message
    status_msg = await message.reply_text(
        f"⏳ **Processing your request...**\n\n"
        f"📊 Usage: {daily_usage + 1}/{limit}\n"
        f"🔗 Link: `{url}`\n\n"
        f"Please wait, this may take a moment..."
    )
    
    try:
        # Download using Apify
        results = await downloader.download([url])
        
        if not results:
            await status_msg.edit_text(
                "❌ **Download Failed!**\n\n"
                "No results returned. Please check the link and try again."
            )
            return
        
        # Record usage
        await db.add_usage(user_id, url)
        
        # Send results
        await status_msg.edit_text("✅ **Download Complete!**\n\nSending results...")
        
        for item in results:
            result_text = downloader.format_result(item)
            await message.reply_text(result_text, disable_web_page_preview=False)
        
        # Update usage info
        new_usage = daily_usage + 1
        await message.reply_text(
            f"✅ **Success!**\n\n"
            f"📊 Daily Usage: {new_usage}/{limit}\n"
            f"📥 Remaining: {limit - new_usage}"
        )
        
    except Exception as e:
        await status_msg.edit_text(
            f"❌ **Error occurred!**\n\n"
            f"Error: {str(e)}\n\n"
            f"Please try again or contact admin if the problem persists."
        )
        print(f"Download error: {e}")


@Client.on_message(filters.command("download") & filters.private)
async def download_command(client: Client, message: Message):
    """Handle /download command"""
    # Extract URL from command
    if len(message.command) < 2:
        await message.reply_text(
            "❌ **Missing URL!**\n\n"
            "Usage: `/download <terabox_url>`\n"
            "Example: `/download https://terabox.com/s/1DSPC_UmN4ALi3pD_eoFa_Q`"
        )
        return
    
    url = message.command[1]
    await process_download(client, message, url)


@Client.on_message(filters.regex(TERABOX_PATTERN) & filters.private)
async def download_by_url(client: Client, message: Message):
    """Handle direct URL messages"""
    url = message.text.strip()
    await process_download(client, message, url)
