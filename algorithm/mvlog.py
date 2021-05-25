"""Обнаружение структуры во входном файле"""

import re

NAME_STR = 'Name *= *[A-Za-z0-9_]+\n'
VALUES_STR = 'Values *= *\[(\S+, *)*\S+\]\n'
VALUE = '[^\s,]+'
FUNCTION = '[A-Za-z0-9_]+ *\\{[^\\}]+\\}'
SENTENCE_STR = '[^\n]+=[^;]+'


class ParsingException(ValueError):
    """Вызывается, когда во входном файле находится ошибка"""
    pass


class Mvlog:
    def __init__(self, path):
        self.name, self.values, self.functions = Mvlog._parse(path)

    @staticmethod
    def _parse(path):
        with open(path) as f:
            data = f.read()

        name_str = re.search(NAME_STR, data)
        if not name_str:
            raise ParsingException('Ошибка в объявлении имени логики файла ' + path)
        name = name_str.group(0).split('=')[1].strip()

        val_str = re.search(VALUES_STR, data[name_str.end():])
        if not val_str:
            raise ParsingException('Ошибка в объявлении переменных логики файла ' + path)
        values = dict([(j, i) for i, j in enumerate(
            sorted(tuple(
                re.findall(VALUE, val_str.group(0).split('=')[1].strip()[1:-1]))))])

        functions_texts = re.findall(FUNCTION, data[name_str.end() + val_str.end():])
        functions = tuple(map(lambda text: Function(text, path), functions_texts))

        return name, values, functions

    def __str__(self):
        return 'Name: ' + self.name + '   Values: ' + str(self.values) + '   Functions: ' + str(self.functions)

    def __repr__(self):
        return self.name


class Function:
    def __init__(self, text, file_path):
        self.name, self.sentences = Function._parse(text, file_path)
        self.dim = len(self.sentences[0][0])

    @staticmethod
    def _parse(text, file_path):
        name = re.search('\S+', text).group(0)

        sentences_texts = re.findall(SENTENCE_STR, text)
        if len(sentences_texts) == 0:
            raise ParsingException('Отсутствуют предложения для функции {} {}'.format(name, file_path))

        sentences = tuple(map(lambda text:
                              tuple(map(lambda x: x.strip(), text.split('='))),
                              sentences_texts))
        sentences = tuple(map(lambda s: (s[0].split(' '), s[1]), sentences))

        for sentence in sentences:
            if len(sentence[0]) != len(sentences[0][0]):
                raise ParsingException('Несовпадение количеств аргументов для функции {} {}'.format(name, file_path))
            if len(sentence[1].split(' ')) != 1:
                raise ParsingException('Количество возвращаемых значений != 1 для функции {} {}'.format(name, file_path))

        return name, sentences

    def __str__(self):
        return self.name + str(self.sentences)

    def __repr__(self):
        return self.name
