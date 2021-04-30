"""Обнаружение структуры во входном файле"""


import re

NAME_STR = 'Name\s*=\s*[A-Za-z0-9_]+'
VALUES_STR = 'Values\s*=\s*\[(\S+,\s*)*\S+\]'
VALUE = '[^\s,]+'
FUNCTION = '[A-Za-z0-9_]+\s*\\{[^\\}]+\\}'
SENTENCE_STR = '[^\n]+=[^;]+'


class Mvlog:
    def __init__(self, path):
        self.name, self.values, self.functions = Mvlog._parse(path)

    @staticmethod
    def _parse(path):
        with open(path) as f:
            data = f.read()

        name_str = re.search(NAME_STR, data)
        name = name_str.group(0).split('=')[1].strip()

        val_str = re.search(VALUES_STR, data[name_str.end():])
        values = dict([(j, i) for i, j in enumerate(
            sorted(tuple(
                re.findall(VALUE, val_str.group(0).split('=')[1].strip()[1:-1]))))])

        functions_texts = re.findall(FUNCTION, data[name_str.end() + val_str.end():])
        functions = tuple(map(lambda text: Function(text), functions_texts))

        return name, values, functions

    def __str__(self):
        return 'Name: ' + self.name + '   Values: ' + str(self.values) + '   Functions: ' + str(self.functions)

    def __repr__(self):
        return self.name


class Function:
    def __init__(self, text):
        self.name, self.sentences = Function._parse(text)
        self.dim = len(self.sentences[0][0])

    @staticmethod
    def _parse(text):
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
