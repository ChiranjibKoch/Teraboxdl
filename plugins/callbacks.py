from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from helpers import check_force_sub


@Client.on_callback_query(filters.regex("^check_sub$"))
async def check_subscription_callback(client: Client, callback_query: CallbackQuery):
    """Handle check subscription callback"""
    user_id = callback_query.from_user.id
    
    # Check if user has joined
    is_subscribed, join_button = await check_force_sub(client, user_id)
    
    if is_subscribed:
        await callback_query.answer("✅ You are now subscribed! You can use the bot.", show_alert=True)
        await callback_query.message.delete()
        
        # Send welcome message
        await client.send_message(
            user_id,
            "✅ **Subscription Verified!**\n\n"
            "You can now use the bot. Send /start to begin."
        )
    else:
        await callback_query.answer("❌ You haven't joined the channel yet!", show_alert=True)
