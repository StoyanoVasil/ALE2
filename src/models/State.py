
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

    def is_finite(self, states=None, consumed=None):
        # TODO: empty transitions bug
        if states is None:
            tempStates = []
        else:
            tempStates = states[:]
        if consumed is None:
            tempConsumed = []
        else:
            tempConsumed = consumed[:]
        if self not in tempStates:
            tempStates.append(self)
            if '_' in self.transitions:
                for state in self.transitions['_']:
                    if state == self: continue
                    tempConsumed.append(('_', self))
                    if not state.is_finite(states=tempStates, consumed=tempConsumed): return False
            for k in self.transitions.keys():
                if k is not '_':
                    for state in self.transitions[k]:
                        tempConsumed.append((k, self))
                        if not state.is_finite(states=tempStates, consumed=tempConsumed): return False
            return True
        else:
            for tuple in reversed(tempConsumed):
                if tuple[0] is not '_': return False
                if tuple[1] == self: break
            return True

    def get_all_words(self, words, word=None):
        # TODO: fix infinite loop when there is empty transition loop
        if word is None: word = ''
        if self.is_final:
            words.append(word)
        if '_' in self.transitions:
            for state in self.transitions['_']:
                if state == self: continue
                state.get_all_words(word=word, words=words)
        for k in self.transitions.keys():
            if k is not '_':
                temp = word + k
                for state in self.transitions[k]:
                    state.get_all_words(word=temp, words=words)
