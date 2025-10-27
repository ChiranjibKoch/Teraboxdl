"""
Setup script for Terabox Bot
"""
import os
import sys


def check_env_file():
    """Check if .env file exists"""
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("📝 Creating .env from .env.example...")
        
        if os.path.exists('.env.example'):
            with open('.env.example', 'r') as example:
                with open('.env', 'w') as env:
                    env.write(example.read())
            print("✅ .env file created. Please edit it with your credentials.")
        else:
            print("❌ .env.example not found!")
        return False
    return True


def check_required_vars():
    """Check if required environment variables are set"""
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = [
        'API_ID',
        'API_HASH',
        'BOT_TOKEN',
        'APIFY_API_TOKEN',
        'MONGODB_URI'
    ]
    
    missing = []
    for var in required_vars:
        if not os.getenv(var) or os.getenv(var) == f"your_{var.lower()}":
            missing.append(var)
    
    if missing:
        print("❌ Missing or unconfigured environment variables:")
        for var in missing:
            print(f"  - {var}")
        return False
    
    print("✅ All required environment variables are set")
    return True


def test_mongodb():
    """Test MongoDB connection"""
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        from config import Config
        import asyncio
        
        async def test():
            client = AsyncIOMotorClient(Config.MONGODB_URI)
            await client.server_info()
            client.close()
            print("✅ MongoDB connection successful")
            return True
        
        asyncio.run(test())
        return True
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False


def main():
    """Main setup function"""
    print("🤖 Terabox Bot Setup")
    print("=" * 50)
    
    # Check environment file
    if not check_env_file():
        sys.exit(1)
    
    # Check required variables
    if not check_required_vars():
        print("\n⚠️ Please configure your .env file before running the bot")
        sys.exit(1)
    
    # Test MongoDB connection
    print("\n🔍 Testing MongoDB connection...")
    if not test_mongodb():
        print("\n⚠️ Please check your MongoDB configuration")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✅ Setup complete! You can now run the bot with:")
    print("   python bot.py")
    print("   or")
    print("   ./run.sh")


if __name__ == "__main__":
    main()
