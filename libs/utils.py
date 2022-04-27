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


def check_auto_sync() -> bool:
    if os.path.exists("data/auto_sync"):
        with open("data/auto_sync", "rb") as f:
            auto_sync = pickle.load(f)
        return auto_sync
    else:
        return False


def set_auto_sync(value: bool) -> None:
    with open("data/auto_sync", "wb") as f:
        pickle.dump(value, f)


def auto_password(len: int, ascii=True, digits=True, special_chars=True) -> str:
    sample = (
        string.ascii_letters * ascii
        + string.digits * digits
        + string.punctuation * special_chars
    )
    if sample:
        random_pass = "".join(random.sample(sample, len))
    else:
        random_pass = ""
    return random_pass

def write_backup_failure(value: bool) -> None:
    with open("data/backup_failure.txt", "w") as f:
        f.write(str(value))

def is_backup_failure() -> bool:
    if os.path.exists("data/backup_failure.txt"):
        with open("data/backup_failure.txt", "r") as f:
            backup_failure = f.read()
        return backup_failure == "True"
    else:
        return False