"""Алгоритмы анализа и сравнения логик"""

from algorithm.structures.logic import TableFunction
from algorithm import optimizations
import logging
from abc import ABC, abstractmethod


class LogicComparator(ABC):
    def __call__(self, logic1, logic2):
        dominance1 = self.check_dominance(logic1, logic2)
        dominance2 = self.check_dominance(logic2, logic1)

        if dominance1 and dominance2:
            return 'equivalent'
        elif dominance1:
            return 'embedded'
        elif dominance2:
            return 'embeds'
        else:
            return 'non-comparable'

    def check_dominance(self, logic1, logic2):
        logging.debug(logic1.name + ' on ' + logic2.name)

        if not optimizations.indiscernible_of_values(logic1, logic2):
            return False

        if not optimizations.embedding_of_value_area(logic1, logic2):
            return False

        if not optimizations.closure_sets(logic1, logic2):
            return False

        found = optimizations.sets_w(logic1, logic2, self.brute_force)
        if found is None:
            return False

        need = self.brute_force(set(logic2.functions) - set(found), logic1.functions)
        if len(need) == 0:
            return True
        else:
            logging.debug('(brute-force) functions {} in {} cannot be constructed in the basis of {}'.format(
                need, logic2.name, logic1.name
            ))
            return False

    @abstractmethod
    def brute_force(self, need_functions, have_functions):
        """Возвращает функции, которые не удалось вывести"""
        pass


class AsymmetricComparator(LogicComparator):
    def brute_force(self, need_functions, have_functions):
        checked, to_check = set(have_functions), set(have_functions)
        need = set(need_functions) - checked

        while len(to_check):
            new = set()

            for f in to_check:
                for g in checked:
                    new.update(AsymmetricComparator._compose_functions(f, g))
                    if g not in to_check:
                        new.update(AsymmetricComparator._compose_functions(g, f))

                    need -= new
                    if len(need) == 0:
                        return need

            to_check = new - checked
            checked.update(to_check)

        return need

    @staticmethod
    def _compose_functions(f, g):
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
                    # tables.append(
                    #     tuple(tuple(f(i, i) for _ in values) for i in values))
                    # tables.append(
                    #     tuple(tuple(f(j, j) for j in values) for _ in values))
                    tables.append(
                        tuple(f(i, i) for i in values))
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


class SymmetricComparator(LogicComparator):
    def brute_force(self, need_functions, have_functions):
        values = tuple(have_functions[0].values.keys())
        value_area = set()
        for f in have_functions:
            value_area.update(f.value_area)

        base_1d = tuple(filter(lambda x: x.dim == 1, have_functions))
        base_2d = tuple(filter(lambda x: x.dim == 2, have_functions))

        checked, to_check = set(), set()
        need = set(filter(lambda x: x.dim == 2, need_functions))
        for uno in filter(lambda x: x.dim == 1, need_functions):
            need.add(TableFunction(
                tuple(tuple(uno(i) for _ in values) for i in values),
                have_functions[0].values
            ))

        to_check.add(TableFunction(
            tuple(tuple(i for _ in values) for i in values),
            have_functions[0].values
        ))
        to_check.add(TableFunction(
            tuple(tuple(j for j in values) for _ in values),
            have_functions[0].values
        ))
        for v in value_area:
            to_check.add(TableFunction(
                tuple(tuple(v for _ in values) for _ in values),
                have_functions[0].values
            ))

        checked.update(to_check)

        while len(to_check):
            new = set()

            for k in to_check:
                for o in base_1d:
                    new.add(TableFunction(
                        tuple(tuple(o(k(i, j)) for j in values) for i in values),
                        have_functions[0].values))

                for p in checked:
                    for o in base_2d:
                        new.add(SymmetricComparator._compose_functions(k, p, o))
                        if not o.is_symmetric and p not in to_check:
                            new.add(SymmetricComparator._compose_functions(p, k, o))

                    need -= new
                    if len(need) == 0:
                        return need

            to_check = new - checked
            checked.update(to_check)

        return need

    @staticmethod
    def _compose_functions(f, g, o):
        if f.dim == 2 and g.dim == 2:
            table = tuple(tuple(o(f(i, j), g(i, j)) for j in f.values.keys()) for i in f.values.keys())
        elif f.dim == 2 and g.dim == 1:
            table = tuple(tuple(o(f(i, j), g(j)) for j in f.values.keys()) for i in f.values.keys())
        elif f.dim == 1 and g.dim == 2:
            table = tuple(tuple(o(f(i), g(i, j)) for j in f.values.keys()) for i in f.values.keys())
        else:
            table = tuple(tuple(o(f(i), g(j)) for j in f.values.keys()) for i in f.values.keys())

        return TableFunction(table, f.values)


class AggregatedComparator(AsymmetricComparator, SymmetricComparator):
    def brute_force(self, need_functions, have_functions):
        checked, to_check = set(have_functions), set(have_functions)
        need = set(need_functions) - checked

        have_2d = list(filter(lambda x: x.dim == 2, have_functions))

        while len(to_check):
            new = set()

            for f in to_check:
                for g in checked:
                    new.update(AggregatedComparator._compose_functions(f, g))
                    if g not in to_check:
                        new.update(AggregatedComparator._compose_functions(g, f))

                    need -= new
                    if len(need) == 0:
                        return need

            for f in to_check:
                for g in checked:
                    for o in have_2d:
                        new.add(AggregatedComparator._compose_functions(f, g, o))
                        if g not in to_check and not o.is_symmetric:
                            new.add(AggregatedComparator._compose_functions(g, f, o))

                    need -= new
                    if len(need) == 0:
                        return need

            to_check = new - checked
            checked.update(to_check)

        return need

    @staticmethod
    def _compose_functions(*args):
        if len(args) == 2:
            return AsymmetricComparator._compose_functions(*args)
        else:
            return SymmetricComparator._compose_functions(*args)
