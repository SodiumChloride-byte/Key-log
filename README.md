# Keylogger with Telegram Integration

⚠️ **DISCLAIMER**: This tool is for educational purposes and authorized penetration testing only. 
Only use on systems you own or have explicit written permission to test.

## Description
This keylogger captures keystrokes and periodically sends them to a configured Telegram chat. 
It is designed for security research and authorized penetration testing purposes.

## ⚠️ Legal Notice
- Only use with explicit written permission from the system owner
- Unauthorized use is illegal and violates privacy laws
- This tool should only be used in controlled environments for security assessments
- The creator is not responsible for misuse of this tool
- Always follow responsible disclosure practices

## Features
- Records keystrokes silently in the background
- Periodically sends logs to a Telegram bot
- Configurable sending intervals
- Local log storage with automatic cleanup after sending
- Special key detection (Enter, Tab, Backspace, etc.)
- Size-limited messages to comply with Telegram restrictions

## Requirements
- Python 3.x
- Telegram Bot Token
- Target system permissions

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/keylogger-telegram.git
   cd keylogger-telegram

2. Install dependencies
   ```bash
   pip install -r requirements.txt

3. Configure your Telegram credentials in config.py

4. Run the Keylogger
   ```bash
   python keylogger.py

## Setup Telegram Bot
1. Open Telegram and search for @BotFather
2. Start a chat with BotFather and send /newbot
3. Follow the instructions to create a new bot
4. Copy the HTTP API token
5. Start a chat with your newly created bot and send a message (like "Hello")
6. Visit https://api.telegram.org/bot[YOUR_BOT_TOKEN]/getUpdates (replace YOUR_BOT_TOKEN)
7. Find your chat ID in the response (the "id" field under "chat")

## Configuration
Edit config.py to set your Telegram credentials:
```bash
TELEGRAM_BOT_TOKEN = "your_bot_token_here"
TELEGRAM_CHAT_ID = "your_chat_id_here"
```
Other configurable options:
1. SEND_INTERVAL: How often to send logs (in seconds)
2. LOG_FILE: Local file to temporarily store logs
3. MAX_LOG_SIZE: Maximum size of message sent to Telegram (characters)

## Usage 
```bash
python keylogger.py
```
The keylogger will start capturing keystrokes and sending them to your Telegram chat periodically. To stop the keylogger, press the ESC key.

## Technical Details
1. Uses pynput library for key capture
2. Implements multithreading to separate logging from sending
3. Handles special keys appropriately
4. Automatically truncates large logs to fit Telegram limitations
5. Deletes local log file after successful transmission
