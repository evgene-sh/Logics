from mvlog import Mvlog
from logic import Logic
from brute_force import *


def parse(path):
    mvlog = Mvlog(path)
    return Logic(mvlog)


klini = parse('data/Klini.mvlog')

functions = generate_functions_of_logic(klini)
print(*functions, sep='\n')

# print(compare_logics(klini, klini))
