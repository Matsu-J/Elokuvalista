from random import randint
from flask import session

def random_greeting():
    if session["username"]:
        user = session["username"]
    else:
        user = ""

    messages = [
        f"Tervetuloa {user}",
        f"Hei, {user}! Mitäs tänään katsottaisiin?",
        f"Hyvää huomenta, päivää, iltaa tai milloin tätä käytätkään {user}",
        f"Heimoi {user}",
        f"Hello there {user}!"
    ]
    random_number = randint(0, len(messages)-1)
    return messages[random_number]