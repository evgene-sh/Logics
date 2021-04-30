import itertools


class Logic:
    def __init__(self, mvlog):
        self.name = mvlog.name
        self.values = mvlog.values
        self.functions = self._parse(mvlog)

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

    def __str__(self):
        return 'Name: ' + self.name + '\n' + \
               'Values: ' + str(list(self.values.keys())) + '\n' + \
               'Functions: ' + '\n' + str(self.functions)


class TableFunction:
    """Представление функций в логиках"""
    def __init__(self, name, data, dim, values):
        self.name = name
        self.data = data
        self.dim = dim
        self.values = values
        self.is_symmetric = TableFunction._is_symmetric(self.data, self.dim)

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

    @staticmethod
    def _is_symmetric(data, dim):
        if dim > 1:
            for i in range(len(data)):
                for j in range(i+1, len(data[i])):
                    if data[i][j] != data[j][i]:
                        return False

        return True
