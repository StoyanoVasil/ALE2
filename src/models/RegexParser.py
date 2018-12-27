from graphviz import Digraph
import pydot

from src.models.StateGenerator import *
from src.models.Automaton import Automaton
from src.models.utils import swap_node_shape


class Counter:
    def __init__(self):
        self.counter = 0

    def __repr__(self):
        self.counter = self.counter + 1
        return f'{self.counter}'


operators = {
    '*': generate_kleene,
    '|': generate_or,
    '.': generate_concatenation
}

def parse_regex(expression):
    counter = Counter()
    dot = Digraph()
    dot.attr(rankdir='TB')
    data = _generate_automaton(_remove_expression_whitespaces(expression), dot, counter)
    data['final'].is_final = True
    swap_node_shape(dot, data['final'].id, "doublecircle")

    # begging arrow
    dot.node('arr', '', shape="point")
    dot.edge('arr', data['initial'].id, shape="arrow")

    aut = Automaton('', data['initial'])
    name = str(id(aut))
    dot.save(f'src/static/pics/{name}.gv')
    (graph, ) = pydot.graph_from_dot_file(f'src/static/pics/{name}.gv')
    graph.write_png(f'src/static/pics/{name}.png')
    finite = aut.is_finite()
    possible_words = []
    if finite:
        possible_words = aut.get_all_words()
    return [name, False, [], finite, possible_words]

def _remove_expression_whitespaces(expression):
    return ''.join(expression.split(' '))

def _generate_automaton(expression, dot, counter):
    try:
        index = _get_operator_comma_index(expression)
        operator = operators[expression[0]]
        if expression[0] == '*':
            return operator(
                counter,
                _generate_automaton(expression[2:-1], dot, counter),
                dot
            )
        else:
            return operator(
                counter,
                _generate_automaton(expression[2:index], dot, counter),
                _generate_automaton(expression[index+1:-1], dot, counter),
                dot
            )
    except KeyError:
        return generate_transition(counter, expression, dot)

def _get_operator_comma_index(expression):
    index = -1
    coma_count = 0
    bracket_count = 0
    for i, char in enumerate(expression):
        if char == '(': bracket_count += 1
        if char == ')': bracket_count -= 1
        if bracket_count == 1 and char == ',':
            index = i
            coma_count += 1
    return index
