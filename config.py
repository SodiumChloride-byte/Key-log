"""
Configuration file for Keylogger with Telegram Integration
Ensure this file is properly secured and not exposed publicly
"""

# === Telegram Settings ===
# Obtain these values by creating a bot with @BotFather on Telegram
TELEGRAM_BOT_TOKEN = "your_bot_token_here"          # e.g., "123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ"
TELEGRAM_CHAT_ID = "your_chat_id_here"              # e.g., "987654321"

# === Logging Settings ===
LOG_FILE = "keylogs.txt"                           # Local temporary log storage
SEND_INTERVAL = 60                                 # Send logs every X seconds
MAX_LOG_SIZE = 4000                                # Max chars per Telegram message (Telegram limit ~4096)

# === Application Behavior ===
APP_NAME = "Keylogger Service"                     # Process name (for discretion)
BUFFER_FLUSH_THRESHOLD = 100                       # Flush buffer after X keystrokes

# === Security Settings ===
ENABLE_ENCRYPTION = False                          # Future enhancement placeholder
ENCRYPTION_KEY = ""                                # Future enhancement placeholder
