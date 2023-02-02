import random
import json

def generate(lenghtcap:int = 16):
    with open("usernames/firstnames.json", "r", encoding='utf-8') as f:
        fn = json.load(f)
    with open("usernames/lastnames.json", "r", encoding='utf-8') as f:
        ln = json.load(f)

    first = random.choice(fn)
    last = random.choice(ln)

    username = first

    n = random.randint(0, 10)
    if n == 5:
        username = f"_{username}"

    n = random.randint(0, 1)
    if n == 1:
        username = f"{username}_"
    
    username = f"{username}{last}{str(random.randint(0, 999))}"

    if "-" in username:
        username = username.replace("-", "_")

    username = username[:lenghtcap]

    n = random.randint(0, 1)
    if n == 1:
        return username.lower(), f"{first} {last}"
    else:
        return username.lower(), first
