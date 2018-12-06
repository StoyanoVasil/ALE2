
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

    def evaluate_word(self, word, epsilon=None):
        if len(word) == 0:
            if self.is_final: return True
            else: return False
        if '_' in self.transitions:
            for state in self.transitions['_']:
                if epsilon is None:
                    epsilon = [state]
                    if state.evaluate_word(word, epsilon=epsilon): return True
                elif state not in epsilon:
                    epsilon.append(state)
                    if state.evaluate_word(word, epsilon=epsilon): return True
        if word[0] in self.transitions:
            for state in self.transitions[word[0]]:
                if state.evaluate_word(word[1:]): return True
        return False

    def is_finite(self, states=None):
        if states is None: states = []
        if self not in states:
            states.append(self)
            if '_' in self.transitions:
                for state in self.transitions['_']:
                    if state == self: continue
                    if not state.is_finite(states=states): return False
            for k in self.transitions.keys():
                for state in self.transitions[k]:
                    if not state.is_finite(states=states): return False
            return True
        else: return False
