from mvlog import Mvlog
from logic import Logic
from brute_force import *
from sys import getsizeof as gs
import numpy as np


def parse(path):
    mvlog = Mvlog(path)
    return Logic(mvlog)


klini = parse('data/Klini.mvlog')
print(klini)


# TODO create functional generating all functions of a logic
