import sys
import time

# Colors for styling the banner
green = "\033[0;32m"
red = "\033[0;31m"
cyan = "\033[0;36m"
yellow = "\033[0;33m"
blue = "\033[0;34m"
purple = "\033[0;35m"

# Banner content
logo = f'''
{green}             _           ____                                  
{red}__   ___   _| |_ __     / ___|  ___ __ _ _ __  _ __   ___ _ __ 
{cyan}\\ \\ / / | | | | '_ \\    \\___ \\ / __/ _` | '_ \\| '_ \\ / _ \\ '__|
{yellow} \\ V /| |_| | | | | |    ___) | (_| (_| | | | | | | |  __/ |   
{blue}  \\_/  \\__,_|_|_| |_|___|____/ \\___\\__,_|_| |_|_| |_|\\___|_|   
{purple}                   |_____|                                     
{green}
'''

def generate_banner():
    """Displays the banner with a typing effect."""
    for char in logo:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01)
