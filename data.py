from cryptography.fernet import Fernet
import word_list_generator as word_list
import json
import os


# --- Profile Data ---

profile_data = None
current_game = None
game_data = None

with open("profile.json", "r") as profile_f:
    profile_data = json.loads(profile_f.read())

def load_profile(type):
    global game_data, current_game
    game_data = profile_data[type]
    current_game = type

def update_profile(word_type, val):
    game_data[word_type] = val
    save_profile()

def save_profile():
    profile_data[current_game] = game_data

    with open("profile.json", "w") as profile_f:
        profile_f.write(json.dumps(profile_data))


# --- Statistics Data ---

# build data

data = {
    "coins" : 0,
    "wordle_basic" : {}
}

for i in range(3, 13):
    data["wordle_basic"][i] = {
            "streak" : 0,
            "high_streak" : 0,
            "time" : None
            }

def encrypt_data():
    # save key
    key = Fernet.generate_key()
    with open("filekey.key", "wb") as f:
        f.write(key)

    fernet = Fernet(key)

    # read in binary
    with open("data.json", 'rb') as json_f:
        binary_data = json_f.read()

    # encrypt
    encrypted_data = fernet.encrypt(binary_data)

    # replace data
    with open("data.json", "wb") as json_f:
        json_f.write(encrypted_data)


def load_data():
    global data
    data_presence_check()
    # load key
    with open("filekey.key", "rb") as key_f:
        key = key_f.read()

    fernet = Fernet(key)

    # read encrypted data
    with open("data.json", "rb") as json_f:
        encrypted_data = json_f.read()

    # decrypt
    decrypted_data = fernet.decrypt(encrypted_data).decode("utf-8") 

    # parse decrypted json into dictionary
    data = json.loads(decrypted_data)


def save_data():
    data_presence_check()
    # write dict to json
    json_data = json.dumps(data)
    with open("data.json", "wb") as json_f:
        json_f.write(json_data.encode("utf-8"))

    encrypt_data()


def data_presence_check():
    # check if file exists
    if not (os.path.exists("data.json")):
        json_data = json.dumps(data)
        with open("data.json", "wb") as json_f:
            json_f.write(json_data.encode("utf-8"))

        encrypt_data()


data_presence_check()