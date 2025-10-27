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
