import unittest

from homework import KnowledgeBase


class TestKnowledgeBase(unittest.TestCase):
    def test_parse(self):
        kb = KnowledgeBase()
        ast = kb._parse('~G(y, H(z)) => I(B) & J(C)')
        self.assertEqual([
            '|',
            ['~', ['~', ['G', 0, ['H', 1]]]],
            ['&', ['I', 'B'], ['J', 'C']]
        ], ast)
        self.assertEqual(2, kb._next_var_id)


if __name__ == '__main__':
    unittest.main()
