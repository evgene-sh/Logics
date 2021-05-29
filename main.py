from algorithm.mvlog import Mvlog
from algorithm.logic import Logic
from algorithm.logic_comparison import AsymmetricComparator, SymmetricComparator, AggregatedComparator
import itertools
import os
from sys import argv
from algorithm.optimizations import Transitivity
import logging
from math import factorial
from tqdm import tqdm
from visualization import draw_graph
import argparse


DATA_PATH = 'data/'
RESULTS_PATH = 'results/'


def parse(path):
    """Получение логики из mvlog-файла"""
    mvlog = Mvlog(path)
    return Logic(mvlog)


def get_logics(path):
    """Получение всех логик из директории"""
    files = tuple(map(lambda x: path + x, os.listdir(path)))
    return [parse(file) for file in files]


def algorithm(input_dir, need_csv, need_dot, comparator_class=AsymmetricComparator):
    """Основной алгоритм"""
    input_path = DATA_PATH + input_dir + '/'
    output_path = RESULTS_PATH + input_dir

    logics = get_logics(input_path)
    compare = comparator_class()
    transitivity = Transitivity([l.name for l in logics])

    cnt_pairs = int(factorial(len(logics))/(2*factorial((len(logics)-2))))
    for l1, l2 in tqdm(itertools.combinations(logics, 2),
                       total=cnt_pairs, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} {elapsed}'):
        if not transitivity(l1.name, l2.name):
            result = compare(l1, l2)
            transitivity.update(l1.name, result, l2.name)

    # csv output
    if need_csv:
        with open(output_path+'.csv', 'w') as file:
            file.write(','.join(('logic1_name', 'logic2_name', 'relation')) + '\n')
            for name1, name2 in itertools.permutations(sorted([l.name for l in logics], key=lambda x: (len(x), x)), 2):
                file.write(','.join([name1, name2, transitivity(name1, name2)]) + '\n')

    # dot output
    if need_dot:
        draw_graph(transitivity, output_path)

    return ((name1, name2, transitivity(name1, name2))
            for name1, name2 in itertools.combinations(sorted([l.name for l in logics], key=lambda x: (len(x), x)), 2))


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('input', help='name of dir in DATA_PATH with mvlog files')
    argparser.add_argument('-csv', action='store_true', default=False, help='if you need to generate csv file')
    argparser.add_argument('-dot', action='store_true', default=False, help='if you need to generate dot file')

    args = argparser.parse_args()

    logging.basicConfig(
        format='%(asctime)s %(levelname)s: %(message)s',
        level=logging.DEBUG,
        filename='debug.log',
        filemode='w',
        datefmt='%H:%M:%S'
    )

    results = algorithm(args.input, args.csv, args.dot)

    # if len(argv) == 2:
    #     for res in results:
    #         print(res[0], res[1], ':', res[2])
