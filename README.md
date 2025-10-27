# Terabox Telegram Bot 🤖

A subscription-based modular Telegram bot for downloading files from Terabox using Apify API. The bot features MongoDB integration, force subscription, and daily usage limits for free and premium users.

## Features ✨

- 🔐 **Force Subscription**: Users must join a channel to use the bot
- 💳 **Subscription System**: Free and Premium tiers with different limits
- 📊 **Usage Tracking**: MongoDB-based usage tracking with daily limits
- 🎯 **Free Users**: 3 downloads per day
- ⭐ **Premium Users**: 100 downloads per day
- 🛡️ **Admin Panel**: Manage subscriptions and broadcast messages
- 🔄 **Modular Design**: Easy to extend and maintain
- 🚀 **Apify Integration**: Uses Apify Actor for reliable downloads

## Requirements 📋

- Python 3.8 or higher
- MongoDB (local or cloud instance)
- Telegram Bot Token
- Telegram API ID and Hash
- Apify API Token

## Installation 🚀

### 1. Clone the repository

```bash
git clone https://github.com/ChiranjibKoch/Teraboxdl.git
cd Teraboxdl
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` file with your credentials:

```env
# Telegram Bot Configuration
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token

# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/
DATABASE_NAME=terabox_bot

# Force Subscription (optional)
FORCE_SUB_CHANNEL=-100xxxxxxxxxx

# Apify Configuration
APIFY_API_TOKEN=your_apify_api_token

# Admin Configuration
ADMIN_IDS=123456789,987654321

# Subscription Settings
FREE_DAILY_LIMIT=3
PREMIUM_DAILY_LIMIT=100
```

### 4. Getting Required Credentials

#### Telegram API ID and Hash:
1. Visit https://my.telegram.org/auth
2. Log in with your phone number
3. Go to "API Development Tools"
4. Create a new application
5. Copy API_ID and API_HASH

#### Bot Token:
1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow the instructions
4. Copy the bot token

#### Apify API Token:
1. Sign up at https://apify.com
2. Go to Settings > Integrations
3. Create a new API token
4. Copy the token

#### Force Subscription Channel:
1. Create a Telegram channel
2. Add your bot as admin
3. Get the channel ID (use [@userinfobot](https://t.me/userinfobot))
4. Use the channel ID with `-100` prefix

### 5. Set up MongoDB

#### Local MongoDB:
```bash
# Install MongoDB (Ubuntu/Debian)
sudo apt-get install mongodb

# Start MongoDB service
sudo systemctl start mongodb
```

#### MongoDB Atlas (Cloud):
1. Sign up at https://www.mongodb.com/cloud/atlas
2. Create a free cluster
3. Get the connection string
4. Update MONGODB_URI in .env

## Usage 🎮

### Starting the Bot

```bash
python bot.py
```

### User Commands

- `/start` - Start the bot and register
- `/help` - Get help information
- `/download <link>` - Download from Terabox
- `/status` - Check subscription status
- `/upgrade` - Information about premium

### Admin Commands

- `/admin` - Show admin panel
- `/stats` - View bot statistics
- `/addpremium <user_id> <days>` - Add premium to user
- `/removepremium <user_id>` - Remove premium from user
- `/userinfo <user_id>` - Get user information
- `/broadcast <message>` - Broadcast to all users

### Example Usage

**Download a file:**
```
Send: https://terabox.com/s/1DSPC_UmN4ALi3pD_eoFa_Q

or

Command: /download https://terabox.com/s/1DSPC_UmN4ALi3pD_eoFa_Q
```

**Add premium subscription:**
```
/addpremium 123456789 30
```

## Project Structure 📁

```
Teraboxdl/
├── bot.py                 # Main bot entry point
├── config.py             # Configuration management
├── requirements.txt      # Python dependencies
├── .env.example         # Example environment file
├── .gitignore          # Git ignore rules
├── database/
│   ├── __init__.py
│   └── mongodb.py      # MongoDB operations
├── helpers/
│   ├── __init__.py
│   ├── apify_downloader.py  # Apify integration
│   └── force_sub.py    # Force subscription checker
└── plugins/
    ├── __init__.py
    ├── commands.py     # Basic commands
    ├── download.py     # Download handlers
    ├── admin.py        # Admin commands
    └── callbacks.py    # Callback handlers
```

## Subscription System 💳

### Free Tier
- 3 downloads per day
- Basic support
- All standard features

### Premium Tier
- 100 downloads per day
- Priority support
- Managed by admin

## Development 🛠️

### Adding New Features

The bot uses a modular plugin system. To add new commands:

1. Create a new file in `plugins/` directory
2. Import required modules
3. Use `@Client.on_message()` decorator
4. The plugin will be automatically loaded

Example:
```python
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("mycommand") & filters.private)
async def my_command(client: Client, message: Message):
    await message.reply_text("Hello!")
```

### Database Schema

**Users Collection:**
```json
{
  "user_id": 123456789,
  "username": "user",
  "first_name": "User Name",
  "subscription_type": "free",
  "subscription_expiry": null,
  "joined_date": "2025-01-01T00:00:00",
  "last_used": "2025-01-01T12:00:00"
}
```

**Usage Collection:**
```json
{
  "user_id": 123456789,
  "link": "https://terabox.com/s/...",
  "timestamp": "2025-01-01T12:00:00"
}
```

## Troubleshooting 🔧

### Bot not responding
- Check if bot token is correct
- Ensure bot is started with `python bot.py`
- Check MongoDB connection

### Force subscription not working
- Ensure bot is admin in the channel
- Check channel ID format (-100xxxxxxxxxx)
- Verify FORCE_SUB_CHANNEL in .env

### Downloads failing
- Verify Apify API token
- Check Apify account credits
- Ensure valid Terabox URL

## Security 🔒

- Never commit `.env` file
- Keep API tokens secure
- Use environment variables for sensitive data
- Regularly update dependencies

## Contributing 🤝

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License 📄

This project is open source and available under the MIT License.

## Support 💬

For issues and questions:
- Open an issue on GitHub
- Contact the admin

## Acknowledgments 🙏

- [Pyrogram](https://docs.pyrogram.org/) - Telegram MTProto API framework
- [Apify](https://apify.com/) - Web scraping and automation platform
- [MongoDB](https://www.mongodb.com/) - Database solution

## Disclaimer ⚠️

This bot is for educational purposes. Ensure you have the right to download content and comply with Terabox's terms of service.