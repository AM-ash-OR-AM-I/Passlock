import os.path, pickle, json
import string
import random

if not os.path.exists("data"):
    os.mkdir("data")


def auto_password(length: int, ascii=True, digits=True, special_chars=True) -> str:
    universe = ""
    password = ""
    if ascii:
        password += random.choice(string.ascii_letters)
        universe += string.ascii_letters
    if digits:
        universe += string.digits
        password += random.choice(string.digits)
    if special_chars:
        universe += string.punctuation
        password += random.choice(string.punctuation)

    rest = length - len(password)
    if universe == "":  # if all options are false
        return "Error: No options selected"
    for _ in range(rest):
        password += random.choice(universe)

    password = list(password)
    random.shuffle(password)
    password = "".join(password)
    return password


def load_passwords() -> dict:
    if os.path.exists("data/passwords"):
        with open("data/passwords", "rb") as f:
            encrypted_pass = pickle.load(f)
        return encrypted_pass
    else:
        return {}


def get_uid() -> str:
    with open("data/user_id.txt", "r") as f:
        uid = f.read()
    return uid


def write_passwords(dictionary: dict) -> None:
    with open("data/passwords", "wb") as f:
        pickle.dump(dictionary, f)


def remove_user_data() -> None:
    if os.path.exists("data/user_id.txt"):
        os.remove("data/user_id.txt")
    if os.path.exists("data/passwords"):
        os.remove("data/passwords")
    if os.path.exists("data/encrypted_file.txt"):
        os.remove("data/encrypted_file.txt")


def _get_config() -> dict:
    if os.path.exists("data/config.json"):
        with open("data/config.json", "r") as f:
            config = json.load(f)
        return config
    else:
        return {}


def get_email() -> str:
    if os.path.exists("data/email.txt"):
        with open("data/email.txt", "r") as f:
            email = f.read()
        return email
    else:
        return "DemoMail"


def get_primary_palette() -> str:
    if os.path.exists("data/config.json"):
        with open("data/config.json", "r") as f:
            config = json.load(f)
        return config.get("primary_palette", "DeepOrange")
    else:
        return "DeepOrange"


def is_dark_mode(system=False) -> bool:
    json_data = _get_config()
    return json_data.get("system_dark_mode" if system else "dark_mode", False)


def is_backup_failure() -> bool:
    _json_file = _get_config()
    return _json_file.get("backup_failure", False)


def is_extra_security() -> bool:
    _json_file = _get_config()
    return _json_file.get("extra_security", False)


def check_auto_sync() -> bool:
    json_data = _get_config()
    return json_data.get("auto_sync", False)
