"""Алгоритмы анализа и сравнения логик"""

from logic import TableFunction


def compare_logics(logic1, logic2):
    if logic1.values != logic2.values:
        return 'non-comparable'

    dominance1 = set(logic2.functions) <= generate_functions_of_logic(logic1)
    dominance2 = set(logic1.functions) <= generate_functions_of_logic(logic2)

    if dominance1 and dominance2:
        return 'equivalent'
    elif dominance1:
        return 'embedded'
    elif dominance2:
        return 'embeds'
    else:
        return 'non-comparable'


def generate_functions_of_logic(logic):
    new_functions, loop_functions = set(logic.functions),  set(logic.functions)

    while len(loop_functions):
        temp_functions = set()

        for f in loop_functions:
            for g in new_functions:
                temp_functions.update(compose_functions(f, g))

        loop_functions = temp_functions - new_functions
        new_functions.update(temp_functions)

    return new_functions


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

        tables.append(
            tuple(tuple(f(g(i, j), j) for j in f.values.keys()) for i in f.values.keys()))

        tables.append(
            tuple(tuple(f(i, g(i, j)) for j in f.values.keys()) for i in f.values.keys()))

        tables.append(
            tuple(tuple(f(j, g(i, j)) for j in f.values.keys()) for i in f.values.keys()))

    elif f.dim == 1 and g.dim == 2:
        tables.append(
            tuple(tuple(f(g(i, j)) for j in f.values.keys()) for i in f.values.keys()))

    elif f.dim == 2 and g.dim == 1:
        tables.append(
            tuple(tuple(f(g(i), i) for j in f.values.keys()) for i in f.values.keys()))

        tables.append(
            tuple(tuple(f(i, g(j)) for j in f.values.keys()) for i in f.values.keys()))

        tables.append(
            tuple(tuple(f(g(i), g(j)) for j in f.values.keys()) for i in f.values.keys()))

    else:
        raise NotImplementedError('Пары функции таких размерностей не проработаны:' + str(f.dim) + str(g.dim))

    functions = set(map(lambda table: TableFunction('nameless', table, max(f.dim, g.dim), f.values), tables))

    return functions

# TODO make the compose_functions to work with functions with any number of arguments
