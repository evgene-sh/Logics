from algorithm.structures.mvlog import Mvlog
from algorithm.structures.logic import Logic
from algorithm.logic_comparison import AsymmetricComparator, SymmetricComparator, AggregatedComparator
import itertools
import os
from algorithm.optimizations import Transitivity
import logging
from math import factorial
from tqdm import tqdm
from algorithm.visualization import draw_graph
import argparse
from collections import defaultdict


DATA_PATH = 'data/'
RESULTS_PATH = 'results/'
EXTERNAL_PATH = 'external/'
SEPARATOR = ' '


def parse(path):
    """Получение логики из mvlog-файла"""
    mvlog = Mvlog(path)
    return Logic(mvlog)


def get_logics(path):
    """Получение всех логик из директории"""
    files = tuple(map(lambda x: path + x, os.listdir(path)))
    return [parse(file) for file in files]


def fill_transitivity(known, transitivity):
    with open(EXTERNAL_PATH + known + '.csv', 'r') as f:
        next(f)
        non_final_result = defaultdict(lambda: (None, None))
        for line in f:
            logic1, logic2, verdict = line.replace('\n', '').split(SEPARATOR)
            if not transitivity(logic1, logic2):

                if verdict == 'not-embeds':
                    dominance = non_final_result[logic1 + logic2]
                    if dominance[1] is None:
                        non_final_result[logic1 + logic2] = (dominance[0], False)
                    else:
                        raise ValueError('Logical mistake in the input csv file: {} {} : {}'.format(logic1, logic2, verdict))

                elif verdict == 'is-embeds':
                    dominance = non_final_result[logic1 + logic2]
                    if dominance[1] is None:
                        non_final_result[logic1 + logic2] = (dominance[0], True)
                    else:
                        raise ValueError(
                            'Logical mistake in the input csv file: {} {} : {}'.format(logic1, logic2, verdict))

                elif verdict == 'not-embedded':
                    dominance = non_final_result[logic1 + logic2]
                    if dominance[0] is None:
                        non_final_result[logic1 + logic2] = (False, dominance[1])
                    else:
                        raise ValueError(
                            'Logical mistake in the input csv file: {} {} : {}'.format(logic1, logic2, verdict))

                elif verdict == 'is-embedded':
                    dominance = non_final_result[logic1 + logic2]
                    if dominance[0] is None:
                        non_final_result[logic1 + logic2] = (True, dominance[1])
                    else:
                        raise ValueError(
                            'Logical mistake in the input csv file: {} {} : {}'.format(logic1, logic2, verdict))

                else:
                    transitivity.update(logic1, verdict, logic2)
    return non_final_result


def algorithm(input_dir, need_csv, need_dot, comparator_class=AsymmetricComparator, known=False):
    """Основной алгоритм"""

    input_path = DATA_PATH + input_dir + '/'
    output_path = RESULTS_PATH + input_dir

    logics = get_logics(input_path)
    compare = comparator_class()
    transitivity = Transitivity([l.name for l in logics])

    non_final_result = defaultdict(lambda: (None, None))  # for using -know key
    if known:
        non_final_result = fill_transitivity(known, transitivity)

    cnt_pairs = int(factorial(len(logics))/(2*factorial((len(logics)-2))))
    for l1, l2 in tqdm(itertools.combinations(logics, 2),
                       total=cnt_pairs, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} {elapsed}'):
        if not transitivity(l1.name, l2.name):
            d1, d2 = non_final_result[l1.name+l2.name]
            result = compare(l1, l2, dominance1=d1, dominance2=d2)
            transitivity.update(l1.name, result, l2.name)

    # csv output
    if need_csv:
        with open(output_path+'.csv', 'w') as file:
            file.write(SEPARATOR.join(('logic1_name', 'logic2_name', 'relation')) + '\n')
            for name1, name2 in itertools.permutations(sorted([l.name for l in logics], key=lambda x: (len(x), x)), 2):
                file.write(SEPARATOR.join([name1, name2, transitivity(name1, name2)]) + '\n')

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
    argparser.add_argument('-aggr', action='store_true', default=False, help='if you want to run AggregatedComparator')
    argparser.add_argument('-know', nargs='?', default=False, help='csv file with known results')

    args = argparser.parse_args()

    logging.basicConfig(
        format='%(asctime)s %(levelname)s: %(message)s',
        level=logging.DEBUG,
        filename='debug.log',
        filemode='w',
        datefmt='%H:%M:%S'
    )

    for res in algorithm(args.input, args.csv, args.dot, AggregatedComparator if args.aggr else AsymmetricComparator, args.know):
        print(res[0], res[1], ':', res[2])
