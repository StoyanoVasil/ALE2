
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

    def evaluate_word(self, word):
        if len(word) == 0:
            if self.is_final: return True
            else: return False
        if word[0] in self.transitions:
            for state in self.transitions[word[0]]:
                if state.evaluate_word(word[1:]): return True
        return False
