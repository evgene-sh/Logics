import numpy as np


class Logic:
    def __init__(self, mvlog):
        self.name = mvlog.name
        self.values = mvlog.values
        self.functions = self._parse(mvlog)

    def _parse(self, mvlog):
        table_functions = list(map(
            lambda f: TableFunction(f.name, self._parse_function(f), mvlog.values),
            mvlog.functions))

        return table_functions

    def _parse_function(self, f):
        dim = len(f.sentences[0][0])
        table = np.chararray([len(self.values)] * dim)
        print(*f.sentences, sep='\n', end='\n\n')

        for sentence in f.sentences:
            table[tuple(self.values[sentence[0][i]] for i in range(dim))] = sentence[1]

        return table

    def __str__(self):
        return 'Name: ' + self.name + '\n' + \
               'Values: ' + str(self.values) + '\n' + \
               'Functions: ' + '\n' + str(self.functions)


class TableFunction:
    def __init__(self, name, data, values):
        self.name = name
        self.data = data
        self.values = values
        self._hash = hash(str(self.data))

    def __call__(self, *args):
        return self.data[[self.values[arg].decode() for arg in args]]

    def __str__(self):
        return self.name + '\n' + str(self.data) + '\n'

    def __repr__(self):
        return '\n' + self.__str__() + '\n'

    def __eq__(self, other):
        return self.values == other.values and (self.data == other.data).all()

    def __hash__(self):
        return self._hash
