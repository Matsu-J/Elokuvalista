from random import randint
from flask import session

def random_greeting():
    try:
        if session["username"]:
            user = session["username"]
            messages = [
                        f"Tervetuloa {user}",
                        f"Hei, {user}! Mitäs tänään katsottaisiin?",
                        f"Hyvää huomenta, päivää, iltaa tai milloin tätä käytätkään {user}",
                        f"Heimoi {user}",
                        f"Hello there {user}!",
                        f"Oh look, it's {user}",
                        f"Good to see you {user}"
                    ]
    except:
        messages = [
                    f"Tervetuloa",
                    f"Hei! Mitäs tänään katsottaisiin?",
                    f"Hyvää huomenta, päivää, iltaa tai milloin tätä käytätkään",
                    f"Heimoi",
                    f"Hello there!",
                    "Good to see you"
                    ]

    
    random_number = randint(0, len(messages)-1)
    return messages[random_number]