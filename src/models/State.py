
class State:

    def __init__(self, name):
        self.id = str(id(self))
        self.name = name
        self.is_final = False
        self.transitions = {}

    def __repr__(self):
        return self.name

    def add_transition(self, symbol, next_state):
        if symbol in self.transitions: self.transitions[symbol].append(next_state)
        else: self.transitions[symbol] = [next_state]