from unittest import TestCase

from engine import Pente


class TestPente(TestCase):
    def test_capture(self):
        game = Pente()
        game.move('10K')
        game.move('10J')
        game.move('10L')
        game.move('10M')
        self.assertIsNone(game._state[9][9])
        self.assertIsNone(game._state[9][10])
        self.assertEqual(1, game.pairs_captured[0])

    def test_win_by_connect_five(self):
        game = Pente()
        game._state[9][7] = game._state[9][8] = game._state[9][10] = game._state[9][11] = True
        game.move('10K')
        self.assertTrue(game.result)