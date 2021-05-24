"""Алгоритмы анализа и сравнения логик"""

from algorithm.logic import TableFunction
from algorithm.optimizations import value_area_1, value_area_2
import logging


def compare_logics(logic1, logic2, brute_force):
    """Определение отношения между двумя логиками"""
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
    """Проверка, доминирует ли logic1 над logic2"""
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
    if found is None:
        return False

    return brute_force(set(logic2.functions) - set(found), logic1.functions)


################### первый переборочный алгоритм ###################


def find_functions(need_functions, have_functions):
    """Поиск нужных функций путем перебора композиций имеющихся"""
    checked, to_check = set(have_functions), set(have_functions)
    need = set(need_functions) - checked

    have_2d = list(filter(lambda o: o.dim == 2, have_functions))

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

        # Добавление идей второго алгоритма ###########
        # for f in to_check:
        #     for g in checked:
        #         for o in have_2d:
        #             new.add(compose_functions2(f, g, o))
        #             if g not in to_check and not o.is_symmetric:
        #                 new.add(compose_functions2(f, g, o))
        #
        #         need -= new
        #         if len(need) == 0:
        #             return True
        ###############################################

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

    return map(lambda table: TableFunction(table, f.values), tables)


################### второй переборочный алгоритм ###################


def find_functions2(need_functions, have_functions):
    values = tuple(have_functions[0].values.keys())
    value_area = set()
    for f in have_functions:
        value_area.update(f.value_area)

    base_1d = tuple(filter(lambda o: o.dim == 1, have_functions))
    base_2d = tuple(filter(lambda o: o.dim == 2, have_functions))

    checked, to_check = set(), set()
    need = set(filter(lambda f: f.dim == 2, need_functions))
    for uno in filter(lambda f: f.dim == 1, need_functions):
        need.add(TableFunction(
            tuple(tuple(uno(i) for j in values) for i in values),
            have_functions[0].values
        ))

    to_check.add(TableFunction(
        tuple(tuple(i for j in values) for i in values),
        have_functions[0].values
    ))
    to_check.add(TableFunction(
        tuple(tuple(j for j in values) for i in values),
        have_functions[0].values
    ))
    for v in value_area:
        to_check.add(TableFunction(
            tuple(tuple(v for j in values) for i in values),
            have_functions[0].values
        ))

    checked.update(to_check)

    cnt = 0
    while len(to_check):
        logging.debug('    Повтор: ' + str(cnt) + '    новых: ' + str(len(to_check)))
        cnt += 1

        new = set()

        for k in to_check:
            for o in base_1d:
                new.add(TableFunction(
                    tuple(tuple(o(k(i, j)) for j in values) for i in values),
                    have_functions[0].values))

            for p in checked:
                for o in base_2d:
                    new.add(TableFunction(
                        tuple(tuple(o(k(i, j), p(i, j)) for j in values) for i in values),
                        have_functions[0].values))
                    if not o.is_symmetric and p not in to_check:
                        new.add(TableFunction(
                            tuple(tuple(o(p(i, j), k(i, j)) for j in values) for i in values),
                            have_functions[0].values))

                need -= new
                if len(need) == 0:
                    return True

        to_check = new - checked
        checked.update(to_check)

    return False


def compose_functions2(f, g, o):

    if f.dim == 2 and g.dim == 2:
        table = tuple(tuple(o(f(i, j), g(i, j)) for j in f.values.keys()) for i in f.values.keys())
    elif f.dim == 2 and g.dim == 1:
        table = tuple(tuple(o(f(i, j), g(j)) for j in f.values.keys()) for i in f.values.keys())
    elif f.dim == 1 and g.dim == 2:
        table = tuple(tuple(o(f(i), g(i, j)) for j in f.values.keys()) for i in f.values.keys())
    else:
        table = tuple(tuple(o(f(i), g(j)) for j in f.values.keys()) for i in f.values.keys())

    return TableFunction(table, f.values)
