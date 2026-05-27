DEBUG = True
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'

def log(string):
    if DEBUG:
        print(f"{BOLD}{CYAN}[DEBUG]{RESET} {string}")