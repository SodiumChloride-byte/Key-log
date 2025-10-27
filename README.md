# Key-log

# Keylogger with Telegram Integration

⚠️ **DISCLAIMER**: This tool is for educational purposes and authorized penetration testing only. Only use on systems you own or have explicit written permission to test.

## Features
- Records keystrokes
- Sends logs to Telegram bot
- Configurable sending intervals
- Local log storage

## Requirements
- Python 3.x
- Telegram Bot Token
- Target system permissions

## Installation
1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure your Telegram credentials in `config.py`
4. Run: `python keylogger.py`

## Configuration
Set your Telegram bot token and chat ID in `config.py`:

```python
TELEGRAM_BOT_TOKEN = "your_bot_token_here"
TELEGRAM_CHAT_ID = "your_chat_id_here"
