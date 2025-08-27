import random 
import string
import numbers

def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))

def random_age() -> int:
    return random.randint(1, 100)

def random_sexe():
    sexes = ["M", "F"]
    return random.choice(sexes)