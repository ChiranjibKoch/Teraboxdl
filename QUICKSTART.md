# Quick Start Guide 🚀

This guide will help you get the Terabox Telegram Bot up and running in minutes.

## Prerequisites

- Python 3.8+
- MongoDB (local or cloud)
- Telegram account
- Apify account

## Step-by-Step Setup

### 1. Get Your Credentials

#### A. Telegram Bot Token
```bash
1. Open Telegram and search for @BotFather
2. Send /newbot
3. Follow instructions and copy the token
```

#### B. Telegram API Credentials
```bash
1. Visit https://my.telegram.org/auth
2. Login with your phone
3. Go to "API Development Tools"
4. Copy API_ID and API_HASH
```

#### C. Apify API Token
```bash
1. Sign up at https://apify.com
2. Go to Settings > Integrations
3. Create API token
4. Copy the token
```

#### D. Force Subscription Channel (Optional)
```bash
1. Create a Telegram channel
2. Add your bot as admin
3. Get channel ID using @userinfobot
4. Use format: -100xxxxxxxxxx
```

### 2. Clone and Configure

```bash
# Clone repository
git clone https://github.com/ChiranjibKoch/Teraboxdl.git
cd Teraboxdl

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Edit with your credentials
```

### 3. Set Up MongoDB

**Option A: Local MongoDB**
```bash
# Ubuntu/Debian
sudo apt-get install mongodb
sudo systemctl start mongodb
```

**Option B: MongoDB Atlas (Cloud)**
```bash
1. Create account at https://www.mongodb.com/cloud/atlas
2. Create free cluster
3. Get connection string
4. Update MONGODB_URI in .env
```

### 4. Run the Bot

**Method 1: Direct Python**
```bash
python bot.py
```

**Method 2: Using Run Script**
```bash
chmod +x run.sh
./run.sh
```

**Method 3: Docker**
```bash
docker-compose up -d
```

**Method 4: Systemd Service**
```bash
# Edit service file with correct paths
sudo cp terabox-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start terabox-bot
sudo systemctl enable terabox-bot
```

### 5. Test the Bot

1. Open Telegram
2. Search for your bot
3. Send `/start`
4. Try downloading a Terabox link

## Example .env Configuration

```env
# Telegram
API_ID=12345678
API_HASH=abcdef1234567890abcdef1234567890
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# MongoDB
MONGODB_URI=mongodb://localhost:27017/
DATABASE_NAME=terabox_bot

# Force Sub (optional, use 0 to disable)
FORCE_SUB_CHANNEL=-1001234567890

# Apify
APIFY_API_TOKEN=apify_api_xxxxxxxxxxxxxxxxxxxxxxxx

# Admin (your Telegram user ID)
ADMIN_IDS=123456789

# Limits
FREE_DAILY_LIMIT=3
PREMIUM_DAILY_LIMIT=100
```

## Common Issues

### Bot not responding
- Check if bot token is correct
- Verify bot is running (`ps aux | grep bot.py`)
- Check logs for errors

### MongoDB connection failed
- Ensure MongoDB is running (`sudo systemctl status mongodb`)
- Check MONGODB_URI in .env
- For MongoDB Atlas, check if IP is whitelisted

### Force subscription not working
- Verify bot is admin in channel
- Check channel ID format (-100xxxxxxxxxx)
- Use 0 to disable force subscription

### Downloads failing
- Verify Apify API token
- Check Apify account credits
- Ensure Terabox URL is valid

## Getting Help

- Check [README.md](README.md) for detailed documentation
- See [CONTRIBUTING.md](CONTRIBUTING.md) for development guide
- Open an issue on GitHub

## Next Steps

- Add your channel for force subscription
- Configure admin IDs
- Customize daily limits
- Set up premium subscriptions
- Share your bot with users!

Happy downloading! 🎉
