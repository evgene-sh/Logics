"""Оптимизации при сравнении логик"""

from copy import copy
import itertools
import logging


class Transitivity:
    def __init__(self, logic_names):
        self.length = len(logic_names)
        self.names = dict([(name, num) for num, name in enumerate(logic_names)])
        self.relations = [[None] * self.length for _ in range(self.length)]

    def find_relation(self, relation, start_group):
        group = set(start_group)
        loop_group = copy(group)

        while len(loop_group):
            new_group = set()
            for i in loop_group:
                for j in range(self.length):
                    if self.relations[i][j] == relation:
                        new_group.add(j)
            loop_group = new_group - group
            group.update(new_group)

        return group

    def __call__(self, name1, name2):
        return self.relations[self.names[name1]][self.names[name2]]

    def update(self, name1, relation, name2):
        self.relations[self.names[name1]][self.names[name2]] = relation

        if relation == 'embeds':
            self.relations[self.names[name2]][self.names[name1]] = 'embedded'
        elif relation == 'embedded':
            self.relations[self.names[name2]][self.names[name1]] = 'embeds'
        else:
            self.relations[self.names[name2]][self.names[name1]] = relation

        if relation in ('embeds', 'embedded'):
            if relation == 'embedded':
                dominants, slaves = {self.names[name1]}, {self.names[name2]}
            else:
                dominants, slaves = {self.names[name2]}, {self.names[name1]}

            dominants = self.find_relation('embeds', dominants)
            slaves = self.find_relation('embedded', slaves)

            for d, s in itertools.product(dominants, slaves):
                self.relations[d][s] = 'embedded'
                self.relations[s][d] = 'embeds'

        elif relation == 'equivalent':
            eq_name1 = self.find_relation('equivalent', {self.names[name1]})
            eq_name2 = self.find_relation('equivalent', {self.names[name2]})
            for i, j in itertools.product(eq_name1, eq_name2):
                self.relations[i][j] = 'equivalent'
                self.relations[j][i] = 'equivalent'


def indiscernible_of_values(logic1, logic2):
    if logic1.eq_vals <= logic2.eq_vals:
        return True

    logging.debug('values {} are discernible in {}, indiscernible in {}'.format(
        logic1.eq_vals - logic2.eq_vals, logic2.name, logic1.name))
    return False


def embedding_of_value_area(logic1, logic2):
    if logic1.value_area >= logic2.value_area:
        return True

    logging.debug('{} returns {} not generated in {}'.format(
        logic2.name, logic2.value_area - logic1.value_area, logic1.name))
    return False


# ПРОВЕРКА ОЗ(4) ########################
def closure_sets(logic1, logic2):
    for length in range(1, len(logic1.values)):
        for w in itertools.combinations(logic1.values.keys(), length):
            is_closure = True
            for f in logic1.functions:
                if not f.set_is_closure(w):
                    is_closure = False
                    break

            if is_closure:
                for g in logic2.functions:
                    if not g.set_is_closure(w):
                        logging.debug('function {} in {} cannot be constructed in {}'.format(
                            g.name, logic2.name, logic1.name))
                        return False
    return True


# ПРОВЕРКА ОЗ(5) ########################
def sets_w(logic1, logic2, find):
    closure_sets = set()

    # выбор таких оз, которые замкнуты для всех f из logic1
    for w in set(map(lambda x: frozenset(x.value_area), logic1.functions)):
        is_closure = True
        for f in logic1.functions:
            if not f.set_is_closure(w):
                is_closure = False
                break
        if is_closure:
            closure_sets.add(w)

    found_functions = []
    # перебор вариантов для каждой искомой o
    for o in logic2.functions:
        o_closure = list(filter(lambda x: o.value_area > x, closure_sets))

        if len(o_closure) == 0:
            continue

        # исключение вложенных w
        for i in range(len(o_closure)):
            for j in range(i+1, len(o_closure)):
                if o_closure[i] >= o_closure[j]:
                    o_closure[j] = None
                elif o_closure[i] < o_closure[j]:
                    o_closure[i] = None
                    break

        can, tried_funcs = False, []
        for w in tuple(filter(lambda x: x is not None, o_closure)):
            funcs_w = tuple(filter(lambda x: x.value_area > w, logic1.functions))
            need = find([o], funcs_w)
            if len(need) == 0:
                found_functions.append(o)
                can = True
                break
            tried_funcs.extend(list(map(lambda x: x.name, funcs_w)))

        if not can:
            logging.debug('function {} in {} cannot be constructed in the basis {} of {}'.format(
                o.name, logic2.name, tried_funcs, logic1.name
            ))
            return None

    return found_functions
