import os.path, pickle
import string
import random

if not os.path.exists("data"):
    os.mkdir("data")


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


def is_dark_mode(system=False) -> bool:
    if os.path.exists("data/dark_mode"):
        with open("data/dark_mode", "rb") as f:
            dark_mode = pickle.load(f)
        return dark_mode["system_dark_mode" if system else "dark_mode"]
    else:
        return False


def set_dark_mode(app: bool, system: bool) -> None:
    if os.path.exists("data/dark_mode"):
        with open("data/dark_mode", "rb") as f:
            _dict = pickle.load(f)
    else:
        _dict = {}
    _dict["system_dark_mode"] = system
    _dict["dark_mode"] = app
    with open("data/dark_mode", "wb") as f:
        pickle.dump(_dict, f)

def auto_password(len: str, ascii = True, digits = True, special_char = True) -> str:
    sample = string.ascii_letters*ascii + string.digits*digits + string.punctuation*special_char
    random_pass = "".join(random.sample(sample, int(len)))
    return random_pass