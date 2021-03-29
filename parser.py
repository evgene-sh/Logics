import re
import pandas as pd

NAME_STR = 'Name\s*=\s*[A-Za-z0-9_]+'
VALUES_STR = 'Values\s*=\s*\[(\S+,\s*)*\S+\]'
VALUE = '[^\s,]+'
FUNCTION = '[A-Za-z0-9_]+\s*\\{[^\\}]+\\}'
SENTENCE_STR = '[^\n]+=[^;]+'


def parse(path):
    logic_mvlog = Mvlog(path)
    return LogicTables(logic_mvlog)


class LogicTables:
    def __init__(self, mvlog):
        self.name = mvlog.name
        self.values = mvlog.values
        self.tables = self.parse(mvlog.functions)

    def parse(self, functions):
        tables = []

        for f in functions:
            if f.dim == 1:
                tables.append(
                    Table(name=f.name, data=self._parse_1d(f))
                )
            else:
                tables.append(
                    Table(name=f.name, data=self._parse_2d(f))
                )

        return tables

    def _parse_1d(self, f):
        df = pd.Series(index=self.values, dtype=object)

        for s in f.sentences:
            df[s[0][0]] = s[1]

        return df

    def _parse_2d(self, f):
        df = pd.DataFrame(columns=self.values, index=self.values)

        for s in f.sentences:
            df[s[0][0]][s[0][1]] = s[1]

        return df

    def __str__(self):
        return 'Name: ' + self.name + '\n' + \
               'Values: ' + str(self.values) + '\n' + \
               'Tables: ' + '\n' + str(self.tables)


class Table:
    def __init__(self, name, data):
        self.name = name
        self.data = data

    def __str__(self):
        return self.name + '\n' + str(self.data) + '\n'

    def __repr__(self):
        return '\n' + self.__str__() + '\n'


class Mvlog:
    def __init__(self, path):
        self.name, self.values, self.functions = Mvlog.parse(path)

    @staticmethod
    def parse(path):
        with open(path) as f:
            data = f.read()

        name_str = re.search(NAME_STR, data)
        name = name_str.group(0).split('=')[1].strip()

        val_str = re.search(VALUES_STR, data[name_str.end():])
        values = tuple(re.findall(VALUE, val_str.group(0).split('=')[1].strip()[1:-1]))

        functions_texts = re.findall(FUNCTION, data[name_str.end() + val_str.end():])
        functions = tuple(map(lambda text: Function(text), functions_texts))

        return name, values, functions

    def __str__(self):
        return 'Name: ' + self.name + '   Values: ' + str(self.values) + '   Functions: ' + str(self.functions)

    def __repr__(self):
        return self.name


class Function:
    def __init__(self, text):
        self.name, self.sentences = Function.parse(text)
        self.dim = len(self.sentences[0][0])

    @staticmethod
    def parse(text):
        name = re.search('\S+', text).group(0)

        sentences_texts = re.findall(SENTENCE_STR, text)
        sentences = tuple(map(lambda text:
                              tuple(map(lambda x: x.strip(), text.split('='))),
                              sentences_texts))
        sentences = tuple(map(lambda s: (s[0].split(' '), s[1]), sentences))

        return name, sentences

    def __str__(self):
        return self.name + str(self.sentences)

    def __repr__(self):
        return self.name


if __name__ == '__main__':
    klini = parse('data/Klini.mvlog')
    print(klini)
