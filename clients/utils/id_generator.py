import random

def generate_unique_id(prefix: str):
    number = random.randint(10000000, 99999999)
    return f"{prefix}-{number}"