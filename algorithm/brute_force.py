"""Алгоритмы анализа и сравнения логик"""

from algorithm.logic import TableFunction
import itertools


def compare_logics(logic1, logic2):
    if logic1.values != logic2.values:
        return 'non-comparable'

    dominance1 = check_dominance(logic1, logic2)
    dominance2 = check_dominance(logic2, logic1)

    if dominance1 and dominance2:
        return 'equivalent'
    elif dominance1:
        return 'embedded'
    elif dominance2:
        return 'embeds'
    else:
        return 'non-comparable'


def check_dominance(logic, logic2):
    # Проверка на неразличимость значений
    if not logic.eq_vals <= logic2.eq_vals:
        return False

    # ПРОВЕРКА ОЗ(4) ########################
    for length in range(1, len(logic.values)):
        for s in itertools.combinations(logic.values.keys(), length):
            is_closure = True
            for f in logic.functions:
                if not f.set_is_closure(s):
                    is_closure = False
                    break

            if is_closure:
                for g in logic2.functions:
                    if not g.set_is_closure(s):
                        return False
    #########################################

    # ПРОВЕРКА ОЗ(5) ########################
    if not logic.value_area >= logic2.value_area:
        return False

    closure_sets = []
    # поиск множеств значений, которое на всех функциях отображается в себя
    for length in range(1, len(logic.values)):
        for w in itertools.combinations(logic.values.keys(), length):
            is_closure = True
            for f in logic.functions + logic2.functions:
                if not f.set_is_closure(w):
                    is_closure = False
                    break
            if is_closure:
                closure_sets.append(set(w))

    found_functions = []
    for w in closure_sets:
        # поиск всех функций o, которые получают значения за пределами w
        for o in logic2.functions:
            if o.value_area > w:
                o_have_two_vals = False
                # проверка, что есть хотя-бы два значения: v1 o v2 -> not w
                for vs in itertools.permutations(o.value_area-w, o.dim):
                    if o(*vs) not in w:
                        o_have_two_vals = True
                        break
                if o_have_two_vals:
                    # o найдено. проверка набора функций для ее выведения
                    gs = list(filter(lambda g: g.value_area > w, logic.functions))
                    if sum(g.set_able_to_out(w) for g in gs) == 0:
                        if find_functions([o], gs):
                            found_functions.append(o)
                        else:
                            return False
    #########################################

    return find_functions(set(logic2.functions) - set(found_functions), logic.functions)


def find_functions(need_functions, have_functions):
    """Поиск нужных функций путем перебора композиций имеющихся"""
    new_functions, loop_functions = set(have_functions), set(have_functions)
    functions_need_to_find = set(need_functions)

    while len(loop_functions):
        temp_functions = set()

        for f in loop_functions:
            for g in new_functions:
                temp_functions.update(compose_functions(f, g))
                temp_functions.update(compose_functions(g, f))

        loop_functions = temp_functions - new_functions
        new_functions.update(temp_functions)

        if functions_need_to_find <= new_functions:
            return True

    return False


def compose_functions(f, g):
    """создание функций из всевозможных композиций f(g)"""
    if f.values != g.values:
        return set()

    tables = []

    if f.dim == 1 and g.dim == 1:
        tables.append(
            tuple(f(g(i)) for i in f.values.keys()))

    elif f.dim == 2 and g.dim == 2:
        tables.append(
            tuple(tuple(f(g(i, j), i) for j in f.values.keys()) for i in f.values.keys()))

        if not g.is_symmetric:
            tables.append(
                tuple(tuple(f(g(i, j), j) for j in f.values.keys()) for i in f.values.keys()))

        if not f.is_symmetric:
            tables.append(
                tuple(tuple(f(i, g(i, j)) for j in f.values.keys()) for i in f.values.keys()))

            if not g.is_symmetric:
                tables.append(
                    tuple(tuple(f(j, g(i, j)) for j in f.values.keys()) for i in f.values.keys()))

    elif f.dim == 1 and g.dim == 2:
        tables.append(
            tuple(tuple(f(g(i, j)) for j in f.values.keys()) for i in f.values.keys()))
        tables.append(
            tuple(f(g(i, i)) for i in f.values.keys()))

    elif f.dim == 2 and g.dim == 1:
        tables.append(
            tuple(tuple(f(g(i), j) for j in f.values.keys()) for i in f.values.keys()))

        if not f.is_symmetric:
            tables.append(
                tuple(tuple(f(i, g(j)) for j in f.values.keys()) for i in f.values.keys()))

        tables.append(
            tuple(tuple(f(g(i), g(j)) for j in f.values.keys()) for i in f.values.keys()))

    else:
        raise NotImplementedError('Пары функции таких размерностей не проработаны:' + str(f.dim) + str(g.dim))

    functions = set(
        map(lambda table: TableFunction('nameless', table, 2 if type(table[0]) == tuple else 1, f.values), tables))

    return functions

# TODO make the compose_functions to work with functions with any number of arguments
