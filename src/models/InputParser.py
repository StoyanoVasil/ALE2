from graphviz import Digraph
import pydot
from functools import reduce

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

def parse_transition(initial_state, transition_state, states, dot, stack_ops=None):
    initial = initial_state.split(',')
    if stack_ops:
        states[initial[0]].add_transition(initial[1], (states[transition_state], stack_ops))
    else:
        states[initial[0]].add_transition(initial[1], states[transition_state])

def check_if_dfa(states, alphabet):
    for key, value in states.items():
        if len(value.transitions.keys()) != len(alphabet): return False
        if ''.join(sorted(value.transitions.keys())) != ''.join(sorted(alphabet)): return False
        for transition in value.transitions.values():
            if len(transition) != 1: return False
    return True

def generate_dot(states, dot, is_pda=None):
    # dot.attr(rankdir='LR')
    _add_states(states, dot)
    _add_transitions(states, dot, is_pda)

def _add_states(states, dot):
    for key, value in states.items():
        if value.is_final: dot.node(value.id, value.name, shape='doublecircle')
        else: dot.node(value.id, value.name, shape='circle')

def _add_transitions(states, dot, is_pda):
    for key, value in states.items():
        for k, v in value.transitions.items():
            for transition in v:
                if is_pda:
                    if k is '_': dot.edge(value.id, transition[0].id, f'ε {transition[1]}')
                    else: dot.edge(value.id, transition[0].id, f'{k} {transition[1]}')
                else:
                    if k is '_': dot.edge(value.id, transition.id, 'ε')
                    else: dot.edge(value.id, transition.id, k)

def parse(text):
    aut, arr = get_automaton(text)
    return arr

def parse_to_dfa(text):
    arr = get_automaton(text)
    if arr[1][1]: return arr[1]
    else:
        new = convert_to_dfa(arr[0])
        rename_states(new)
        dot = Digraph()
        generate_dot_dfa_conversion([tup[0] for tup in new], dot)
        name = new[0][0].id
        dot.save(f'src/static/pics/{name}.gv')
        (graph,) = pydot.graph_from_dot_file(f'src/static/pics/{name}.gv')
        graph.write_png(f'src/static/pics/{name}.png')
        evaluations = []
        for word in arr[2]:
            accepted = new[0][0].evaluate_word(word[0])
            if accepted:
                if word[1] == 'y':
                    evaluations.append([','.join(word), True])
                else:
                    evaluations.append([','.join(word), False])
            else:
                if word[1] == 'y':
                    evaluations.append([','.join(word), False])
                else:
                    evaluations.append([','.join(word), True])
        return [name, True, evaluations, False, []]

def rename_states(new):
    i = 0
    for tuple in new:
        tuple[0].name = 'S' + str(i)
        i = i + 1

def generate_dot_dfa_conversion(states, dot):
    for state in states:
        if state.is_final: dot.node(state.id, state.name, shape='doublecircle')
        else: dot.node(state.id, state.name, shape='circle')
    for state in states:
        for key in state.transitions.keys():
            dot.edge(state.id, state.transitions[key][0].id, key)
    # beginning arrow
    dot.node('arr', '', shape="point")
    dot.edge('arr', states[0].id, shape="arrow")

def get_automaton(text):
    alphabet = None
    states = None
    dot = Digraph()
    dot.attr(rankdir='TB')
    is_dfa = True
    transitions_marker = False
    words_marker = False
    words = []
    evaluations = []
    pda = False
    for line in text.split('\n'):
        # remove whitespaces in beginning and end; reduce multiple whitespaces to one
        line = ' '.join(line.split())

        # ignore comments and empty lines
        if skip(line): continue

        # stop if end of file
        if line.strip() == 'end.': break

        # handle line
        if line.startswith('alphabet:'): alphabet = parse_alphabet(line)
        elif line.startswith('stack'): pda = True
        elif line.startswith('states:'): states = parse_states(line, dot)
        elif line.startswith('final:'): parse_final(line, states)
        elif line.startswith('transitions:'): transitions_marker = True
        elif line.startswith('words:'):
            transitions_marker = False
            words_marker = True
        elif transitions_marker:
            if pda:
                line = ' '.join(line.split())
                l = line.split(' ')
                if '[' in line and ']' in line:
                    parse_transition(l[0], l[3], states, dot, stack_ops=l[1])
                else:
                    parse_transition(l[0], l[2], states, dot, stack_ops='[_,_]')
            else:
                l = line.split(' ')
                parse_transition(l[0], l[2], states, dot)
                if l[0].split(',')[1] == '_': is_dfa = False
        elif words_marker:
            l = line.split(',')
            words.append((l[0], l[1]))

    aut = Automaton(alphabet, list(states.values())[0], pda)
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
    generate_dot(states, dot, is_pda=pda)
    if is_dfa: finite = False
    else: finite = aut.is_finite() if not pda else False
    possible_words = []
    if finite:
        possible_words = aut.get_all_words()
    name = str(id(aut))

    # beginning arrow
    dot.node('arr', '', shape="point")
    dot.edge('arr', aut.initial_state.id, shape="arrow")

    dot.save(f'src/static/pics/{name}.gv')
    (graph, ) = pydot.graph_from_dot_file(f'src/static/pics/{name}.gv')
    graph.write_png(f'src/static/pics/{name}.png')
    return [aut, [name, is_dfa, evaluations, finite, possible_words], words]

def convert_to_dfa(aut, new=None, iteration=None):
    if new is None:
        initial = State('initial')
        epsilon_closure = []
        get_epsilon_closure(aut.initial_state, epsilon_closure)
        initial.id = str(reduce(lambda x, y: x + y, [int(state.id) for state in epsilon_closure]))
        new = [(initial, epsilon_closure)]
        if contains_final_state(epsilon_closure): initial.is_final = True
    if iteration is None: iteration = 0
    if iteration < len(new):
        sup = {}
        for letter in aut.alphabet:
            sup[letter] = get_states_for_letter(new[iteration][1], letter)
        add_new_states(new, sup)
        add_transitions(new, sup, iteration)
        return convert_to_dfa(aut, new, iteration + 1)
    else:
        return new

def get_epsilon_closure(state, epsilon_closure):
    if state not in epsilon_closure: epsilon_closure.append(state)
    if '_' in state.transitions:
        for transition in state.transitions['_']:
            if transition not in epsilon_closure: epsilon_closure.append(transition)
            get_epsilon_closure(transition, epsilon_closure)


def add_transitions(new, sup, iteration):
    state = new[iteration][0]
    for key in sup.keys():
        transition_state = find_state_from_superset(new, sup[key])
        state.add_transition(key, transition_state)

def find_state_from_superset(new, superset):
    for state in superset:
        get_epsilon_closure(state, superset)
    if len(superset) == 0: id = 0
    else: id = reduce(lambda x, y: x + y, [int(s.id) for s in superset])
    for tuple in new:
        if tuple[0].id == str(id): return tuple[0]

def add_new_states(new, sup):
    for s_arr in sup.values():
        if len(s_arr) == 0:
            if not contains_state_with_id(new, 0):
                new_state = State('0')
                new_state.id = '0'
                new.append((new_state, s_arr))
        else:
            epsilon_closure = []
            for state in s_arr:
                get_epsilon_closure(state, epsilon_closure)
            id = reduce(lambda x, y: x + y, [int(state.id) for state in epsilon_closure])
            if not contains_state_with_id(new, id):
                new_state = State('')
                new_state.id = str(id)
                new_state.is_final = contains_final_state(epsilon_closure)
                new.append((new_state, epsilon_closure))

def contains_final_state(states):
    for state in states:
        if state.is_final: return True
    return False

def contains_state_with_id(new, id):
    for tuple in new:
        if tuple[0].id == str(id): return True
    return False

def get_states_for_letter(states, letter, new_states=None, visited_states=None):
    if new_states is None: new_states = []
    if visited_states is None: temp_visited_states = []
    else: temp_visited_states = visited_states[:]
    for state in states:
        temp_visited_states.append(state)
        if '_' in state.transitions:
            for s in state.transitions['_']:
                if s in temp_visited_states: continue
                get_states_for_letter([s], letter, new_states, temp_visited_states)
        if letter in state.transitions: add_without_duplicates(new_states, state.transitions[letter])
    return new_states

def add_without_duplicates(arr1, arr2):
    for state in arr2:
        if state in arr1: continue
        arr1.append(state)
