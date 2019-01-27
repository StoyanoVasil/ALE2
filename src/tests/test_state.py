import unittest
from unittest.mock import MagicMock

from src.models.State import State


class TestStateClass(unittest.TestCase):

    # Test constructor
    def test_init(self):
        name = 'A'

        state = State(name)

        self.assertEqual(state.name, name, 'State constructor does not set the name properly')
        self.assertEqual(state.is_final, False, 'State constructor did not set is_final properly (should be False)')
        self.assertEqual(state.transitions, {}, 'State constructor did not initialize tansitions as an empty object')

    # Test evaluate_word method
    def test_evaluate_empty_word(self):
        state = State('A')

        # when state is not final
        evaluation = state.evaluate_word('')
        self.assertEqual(evaluation, False, 'Non-final state did not return False for an empty word')

        # when state is final
        state.is_final = True
        evaluation = state.evaluate_word('')
        self.assertEqual(evaluation, True, 'Final state did not return True for an empty word')

    def test_evaluate_non_empty_word_with_no_transitions_in_state_returns_false(self):
        state = State('A')

        evaluation = state.evaluate_word('aaa')

        self.assertEqual(evaluation, False, 'State with no transitions did not return False for a non-empty transitions')

    def test_state_with_epsilon_transition_returns_proper_value(self):
        state = State('A')
        transition_state = State('B')
        transition_state.evaluate_word = MagicMock(return_value=True)
        state.add_transition('_', transition_state)

        evaluation = state.evaluate_word('abc')

        self.assertEqual(evaluation, True, 'State did not return what epsilon transition state returns')

    def test_state_with_letter_transition_returns_proper_value(self):
        state = State('A')
        transition_state = State('B')
        transition_state.evaluate_word = MagicMock(return_value=False)
        state.add_transition('a', transition_state)

        evaluation = state.evaluate_word('abc')

        self.assertEqual(evaluation, False, 'State did not return what letter transition state returns')

    def test_state_with_emtpy_and_letter_transitions_checks_letter_transitions_if_empty_transitions_return_false(self):
        word = 'aa'
        state = State('A')
        empty_transitions_state_1 = State('B')
        empty_transitions_state_1.evaluate_word = MagicMock(return_value=False)
        empty_transitions_state_2 = State('C')
        empty_transitions_state_2.evaluate_word = MagicMock(return_value=False)
        letter_transition = State('D')
        letter_transition.evaluate_word = MagicMock(return_value=True)
        state.add_transition('_', empty_transitions_state_1)
        state.add_transition('_', empty_transitions_state_2)
        state.add_transition('a', letter_transition)

        evaluation = state.evaluate_word(word)

        empty_transitions_state_1.evaluate_word.assert_called()
        empty_transitions_state_2.evaluate_word.assert_called()
        letter_transition.evaluate_word.assert_called_with('a')

        self.assertEqual(evaluation, True, 'State with empty and letter transitions does not return the proper value')

    def test_loop_with_empty_transitions_does_not_create_an_infinite_loop(self):
        state1 = State('A')
        state2 = State('B')
        state3 = State('B')
        state1.add_transition('_', state2)
        state2.add_transition('_', state3)
        state3.add_transition('_', state1)

        evaluation = state1.evaluate_word('abc')

        self.assertEqual(evaluation, False, 'Loop with empty transitions does not act as expected')

    # Test is_finite method
    def test_no_loops_returns_true(self):
        state1 = State('A')
        state2 = State('B')
        state3 = State('B')
        state1.add_transition('_', state2)
        state1.add_transition('_', state3)

        is_finite = state1.is_finite()

        self.assertEqual(is_finite, True, 'State with no following loops does not return True when evaluating if finite')

    def test_epsilon_self_loop_returns_True_when_evaluating_if_finite(self):
        state = State('A')
        state.add_transition('_', state)

        is_finite = state.is_finite()

        self.assertEqual(is_finite, True, 'State with empty self loop does not return True when evaluating if finite')

    def test_letter_self_loop_returns_False_when_evaluating_if_finite(self):
        state = State('A')
        state.add_transition('a', state)

        is_finite = state.is_finite()

        self.assertEqual(is_finite, False, 'State with letter self loop does not return False when evaluating if finite')

    def test_epsilon_multiple_state_loop_returns_True_when_evaluating_if_finite(self):
        state1 = State('A')
        state2 = State('B')
        state3 = State('C')
        state1.add_transition('_', state2)
        state2.add_transition('_', state3)
        state3.add_transition('_', state1)

        is_finite = state1.is_finite()

        self.assertEqual(is_finite, True, 'State with empty multiple state loop does not return True when evaluating if finite')

    def test_letter_multiple_state_loop_returns_False_when_evaluating_if_finite(self):
        state1 = State('A')
        state2 = State('B')
        state3 = State('C')
        state1.add_transition('_', state2)
        state2.add_transition('a', state3)
        state3.add_transition('_', state1)

        is_finite = state1.is_finite()

        self.assertEqual(is_finite, False, 'State with letter multiple state loop does not return False when evaluating if finite')



