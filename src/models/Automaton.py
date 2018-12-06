
class Automaton:

    def __init__(self, alphabet, initial_state):
        self.alphabet = alphabet
        self.initial_state = initial_state

    def __repr__(self):
        return f'alphabet: {self.alphabet}\ninitial state: {self.initial_state}'

    def evaluate_word(self, word):
        return self.initial_state.evaluate_word(word)

    def is_finite(self):
        return self.initial_state.is_finite()

    def get_all_words(self):
        words = []
        self.initial_state.get_all_words(words)
        return words
