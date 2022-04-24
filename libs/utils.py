import os.path, pickle

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


def set_dark_mode(dark_mode: bool, system=False) -> None:
    if os.path.exists("data/dark_mode"):
        with open("data/dark_mode", "rb") as f:
            _dict = pickle.load(f)
    else:
        _dict = {}
    if not "system_dark_mode" in _dict:
        _dict["system_dark_mode"] = False
    if not "dark_mode" in _dict:
        _dict["dark_mode"] = False
    _dict["system_dark_mode" if system else "dark_mode"] = dark_mode
    with open("data/dark_mode", "wb") as f:
        pickle.dump(_dict, f)
