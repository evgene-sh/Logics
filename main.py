from mvlog import Mvlog
from logic import Logic
from brute_force import *
import itertools
import os


def parse(path):
    mvlog = Mvlog(path)
    return Logic(mvlog)


path = 'data/LevinMikenberg/'
files = tuple(map(lambda x: path + x, os.listdir(path)))

logics = [parse(file) for file in files]

# print(*logics, sep='\n\n')


from time import perf_counter

start = perf_counter()
for l1, l2 in itertools.combinations(logics, 2):
    print(l1.name, l2.name, compare_logics(l1, l2))
print(perf_counter()-start)
