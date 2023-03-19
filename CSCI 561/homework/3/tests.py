import unittest

from homework import KnowledgeBase


class TestKnowledgeBase(unittest.TestCase):
    def test_parse(self):
        ast = KnowledgeBase._parse('~G(y, H(z)) => I(B) & J(C)')
        self.assertEqual([
            '|',
            ['~', ['~', ['G', 0, ['H', 1]]]],
            ['&', ['I', 'B'], ['J', 'C']]
        ], ast)

    def test_negate(self):
        self.assertEqual(
            ['|', ['F', 'A'], 'B'],
            KnowledgeBase._negate(['|', ['~', ['~', ['F', 'A']]], 'B'], False)
        )
        self.assertEqual(
            ['|', ['~', 'A'], 'B'],
            KnowledgeBase._negate(['&', 'A', ['~', 'B']], True)
        )

    def test_distribute(self):
        self.assertEqual(
            (('A', ['~', 'C']), ('A', 'D'), (['~', 'B'], ['~', 'C']), (['~', 'B'], 'D')),
            KnowledgeBase._distribute(['|', ['&', 'A', ['~', 'B']], ['&', ['~', 'C'], 'D']])
        )


if __name__ == '__main__':
    unittest.main()
