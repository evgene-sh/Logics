from algorithm.mvlog import Mvlog
from algorithm.logic import Logic
from algorithm.brute_force import compare_logics, find_functions, find_functions2
import itertools
import os
from sys import argv
from algorithm.optimizations import Transitivity
import logging
from math import factorial


def parse(path):
    """Получение логики из mvlog-файла"""
    mvlog = Mvlog(path)
    return Logic(mvlog)


def get_logics(path):
    """Получение всех логик из директории"""
    files = tuple(map(lambda x: path + x, os.listdir(path)))
    return [parse(file) for file in files]


def algorithm(input_path, output_path=None):
    """Основной алгоритм"""
    logics = get_logics(input_path)

    transitivity = Transitivity([l.name for l in logics])

    count_of_pairs, iteration = int(factorial(len(logics))/(2*factorial((len(logics)-2)))), 0
    for l1, l2 in itertools.combinations(logics, 2):
        iteration += 1
        logging.info(' '.join(['Проверка', str(iteration), 'из', str(count_of_pairs), ':', l1.name, '&', l2.name]))

        if not transitivity(l1.name, l2.name):
            result = compare_logics(l1, l2, find_functions)
            transitivity.update(l1.name, result, l2.name)

    if output_path is not None:
        with open(argv[2] + argv[1].split('/')[-2] + '.csv', 'w') as file:
            file.write(','.join(('logic1_name', 'logic2_name', 'relation')) + '\n')
            for name1, name2 in itertools.permutations(sorted([l.name for l in logics], key=lambda x: (len(x), x)), 2):
                file.write(','.join([name1, name2, transitivity(name1, name2)]) + '\n')

    return ((name1, name2, transitivity(name1, name2))
            for name1, name2 in itertools.permutations(sorted([l.name for l in logics], key=lambda x: (len(x), x)), 2))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    if len(argv) not in (2, 3):
        raise TypeError('Неверное число аргументов')

    results = algorithm(*argv[1:])

    if len(argv) == 2:
        for res in results:
            print(res[0], res[1], ':', res[2])
