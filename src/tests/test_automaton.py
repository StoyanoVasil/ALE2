import unittest
from unittest.mock import MagicMock

from src.models.Automaton import Automaton
from src.models.State import State

class TestAutomatonClass(unittest.TestCase):

    def test_init(self):
        alphabet = 'abc'
        initial_state = State('A')
        is_pda = False

        automaton = Automaton(alphabet, initial_state, is_pda)

        self.assertEqual(automaton.alphabet, alphabet, "Automaton alphabet is not properly set")
        self.assertEqual(automaton.initial_state, initial_state, "Automaton initial state is not properly set")
        self.assertEqual(automaton.is_pda, is_pda, "Automaton is_pda is not properly set")

    def test_evaluate_word_calls_proper_method(self):
        # Not PDA
        alphabet = 'abc'
        initial_state = State('A')
        initial_state.evaluate_word = MagicMock(return_value=True)
        is_pda = False
        word = 'test'

        automaton = Automaton(alphabet, initial_state, is_pda)
        automaton.evaluate_word(word)

        initial_state.evaluate_word.assert_called_with(word)

        # PDA
        is_pda = True
        initial_state.pda_evaluate_word = MagicMock(return_value=True)

        automaton = Automaton(alphabet, initial_state, is_pda)
        automaton.evaluate_word(word)

        initial_state.pda_evaluate_word.assert_called_with(word, [])

    def test_is_finite_calls_proper_method(self):
        alphabet = 'abc'
        initial_state = State('A')
        initial_state.is_finite = MagicMock(return_value=True)
        is_pda = False

        automaton = Automaton(alphabet, initial_state, is_pda)
        automaton.is_finite()

        initial_state.is_finite.assert_called()

    def test_get_all_words_calls_proper_method(self):
        alphabet = 'abc'
        initial_state = State('A')
        initial_state.get_all_words = MagicMock(return_value=[])
        is_pda = False

        automaton = Automaton(alphabet, initial_state, is_pda)
        automaton.get_all_words()

        initial_state.get_all_words.assert_called_with([])
