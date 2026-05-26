DEBUG = False

def log(*args, **kwargs):
    if DEBUG:
        print("[DEBUG]", *args, **kwargs)