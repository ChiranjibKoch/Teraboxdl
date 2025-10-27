from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant, ChatAdminRequired
from config import Config


async def check_force_sub(client: Client, user_id: int):
    """
    Check if user is subscribed to the force subscription channel
    
    Args:
        client: Pyrogram client instance
        user_id: User ID to check
        
    Returns:
        tuple: (is_subscribed: bool, join_button: InlineKeyboardMarkup or None)
    """
    if Config.FORCE_SUB_CHANNEL == 0:
        return True, None
    
    try:
        member = await client.get_chat_member(Config.FORCE_SUB_CHANNEL, user_id)
        
        # Check if user is a member (not kicked or left)
        if member.status in ["member", "administrator", "creator"]:
            return True, None
        else:
            # User is not a member
            return False, await get_join_button(client)
    
    except UserNotParticipant:
        # User has not joined the channel
        return False, await get_join_button(client)
    
    except ChatAdminRequired:
        # Bot is not admin in the channel, skip force sub
        return True, None
    
    except Exception as e:
        # In case of any other error, allow access
        print(f"Force sub check error: {e}")
        return True, None


async def get_join_button(client: Client):
    """
    Get the join button for force subscription channel
    
    Args:
        client: Pyrogram client instance
        
    Returns:
        InlineKeyboardMarkup with join button
    """
    try:
        chat = await client.get_chat(Config.FORCE_SUB_CHANNEL)
        invite_link = chat.invite_link
        
        if not invite_link:
            # Try to create an invite link if bot is admin
            try:
                invite_link = await client.export_chat_invite_link(Config.FORCE_SUB_CHANNEL)
            except:
                invite_link = f"https://t.me/{chat.username}" if chat.username else None
        
        if invite_link:
            return InlineKeyboardMarkup([
                [InlineKeyboardButton("🔔 Join Channel", url=invite_link)],
                [InlineKeyboardButton("🔄 Try Again", callback_data="check_sub")]
            ])
        else:
            return None
    
    except Exception as e:
        print(f"Error getting join button: {e}")
        return None
