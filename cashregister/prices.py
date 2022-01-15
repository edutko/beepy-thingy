import math
import random

RNG = random.Random()


def random_price():
    return math.floor(RNG.random() * 10) + 0.99
