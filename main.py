from algorithm.mvlog import Mvlog
from algorithm.logic import Logic
from algorithm.brute_force import compare_logics
import itertools
import os
from sys import argv
from algorithm.optimizations import Transitivity


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

    transitivity = Transitivity([l.name for l in logics])

    for l1, l2 in itertools.combinations(logics, 2):

        if transitivity(l1.name, l2.name):
            result = transitivity(l1.name, l2.name)

        else:
            result = compare_logics(l1, l2)
            transitivity.update(l1.name, result, l2.name)

        yield l1.name, l2.name, result


if __name__ == '__main__':
    for res in algorithm(argv[1]):
        print(res[0], res[1], ':', res[2])
