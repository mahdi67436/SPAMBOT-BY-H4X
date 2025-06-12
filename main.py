import time
import requests
import pyautogui
import os
import sys
import random
from colorama import Fore, Style, init
from tqdm import tqdm
import threading
import webbrowser
from datetime import datetime
import pyfiglet
import socket
import platform

# Initialize colorama
init(autoreset=True)

# Global variables
VERSION = "5.1"
AUTHOR = "H4X Terminal"
RAINBOW_COLORS = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
current_theme = "default"
themes = {
    "default": {
        "text": Fore.LIGHTGREEN_EX,
        "highlight": Fore.CYAN,
        "warning": Fore.YELLOW,
        "error": Fore.RED,
        "success": Fore.GREEN
    },
    "dark": {
        "text": Fore.LIGHTBLACK_EX,
        "highlight": Fore.LIGHTMAGENTA_EX,
        "warning": Fore.LIGHTYELLOW_EX,
        "error": Fore.LIGHTRED_EX,
        "success": Fore.LIGHTGREEN_EX
    },
    "matrix": {
        "text": Fore.GREEN,
        "highlight": Fore.LIGHTGREEN_EX,
        "warning": Fore.YELLOW,
        "error": Fore.RED,
        "success": Fore.LIGHTCYAN_EX
    }
}

def get_theme_color(color_name):
    return themes[current_theme].get(color_name, Fore.WHITE)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def animate_loading(text, duration=2, color=get_theme_color("highlight")):
    symbols = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{color}{symbols[i % len(symbols)]} {text}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write("\r" + " " * (len(text) + 2) + "\r")
    sys.stdout.flush()

def typewriter(text, color=get_theme_color("text"), delay=0.005, new_line=True):
    for char in text:
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(delay)
    if new_line:
        print()

def print_rainbow_text(text):
    for i, char in enumerate(text):
        sys.stdout.write(RAINBOW_COLORS[i % len(RAINBOW_COLORS)] + char)
        sys.stdout.flush()
        time.sleep(0.001)
    print()

def print_banner():
    clear()
    banner_text = "H4X SPAMBOT"
    banner = pyfiglet.figlet_format(banner_text, font="slant")
    print_rainbow_text(banner)
    
    subtitle = f"Ultra CLI Spambot BY H4X MAHDI v{VERSION} by {AUTHOR}"
    typewriter(subtitle, color=get_theme_color("highlight"), delay=0.01)
    
    # System info
    sys_info = f"{platform.system()} {platform.release()} | Python {platform.python_version()}"
    print(get_theme_color("text") + "═" * len(sys_info))
    typewriter(sys_info, color=get_theme_color("text"), delay=0.001)
    
    # Current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    typewriter(current_time, color=get_theme_color("text"), delay=0.001)
    print(get_theme_color("text") + "═" * len(sys_info) + "\n")

def valid_url(url):
    return url.startswith(("https://discord.com/api/webhooks/", "http://discord.com/api/webhooks/"))

def webhook_spam(url, message, delay, count, image_path=None):
    if not valid_url(url):
        print(get_theme_color("error") + "[✗] Invalid Webhook URL.")
        return False

    success_count = 0
    with tqdm(total=count, desc=get_theme_color("highlight") + "Sending Messages", 
              bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
        for i in range(count):
            data = {"content": message}
            files = {'file': open(image_path, 'rb')} if image_path and os.path.isfile(image_path) else None

            try:
                response = requests.post(url, data=data, files=files)
                if response.status_code in [204, 200]:
                    success_count += 1
                    pbar.set_postfix_str(get_theme_color("success") + "Success")
                else:
                    pbar.set_postfix_str(get_theme_color("error") + f"Failed ({response.status_code})")
            except Exception as e:
                pbar.set_postfix_str(get_theme_color("error") + f"Error: {str(e)}")
            pbar.update(1)
            time.sleep(delay)
    
    return success_count

def discord_spam(token, channel_id, message, delay, count):
    headers = {"Authorization": token}
    success_count = 0
    
    # First verify the token
    animate_loading("Verifying token...")
    try:
        user_req = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
        if user_req.status_code != 200:
            print(get_theme_color("error") + f"[✗] Invalid token (Status: {user_req.status_code})")
            return False
    except Exception as e:
        print(get_theme_color("error") + f"[✗] Token verification failed: {str(e)}")
        return False
    
    with tqdm(total=count, desc=get_theme_color("highlight") + "Sending Messages", 
              bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
        for i in range(count):
            try:
                response = requests.post(
                    f"https://discord.com/api/v9/channels/{channel_id}/messages",
                    headers=headers,
                    json={"content": message}
                )
                if response.status_code == 200:
                    success_count += 1
                    pbar.set_postfix_str(get_theme_color("success") + "Success")
                else:
                    pbar.set_postfix_str(get_theme_color("error") + f"Failed ({response.status_code})")
            except Exception as e:
                pbar.set_postfix_str(get_theme_color("error") + f"Error: {str(e)}")
            pbar.update(1)
            time.sleep(delay)
    
    return success_count

def whatsapp_spam(message, delay, count):
    print(get_theme_color("warning") + "[!] Switch to WhatsApp Web chat within 5 seconds...")
    for i in range(5, 0, -1):
        print(f"\rStarting in {i}...", end="")
        time.sleep(1)
    print("\r" + " " * 20 + "\r", end="")
    
    success_count = 0
    with tqdm(total=count, desc=get_theme_color("highlight") + "Sending Messages", 
              bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
        for i in range(count):
            try:
                pyautogui.typewrite(message)
                pyautogui.press('enter')
                success_count += 1
                pbar.set_postfix_str(get_theme_color("success") + "Success")
            except Exception as e:
                pbar.set_postfix_str(get_theme_color("error") + f"Error: {str(e)}")
            pbar.update(1)
            time.sleep(delay)
    
    return success_count

def change_theme():
    global current_theme
    clear()
    print_banner()
    print(get_theme_color("highlight") + "Available Themes:\n")
    for i, theme in enumerate(themes.keys(), 1):
        print(f"[{i}] {theme.capitalize()} Theme")
    print("\n[0] Back to Main Menu\n")
    
    choice = input(get_theme_color("text") + "Select Theme: ")
    if choice == "0":
        return
    try:
        selected_theme = list(themes.keys())[int(choice)-1]
        current_theme = selected_theme
        print(get_theme_color("success") + f"\nTheme changed to {selected_theme.capitalize()}!")
        time.sleep(1)
    except (ValueError, IndexError):
        print(get_theme_color("error") + "\nInvalid selection!")
        time.sleep(1)

def show_stats():
    clear()
    print_banner()
    print(get_theme_color("highlight") + "System Statistics:\n")
    
    # System info
    typewriter(f"OS: {platform.system()} {platform.release()}", delay=0.01)
    typewriter(f"Architecture: {platform.machine()}", delay=0.01)
    typewriter(f"Python Version: {platform.python_version()}", delay=0.01)
    
    # Network info
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        typewriter(f"Hostname: {hostname}", delay=0.01)
        typewriter(f"Local IP: {local_ip}", delay=0.01)
    except:
        pass
    
    # Current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    typewriter(f"Current Time: {current_time}", delay=0.01)
    
    print("\n" + get_theme_color("text") + "Press Enter to return...")
    input()

def main_menu():
    clear()
    print_banner()
    print(get_theme_color("highlight") + "Select Mode:\n")
    print(f"[1] Discord Webhook Spam (Text/Image)")
    print(f"[2] Discord Channel Spam (Token Required)")
    print(f"[3] WhatsApp Web Spam")
    print(f"[4] Change Theme (Current: {current_theme.capitalize()})")
    print(f"[5] System Statistics")
    print(f"[6] Help / Documentation")
    print(f"[0] Exit\n")
    return input(get_theme_color("text") + "Enter Choice: ")

def show_help():
    clear()
    print_banner()
    print(get_theme_color("highlight") + "Help & Documentation:\n")
    
    typewriter("1. Discord Webhook Spam:", get_theme_color("highlight"), 0.01)
    typewriter("   - Requires a valid Discord webhook URL", get_theme_color("text"), 0.01)
    typewriter("   - Can attach images by providing full path", get_theme_color("text"), 0.01)
    
    typewriter("\n2. Discord Channel Spam:", get_theme_color("highlight"), 0.01)
    typewriter("   - Requires a valid Discord user token", get_theme_color("text"), 0.01)
    typewriter("   - Need channel ID where you have permission", get_theme_color("text"), 0.01)
    
    typewriter("\n3. WhatsApp Web Spam:", get_theme_color("highlight"), 0.01)
    typewriter("   - Requires WhatsApp Web to be open in browser", get_theme_color("text"), 0.01)
    typewriter("   - Must manually select chat window", get_theme_color("text"), 0.01)
    
    typewriter("\nNote:", get_theme_color("warning"), 0.01)
    typewriter("This tool is for educational purposes only.", get_theme_color("text"), 0.01)
    typewriter("Misuse may violate terms of service.", get_theme_color("error"), 0.01)
    
    print("\n" + get_theme_color("text") + "Press Enter to return...")
    input()

def main():
    while True:
        choice = main_menu()
        
        if choice == '1':  # Webhook Spam
            clear()
            print_banner()
            print(get_theme_color("highlight") + "Discord Webhook Spam Mode\n")
            
            url = input(get_theme_color("text") + "Webhook URL: ")
            message = input(get_theme_color("text") + "Message to Spam: ")
            image = None
            if input(get_theme_color("text") + "Attach Image? (y/n): ").lower() == 'y':
                image = input(get_theme_color("text") + "Full path to image file: ")
                if not os.path.isfile(image):
                    print(get_theme_color("error") + "[✗] File not found.")
                    image = None
            delay = max(0.5, float(input(get_theme_color("text") + "Delay (sec, min 0.5): ")))
            count = int(input(get_theme_color("text") + "Total messages: "))
            
            success = webhook_spam(url, message, delay, count, image)
            print(get_theme_color("success") + f"\n[✓] Completed! {success}/{count} messages sent successfully.")
            
        elif choice == '2':  # Discord Channel Spam
            clear()
            print_banner()
            print(get_theme_color("highlight") + "Discord Channel Spam Mode\n")
            
            token = input(get_theme_color("text") + "Discord Token: ")
            channel = input(get_theme_color("text") + "Channel ID: ")
            message = input(get_theme_color("text") + "Message to Spam: ")
            delay = max(1.0, float(input(get_theme_color("text") + "Delay (sec, min 1.0): ")))
            count = int(input(get_theme_color("text") + "Total messages: "))
            
            success = discord_spam(token, channel, message, delay, count)
            if success is not False:
                print(get_theme_color("success") + f"\n[✓] Completed! {success}/{count} messages sent successfully.")
            
        elif choice == '3':  # WhatsApp Spam
            clear()
            print_banner()
            print(get_theme_color("highlight") + "WhatsApp Web Spam Mode\n")
            
            webbrowser.open("https://web.whatsapp.com")
            message = input(get_theme_color("text") + "Message to Spam: ")
            delay = max(0.5, float(input(get_theme_color("text") + "Delay (sec, min 0.5): ")))
            count = int(input(get_theme_color("text") + "Total messages: "))
            
            success = whatsapp_spam(message, delay, count)
            print(get_theme_color("success") + f"\n[✓] Completed! {success}/{count} messages sent successfully.")
            
        elif choice == '4':  # Change Theme
            change_theme()
            
        elif choice == '5':  # System Stats
            show_stats()
            
        elif choice == '6':  # Help
            show_help()
            
        elif choice == '0':  # Exit
            print(get_theme_color("warning") + "\n[!] Exiting... Remember to use this tool responsibly!")
            time.sleep(1)
            clear()
            sys.exit(0)
            
        else:
            print(get_theme_color("error") + "\n[✗] Invalid Option!")
            time.sleep(1)
        
        input(get_theme_color("text") + "\n[Press Enter to return to menu...]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(get_theme_color("error") + "\n[✗] Script interrupted by user!")
        time.sleep(1)
        clear()
        sys.exit(0)