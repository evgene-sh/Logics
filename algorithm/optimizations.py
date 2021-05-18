from copy import copy
import itertools


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


def value_area_1(logic1, logic2):
    for length in range(1, len(logic1.values)):
        for s in itertools.combinations(logic1.values.keys(), length):
            is_closure = True
            for f in logic1.functions:
                if not f.set_is_closure(s):
                    is_closure = False
                    break

            if is_closure:
                for g in logic2.functions:
                    if not g.set_is_closure(s):
                        return False
    return True


def value_area_2(logic1, logic2, find):
    closure_sets = []
    # поиск множеств значений, которое на всех функциях отображается в себя
    for length in range(1, len(logic1.values)):
        for w in itertools.combinations(logic1.values.keys(), length):
            is_closure = True
            for f in logic1.functions + logic2.functions:
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
                for vs in itertools.permutations(o.value_area - w, o.dim):
                    if o(*vs) not in w:
                        o_have_two_vals = True
                        break
                if o_have_two_vals:
                    # o найдено. проверка набора функций для ее выведения
                    gs = list(filter(lambda g: g.value_area > w, logic1.functions))
                    if sum(g.set_able_to_out(w) for g in gs) == 0:
                        if find([o], gs):
                            found_functions.append(o)
                        else:
                            return False

    return found_functions
