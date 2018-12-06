from graphviz import Digraph
import pydot

from src.models.Automaton import Automaton
from src.models.State import State


def skip(line):
    if line.startswith('#'): return True
    if line.startswith('\n'): return True
    if len(line) == 0: return True

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
    # dot.attr(rankdir='LR')
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
                if k is '_': dot.edge(value.id, transition.id, 'ε')
                else: dot.edge(value.id, transition.id, k)


def parse(text):
    alphabet = None
    states = None
    dot = Digraph()
    is_dfa = True
    transitions_marker = False
    words_marker = False
    words = []
    evaluations = []
    for line in text.split('\n'):
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
        elif line.startswith('transitions:'):
            transitions_marker = True
        elif line.startswith('words:'):
            transitions_marker = False
            words_marker = True
        elif transitions_marker:
            l = line.split(' ')
            parse_transition(l[0], l[2], states, dot)
            if l[0].split(',')[1] == '_': is_dfa = False
        elif words_marker:
            l = line.split(',')
            words.append((l[0], l[1]))

    aut = Automaton(alphabet, list(states.values())[0])
    if is_dfa:
        is_dfa = check_if_dfa(states, alphabet)
    for word in words:
        accepted = aut.evaluate_word(word[0])
        if accepted:
            if word[1] == 'y': evaluations.append([','.join(word), True])
            else: evaluations.append([','.join(word), False])
        else:
            if word[1] == 'y': evaluations.append([','.join(word), False])
            else: evaluations.append([','.join(word), True])
    generate_dot(states, dot)
    finite = aut.is_finite()
    possible_words = []
    if finite:
        possible_words = aut.get_all_words()
    name = str(id(aut))
    dot.save(f'src/static/pics/{name}.gv')
    (graph, ) = pydot.graph_from_dot_file(f'src/static/pics/{name}.gv')
    graph.write_png(f'src/static/pics/{name}.png')
    return [name, is_dfa, evaluations, finite, possible_words]
