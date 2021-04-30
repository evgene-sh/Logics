from mvlog import Mvlog
from logic import Logic
from brute_force import compare_logics
import itertools
import os
from sys import argv


def parse(path):
    """Получение логики из mvlog-файла"""
    mvlog = Mvlog(path)
    return Logic(mvlog)


def get_logics(path):
    """Получение всех логик из директории"""
    files = tuple(map(lambda x: path + x, os.listdir(path)))
    return [parse(file) for file in files]


def algorithm(path):
    """Основной алгоритм"""
    logics = get_logics(path)

    for l1, l2 in itertools.combinations(logics, 2):
        yield l1.name, l2.name, compare_logics(l1, l2)


if __name__ == '__main__':
    for res in algorithm(argv[1]):
        print(res[0], res[1], ':', res[2])

