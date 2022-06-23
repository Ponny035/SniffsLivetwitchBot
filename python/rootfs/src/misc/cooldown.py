from src.misc import alldata
from src.timefn.timestamp import get_timestamp


# init variable
default_cooldown = 20


# get cooldown
def get_cooldown(command: str):
    match command:
        case "sr":
            return 120
        case "flip":
            return 5
        case _:
            return default_cooldown


def check_global(command: str):
    match command:
        case "uptime" | "discord" | "facebook" | "youtube" | "instagram" | "commands" | "np":
            return True
        case _:
            return False


# cooldown related system
def set_cooldown(username: str, command: str):
    now = get_timestamp()
    if check_global(command):
        try:
            alldata.command_cooldown["global"][command] = now
        except KeyError:
            alldata.command_cooldown["global"] = {}
            alldata.command_cooldown["global"][command] = now
    else:
        try:
            alldata.command_cooldown[username][command] = now
        except KeyError:
            alldata.command_cooldown[username] = {}
            alldata.command_cooldown[username][command] = now


def check_cooldown(username: str, command: str):
    cooldown = get_cooldown(command)
    if check_global(command):
        try:
            timestamp = alldata.command_cooldown["global"][command]
            now = get_timestamp()
            diff = (now - timestamp).total_seconds()
            if diff > cooldown:
                return True
            else:
                print(f"[INFO] [{get_timestamp()}] COOLDOWN: {username} COMMAND: {command} DURATION: {cooldown - diff}s")
                return False
        except KeyError:
            return True
    else:
        try:
            timestamp = alldata.command_cooldown[username][command]
            now = get_timestamp()
            diff = (now - timestamp).total_seconds()
            if diff > cooldown:
                return True
            else:
                print(f"[INFO] [{get_timestamp()}] COOLDOWN: {username} COMMAND: {command} DURATION: {cooldown - diff}s")
                return False
        except KeyError:
            return True
