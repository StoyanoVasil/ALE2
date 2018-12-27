from src.models.State import State


def generate_transition(counter, letter, dot):
    initial_state = State(counter)
    final_state = State(counter)
    initial_state.add_transition(letter, final_state)
    dot.node(initial_state.id, initial_state.name, shape='circle')
    dot.node(final_state.id, final_state.name, shape='circle')
    dot.edge(initial_state.id, final_state.id, letter)
    return {
        'initial': initial_state,
        'final': final_state
    }

def generate_or(counter, data1, data2, dot):
    initial_state = State(counter)
    dot.node(initial_state.id, initial_state.name, shape='circle')

    initial_state.add_transition('_', data1['initial'])
    dot.edge(initial_state.id, data1['initial'].id, label='ε')

    initial_state.add_transition('_', data2['initial'])
    dot.edge(initial_state.id, data2['initial'].id, label='ε')

    final_state = State(counter)
    dot.node(final_state.id, final_state.name, shape='circle')

    data1['final'].add_transition('_', final_state)
    dot.edge(data1['final'].id, final_state.id, label='ε')

    data2['final'].add_transition('_', final_state)
    dot.edge(data2['final'].id, final_state.id, label='ε')

    return {
        'initial': initial_state,
        'final': final_state
    }

def generate_concatenation(counter, data1, data2, dot):
    data1['final'].add_transition('_', data2['initial'])
    dot.edge(data1['final'].id, data2['initial'].id, label='ε')

    return {
        'initial': data1['initial'],
        'final': data2['final']
    }

def generate_kleene(counter, data, dot):
    initial_state = State(counter)
    dot.node(initial_state.id, initial_state.name, shape='circle')

    initial_state.add_transition('_', data['initial'])
    dot.edge(initial_state.id, data['initial'].id, label='ε')

    final_state = State(counter)
    dot.node(final_state.id, final_state.name, shape='circle')

    data['final'].add_transition('_', final_state)
    dot.edge(data['final'].id, final_state.id, label='ε')

    initial_state.add_transition('_', final_state)
    dot.edge(initial_state.id, final_state.id, label='ε')

    data['final'].add_transition('_', data['initial'])
    dot.edge(data['final'].id, data['initial'].id, label='ε')

    return {
        'initial': initial_state,
        'final': final_state
    }