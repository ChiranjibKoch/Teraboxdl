# Contributing to Terabox Telegram Bot

Thank you for your interest in contributing to this project! 🎉

## How to Contribute

### Reporting Bugs 🐛

If you find a bug, please create an issue with:
- A clear title and description
- Steps to reproduce the issue
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)

### Suggesting Features 💡

Feature suggestions are welcome! Please create an issue with:
- Clear description of the feature
- Use cases and benefits
- Any implementation ideas

### Pull Requests 🔧

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add comments where necessary
   - Update documentation if needed

4. **Test your changes**
   - Ensure the bot runs without errors
   - Test new features thoroughly

5. **Commit your changes**
   ```bash
   git commit -m "Add: description of your changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Describe your changes
   - Reference any related issues

## Code Style Guidelines

### Python Code
- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

### Example:
```python
async def process_download(client: Client, message: Message, url: str):
    """
    Process a Terabox download request
    
    Args:
        client: Pyrogram client instance
        message: Message object
        url: Terabox URL to download
    """
    # Your code here
```

### File Organization
- Place new commands in appropriate plugin files
- Create new plugin files for new feature categories
- Update `__init__.py` files when adding new modules

## Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Teraboxdl.git
   cd Teraboxdl
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

4. Run the bot:
   ```bash
   python bot.py
   ```

## Adding New Features

### Adding a New Command

1. Create or edit a plugin file in `plugins/` directory
2. Import required modules
3. Use decorator pattern:

```python
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("mycommand") & filters.private)
async def my_command(client: Client, message: Message):
    await message.reply_text("Response text")
```

### Adding Database Functions

1. Edit `database/mongodb.py`
2. Add async methods to the Database class
3. Document parameters and return values

### Adding Helper Functions

1. Create a new file in `helpers/` directory
2. Export in `helpers/__init__.py`
3. Import where needed

## Testing

Before submitting a PR:
- [ ] Test all affected commands
- [ ] Verify database operations work correctly
- [ ] Check for Python syntax errors
- [ ] Ensure no sensitive data is committed

## Questions?

Feel free to open an issue for any questions or clarifications!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
