# src/utils/banner.py

import sys
import time

from colorama import Fore, Style, init

# Initialize colorama
init()


def type_text(text, delay=0.002):
    """Animated typing effect for text"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)


def print_header():
    """Print the MAISQUELLE ASCII art header with typing animation"""
    header = f"""{Fore.YELLOW}
╔══════════════════════════════════════════════════════════════════════════════╗
║ ███╗   ███╗ █████╗ ██╗███████╗ ██████╗ ██╗   ██╗███████╗██╗     ██╗     ███████╗ ║
║ ████╗ ████║██╔══██╗██║██╔════╝██╔═══██╗██║   ██║██╔════╝██║     ██║     ██╔════╝ ║
║ ██╔████╔██║███████║██║███████╗██║   ██║██║   ██║█████╗  ██║     ██║     █████╗   ║
║ ██║╚██╔╝██║██╔══██║██║╚════██║██║▄▄ ██║██║   ██║██╔══╝  ██║     ██║     ██╔══╝   ║
║ ██║ ╚═╝ ██║██║  ██║██║███████║╚██████╔╝╚██████╔╝███████╗███████╗███████╗███████╗ ║
║ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝ ╚══▀▀═╝  ╚═════╝ ╚══════╝╚══════╝╚══════╝╚══════╝ ║
╚══════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}"""

    tagline = f"\n{Fore.CYAN}                MySQL Performance Monitor & Optimization Tool{Style.RESET_ALL}\n"

    # Clear any previous output (optional)
    print("\033[H\033[J", end="")

    # Print header with typing animation
    type_text(header)

    # Print tagline with slightly slower typing effect
    type_text(tagline, delay=0.01)

    # Add a small pause at the end
    time.sleep(0.5)

    # Optional separator after the banner
    print(f"{Fore.YELLOW}{'═' * 78}{Style.RESET_ALL}\n")


def clear_screen():
    """Clear the terminal screen"""
    print("\033[H\033[J", end="")


if __name__ == "__main__":
    # Test the banner if this file is run directly
    print_header()
