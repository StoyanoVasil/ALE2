from graphviz import Digraph
import pydot

from models.Automaton import Automaton
from models.State import State


def parse_alphabet(alphabet):
    return alphabet.strip()

def parse_states(states, dot):
    sts = {}
    for name in states.strip().split(','):
        st = State(name)
        sts[name] = st
        dot.node(st.id, st.name)
    return sts

def parse_final(final, states):
    for f in final.strip().split(','):
        states[f].is_final = True

def parse_transition(initial_state, transition_state, states):
    initial = initial_state.split(',')
    dot.edge(states[initial[0]].id, states[transition_state].id, initial[1])
    states[initial[0]].add_transition(initial[1], states[transition_state])

def check_if_dfa(states, alphabet):
    for key, value in states.items():
        if len(value.transitions.keys()) != len(alphabet): return False
        if ''.join(sorted(value.transitions.keys())) != ''.join(sorted(alphabet)): return False
        for transition in value.transitions.values():
            if len(transition) != 1: return False
    return True

if __name__ == '__main__':
    alphabet = None
    states = None
    dot = Digraph()
    is_dfa = True
    with open('./nfa.txt', 'r') as file:
        transitions_marker = False
        for line in file:

            # ignore comments
            if line.startswith('#'): continue
            if line.strip() == 'end.': break

            if line.startswith('alphabet:'): alphabet = parse_alphabet(line.split(' ')[1])
            elif line.startswith('states:'): states = parse_states(line.split(' ')[1], dot)
            elif line.startswith('final:'): parse_final(line.split(' ')[1], states)
            elif line.startswith('transitions:'): transitions_marker = True
            elif transitions_marker:
                l = line.strip().split(' ')
                parse_transition(l[0], l[2], states)
                if l[0].split(',')[1] == '_': is_dfa = False
    if is_dfa:
        is_dfa = check_if_dfa(states, alphabet)
    aut = Automaton(alphabet, list(states.values())[0])
    dot.save('./test.gv')
    (graph, ) = pydot.graph_from_dot_file('./test.gv')
    graph.write_png('./test.png')

    print(is_dfa)
