"""Создание dot-файла на основе результатов"""

from graphviz import Digraph


def draw_graph(transitivity, output_path):
    names = dict([(v, k) for k, v in transitivity.names.items()])
    dot = Digraph()
    dot.graph_attr['rankdir'] = 'BT'

    # факторизация
    nums_dict, num = dict(), 0
    for i in range(transitivity.length):
        if i in nums_dict:
            continue
        to_string = []
        for j in transitivity.find_relation('equivalent', [i]):
            nums_dict[j] = str(num)
            to_string.append(names[j])
        dot.node(str(num), '\n'.join(sorted(to_string)))
        num += 1

    # построение ребер
    edges = set()
    for i in range(transitivity.length):
        for j in range(i+1, transitivity.length):
            if transitivity.relations[i][j] == 'embedded':
                group = set(filter(lambda x: x != j and transitivity.relations[i][x] == 'embedded', range(transitivity.length)))
                if j not in transitivity.find_relation('embedded', group):
                    edges.add((nums_dict[j], nums_dict[i]))
            elif transitivity.relations[i][j] == 'embeds':
                group = set(filter(lambda x: x != j and transitivity.relations[i][x] == 'embeds', range(transitivity.length)))
                if j not in transitivity.find_relation('embeds', group):
                    edges.add((nums_dict[i], nums_dict[j]))

    for edge in edges:
        dot.edge(*edge)

    dot.render(output_path+'.dot')
