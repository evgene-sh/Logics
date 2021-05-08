import itertools


class Logic:
    def __init__(self, mvlog):
        self.name = mvlog.name
        self.values = mvlog.values
        self.functions = self._parse(mvlog)
        self.eq_vals = self._get_equal_values()

    def _parse(self, mvlog):
        table_functions = tuple(map(
            lambda f: TableFunction(f.name, *self._parse_function(f), mvlog.values),
            mvlog.functions))

        return table_functions

    def _parse_function(self, f):
        dim = len(f.sentences[0][0])

        if dim == 1:
            table = [''] * len(self.values)
            for sentence in f.sentences:
                if sentence[0][0].startswith('s.'):
                    for i in range(len(table)):
                        if table[i] == '':
                            table[i] = sentence[1]
                else:
                    table[self.values[sentence[0][0]]] = sentence[1]
            table = tuple(table)

        elif dim == 2:
            table = [[''] * len(self.values) for _ in range(len(self.values))]

            for sentence in f.sentences:
                if sentence[0][0].startswith('s.') and sentence[0][1].startswith('s.'):
                    if sentence[0][0] != sentence[0][1]:
                        for i, j in itertools.permutations(range(len(table)), 2):
                            if table[i][j] == '':
                                table[i][j] = sentence[1]

                    for i in range(len(table)):
                        if table[i][i] == '':
                            table[i][i] = sentence[1]

                elif sentence[0][0].startswith('s.') and not sentence[0][1].startswith('s.'):
                    for i in range(len(table)):
                        if table[i][self.values[sentence[0][1]]] == '':
                            table[i][self.values[sentence[0][1]]] = sentence[1]

                elif not sentence[0][0].startswith('s.') and sentence[0][1].startswith('s.'):
                    for i in range(len(table)):
                        if table[self.values[sentence[0][0]]][i] == '':
                            table[self.values[sentence[0][0]]][i] = sentence[1]

                else:
                    table[self.values[sentence[0][0]]][self.values[sentence[0][1]]] = sentence[1]

            for i in range(len(self.values)):
                table[i] = tuple(table[i])
            table = tuple(table)

        else:
            raise NotImplementedError('Can\'t work with dimensions: ' + str(dim))

        return table, dim

    def _get_equal_values(self):
        equals = set()
        for v1, v2 in itertools.combinations(self.values, 2):
            equal = True

            for f in self.functions:
                if f.dim == 1:
                    if f(v1) != f(v2):
                        equal = False
                        break
                elif f.dim == 2:
                    for v in self.values:
                        if f(v1, v) != f(v2, v) or f(v, v1) != f(v, v2):
                            equal = False
                            break
                else:
                    raise NotImplementedError('Не реализовано equals для 2+ мерных функций')

            if equal:
                equals.add((min(v1, v2), max(v1, v2)))

        return equals

    def __str__(self):
        return 'Name: ' + self.name + '\n' + \
               'Values: ' + str(list(self.values.keys())) + '\n' + \
               'Functions: ' + '\n' + str(self.functions)

    @property
    def value_area(self):
        return set().union(*[f.value_area for f in self.functions])


class TableFunction:
    """Представление функций в логиках"""
    def __init__(self, name, data, dim, values):
        self.name = name
        self.data = data
        self.dim = dim
        self.values = values
        self.is_symmetric = TableFunction._is_symmetric(self.data, self.dim)
        self.value_area = TableFunction._value_area(self.data, self.dim)

    def __call__(self, *args):
        data = self.data
        for arg in args:
            data = data[self.values[arg]]
        return data

    def __str__(self):
        return self.name + '\n' + '\n'.join([str(data) for data in self.data]) + '\n'

    def __repr__(self):
        return '\n' + self.__str__() + '\n'

    def __eq__(self, other):
        return self.data == other.data

    def __hash__(self):
        return hash(self.data)

    def set_is_closure(self, s):
        if self.dim == 1:
            for val in s:
                if self(val) not in s:
                    return False
            return True

        elif self.dim == 2:
            for v1, v2 in itertools.permutations(s, 2):
                if self(v1, v2) not in s:
                    return False
            for val in s:
                if self(val, val) not in s:
                    return False
            return True

        else:
            raise NotImplementedError('Проверка замыкания не реализована для  dim 2+')

    def set_able_to_out(self, s):
        if self.dim == 1:
            for val in s:
                if self(val) not in s:
                    return True
            return False

        elif self.dim == 2:
            for val in s:
                for other in self.values.keys():
                    if self(val, other) not in s or self(other, val) not in s:
                        return True
            return False

        else:
            raise NotImplementedError('Проверка возможности выхода не реализована для  dim 2+')

    @staticmethod
    def _is_symmetric(data, dim):
        if dim > 1:
            for i in range(len(data)):
                for j in range(i+1, len(data[i])):
                    if data[i][j] != data[j][i]:
                        return False

        return True

    @staticmethod
    def _value_area(data, dim):
        if dim == 1:
            return set(data)
        else:
            area = set()
            for row in data:
                area.update(row)
            return area
