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

    def test_evaluate(self):
        game = Pente()
        game._state[9][7] = game._state[9][8] = True
        self.assertEqual(20, game.evaluate())
        game._state[9][9] = True
        self.assertEqual(600, game.evaluate())
        game._state[9][10] = False
        self.assertEqual(300, game.evaluate())
        game.pairs_captured[1] = 1
        self.assertEqual(440, game.evaluate())
