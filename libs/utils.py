import os.path, pickle

def load_passwords() -> dict:
    if os.path.exists("data/password"):
        with open("data/password", "rb") as f:
            encrypted_pass = pickle.load(f)
        return encrypted_pass
    else:
        return {}

def get_uid() -> str:
    with open("data/user_id.txt","r") as f:
        uid = f.read()
    return uid

def write_passwords(dictionary: dict) -> None:
    with open("data/password", "wb") as f:
        pickle.dump(dictionary, f)