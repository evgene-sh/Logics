"""Алгоритмы анализа и сравнения логик"""

from algorithm.logic import TableFunction
from algorithm.optimizations import value_area_1, value_area_2
import logging


def compare_logics(logic1, logic2, brute_force):
    if logic1.values != logic2.values:
        return 'non-comparable'

    dominance1 = check_dominance(logic1, logic2, brute_force)
    dominance2 = check_dominance(logic2, logic1, brute_force)

    if dominance1 and dominance2:
        return 'equivalent'
    elif dominance1:
        return 'embedded'
    elif dominance2:
        return 'embeds'
    else:
        return 'non-comparable'


def check_dominance(logic1, logic2, brute_force):
    logging.debug('\033[34m' + logic1.name + ' над ' + logic2.name + '\033[37m')

    # Проверка на неразличимость значений
    if not logic1.eq_vals <= logic2.eq_vals:
        return False

    # Проверка области отображения
    if not logic1.value_area >= logic2.value_area:
        return False

    # ПРОВЕРКА ОЗ(4) ########################
    if not value_area_1(logic1, logic2):
        return False

    # ПРОВЕРКА ОЗ(5) ########################
    found = value_area_2(logic1, logic2, brute_force)
    if found is False:
        return False

    return brute_force(set(logic2.functions) - set(found), logic1.functions)


################### первый переборочный алгоритм ###################


def find_functions(need_functions, have_functions):
    """Поиск нужных функций путем перебора композиций имеющихся"""
    checked, to_check = set(have_functions), set(have_functions)
    need = set(need_functions) - checked

    cnt = 0
    while len(to_check):
        logging.debug('    Повтор: ' + str(cnt) + '    новых: ' + str(len(to_check)))
        cnt += 1

        new = set()

        for f in to_check:
            for g in checked:
                new.update(compose_functions(f, g))
                if g not in to_check:
                    new.update(compose_functions(g, f))

                need -= new
                if len(need) == 0:
                    return True

        to_check = new - checked
        checked.update(to_check)

    return False


def compose_functions(f, g):
    """создание функций из всевозможных композиций f(g)"""
    if f.values != g.values:
        return set()

    tables = []
    values = tuple(f.values.keys())

    if f.dim == 1:
        if g.dim == 1:
            tables.append(
                tuple(f(g(i)) for i in values))

        else:  # g.dim == 2
            tables.append(
                tuple(tuple(f(g(i, j)) for j in values) for i in values))
            tables.append(
                tuple(f(g(i, i)) for i in values))

    else:  # f.dim == 2
        if g.dim == 1:
            tables.append(
                tuple(tuple(f(g(i), j) for j in values) for i in values))
            tables.append(
                tuple(tuple(f(i, g(j)) for j in values) for i in values))
            tables.append(
                tuple(tuple(f(g(i), g(j)) for j in values) for i in values))

        else:  # g.dim == 2
            if f == g:
                tables.append(
                    tuple(tuple(f(i, i) for j in values) for i in values))
                tables.append(
                    tuple(tuple(f(j, j) for j in values) for i in values))
                if not f.is_symmetric:
                    tables.append(
                        tuple(tuple(f(j, i) for j in values) for i in values))

            tables.append(
                tuple(tuple(f(g(i, j), g(i, j)) for j in values) for i in values))
            tables.append(
                tuple(tuple(f(g(i, j), i) for j in values) for i in values))
            tables.append(
                tuple(tuple(f(g(i, j), j) for j in values) for i in values))

    functions = set(
        map(lambda table: TableFunction(table, f.values), tables))

    return functions


################### второй переборочный алгоритм ###################


def find_functions2(need_functions, have_functions):
    vals = set()
    for f in have_functions:
        vals.update(f.value_area)

    checked, to_check = set(), set()
    need = set(filter(lambda f: f.dim == 2, need_functions))
    for uno in filter(lambda f: f.dim == 1, need_functions):
        need.add(TableFunction(
            tuple(tuple(uno(i) for j in have_functions[0].values.keys()) for i in have_functions[0].values.keys()),
            have_functions[0].values
        ))

    to_check.add(TableFunction(
        tuple(tuple(i for j in have_functions[0].values.keys()) for i in have_functions[0].values.keys()),
        have_functions[0].values
    ))
    to_check.add(TableFunction(
        tuple(tuple(j for j in have_functions[0].values.keys()) for i in have_functions[0].values.keys()),
        have_functions[0].values
    ))

    for v in vals:
        to_check.add(TableFunction(
            tuple(tuple(v for j in have_functions[0].values.keys()) for i in have_functions[0].values.keys()),
            have_functions[0].values
        ))

    checked.update(to_check)

    cnt = 0
    while len(to_check):
        logging.debug('    Повтор: ' + str(cnt) + '    новых: ' + str(len(to_check)))
        cnt += 1

        new = set()

        for k in to_check:
            for p in checked:
                new.update(compose_functions2(k, p, have_functions))
                need -= new
                if len(need) == 0:
                    return True

        to_check = new - checked
        checked.update(to_check)

    return False


def compose_functions2(k, p, base):
    tables = []

    for operation in base:
        if operation.dim == 1:
            compose_1d_operation(k, operation, tables)
        else:  # operator.dim == 2
            compose_2d_operation(k, p, operation, tables, not operation.is_symmetric and k != p)

    return set(map(lambda table: TableFunction(table, k.values), tables))


def compose_1d_operation(f, operation, tables):
    tables.append(
        tuple(tuple(operation(f(i, j)) for j in f.values.keys()) for i in f.values.keys()))


def compose_2d_operation(f, g, operation, tables, reflection):
    tables.append(
        tuple(tuple(operation(f(i, j), g(i, j)) for j in f.values.keys()) for i in f.values.keys()))
    if reflection:
        compose_2d_operation(g, f, operation, tables, False)

# TODO make the compose_functions to work with functions with any number of arguments
