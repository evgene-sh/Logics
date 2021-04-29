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

# files = ['data/LevinMikenberg/LM_1_1.mvlog', 'data/LevinMikenberg/LM_1_4.mvlog']
logics = [parse(file) for file in files]

# print(*logics, sep='\n\n')

for l1, l2 in itertools.combinations(logics, 2):
    print(l1.name, l2.name, compare_logics(l1, l2))
