import numpy as np
from logic import TableFunction


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
    if f.values != g.values:
        return set()

    tables = []

    if f.dim == 1 and g.dim == 1:
        tables.append(
            np.array([bytes(f(g(i)), 'utf-8') for i in f.values.keys()]))

    elif f.dim == 2 and g.dim == 2:
        tables.append(
            np.array([[bytes(f(g(i, j), i), 'utf-8') for j in f.values.keys()] for i in f.values.keys()]))

        tables.append(
            np.array([[bytes(f(g(i, j), j), 'utf-8') for j in f.values.keys()] for i in f.values.keys()]))

        tables.append(
            np.array([[bytes(f(i, g(i, j)), 'utf-8') for j in f.values.keys()] for i in f.values.keys()]))

        tables.append(
            np.array([[bytes(f(j, g(i, j)), 'utf-8') for j in f.values.keys()] for i in f.values.keys()]))

    elif f.dim == 1 and g.dim == 2:
        tables.append(
            np.array([[bytes(f(g(i, j)), 'utf-8') for j in f.values.keys()] for i in f.values.keys()]))

    elif f.dim == 2 and g.dim == 1:
        tables.append(
            np.array([[bytes(f(g(i), j), 'utf-8') for j in f.values.keys()] for i in f.values.keys()]))

        tables.append(
            np.array([[bytes(f(i, g(j)), 'utf-8') for j in f.values.keys()] for i in f.values.keys()]))

        tables.append(
            np.array([[bytes(f(g(i), g(j)), 'utf-8') for j in f.values.keys()] for i in f.values.keys()]))

    else:
        raise NotImplementedError('Пары функции таких размерностей не проработаны:' + str(f.dim) + str(g.dim))

    functions = set(map(lambda table: TableFunction('nameless', table, max(f.dim, g.dim), f.values), tables))

    return functions

# TODO make the compose_functions to work with functions with any number of arguments
