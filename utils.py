import random

class ValidationException(Exception):
    pass

def rand_01():
    return random.randrange(2)