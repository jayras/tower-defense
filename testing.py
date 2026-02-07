from game.settings import GameSettings

def log(prefix: str, message: str):
    if GameSettings.debug:
        print(f"{prefix}: {message}")


