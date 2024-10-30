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

    subtitle = f"""{Fore.CYAN}
MySQL {Fore.WHITE}A{Fore.CYAN}rtificial {Fore.WHITE}I{Fore.CYAN}ntelligence {Fore.WHITE}S{Fore.CYAN}ystem for
{Fore.WHITE}Q{Fore.CYAN}uerying, {Fore.WHITE}U{Fore.CYAN}nderstanding, {Fore.WHITE}E{Fore.CYAN}valuating,
{Fore.WHITE}L{Fore.CYAN}earning and {Fore.WHITE}L{Fore.CYAN}og {Fore.WHITE}E{Fore.CYAN}nhancement{Style.RESET_ALL}"""

    # Clear any previous output
    print("\033[H\033[J", end="")

    # Print header with typing animation
    type_text(header)

    # Print subtitle with medium typing effect
    type_text(subtitle, delay=0.005)

    # Add a small pause at the end
    time.sleep(0.5)

    # Separator after the banner
    print(f"\n{Fore.YELLOW}{'═' * 78}{Style.RESET_ALL}\n")


def clear_screen():
    """Clear the terminal screen"""
    print("\033[H\033[J", end="")


if __name__ == "__main__":
    # Test the banner if this file is run directly
    print_header()
