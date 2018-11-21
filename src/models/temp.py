from graphviz import Digraph
import pydot

from models.Automaton import Automaton
from models.State import State


def skip(line):
    if line.startswith('#'): return True
    if line.startswith('\n'): return True

def parse_alphabet(line):
    return line.split(' ')[1]

def parse_states(line, dot):
    states = line.split(' ')[1]
    sts = {}
    for name in states.split(','):
        st = State(name)
        sts[name] = st
        dot.node(st.id, st.name)
    return sts

def parse_final(line, states):
    final = line.split(' ')[1]
    for f in final.split(','):
        states[f].is_final = True

def parse_transition(initial_state, transition_state, states, dot):
    initial = initial_state.split(',')
    states[initial[0]].add_transition(initial[1], states[transition_state])

def check_if_dfa(states, alphabet):
    for key, value in states.items():
        if len(value.transitions.keys()) != len(alphabet): return False
        if ''.join(sorted(value.transitions.keys())) != ''.join(sorted(alphabet)): return False
        for transition in value.transitions.values():
            if len(transition) != 1: return False
    return True

def generate_dot(states, dot):
    _add_states(states, dot)
    _add_transitions(states, dot)

def _add_states(states, dot):
    for key, value in states.items():
        if value.is_final: dot.node(value.id, value.name, shape='doublecircle')
        else: dot.node(value.id, value.name, shape='circle')

def _add_transitions(states, dot):
    for key, value in states.items():
        for k, v in value.transitions.items():
            for transition in v:
                dot.edge(value.id, transition.id, k)


if __name__ == '__main__':
    alphabet = None
    states = None
    dot = Digraph()
    is_dfa = True
    with open('./nfa.txt', 'r') as file:
        transitions_marker = False
        for line in file:
            # remove whitespaces in beginning and end; reduce multiple whitespaces to one
            line = ' '.join(line.split())

            # ignore comments and empty lines
            if skip(line): continue

            # stop if end of file
            if line.strip() == 'end.': break

            # handle line
            if line.startswith('alphabet:'): alphabet = parse_alphabet(line)
            elif line.startswith('states:'): states = parse_states(line, dot)
            elif line.startswith('final:'): parse_final(line, states)
            elif line.startswith('transitions:'): transitions_marker = True
            elif transitions_marker:
                l = line.split(' ')
                parse_transition(l[0], l[2], states, dot)
                if l[0].split(',')[1] == '_': is_dfa = False
        generate_dot(states, dot)

    if is_dfa:
        is_dfa = check_if_dfa(states, alphabet)
    aut = Automaton(alphabet, list(states.values())[0])
    dot.save('./test.gv')
    (graph, ) = pydot.graph_from_dot_file('./test.gv')
    graph.write_png('./test.png')

    print(is_dfa)
