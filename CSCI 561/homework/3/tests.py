import unittest

from homework import KnowledgeBase


class TestKnowledgeBase(unittest.TestCase):
    def test_parse(self):
        ast = KnowledgeBase._parse('~G(y, H(z)) => I(B) & J(C)')
        self.assertEqual((
            '|',
            ('~', ('~', ('G', 'y', ('H', 'z')))),
            ('&', ('I', 'B'), ('J', 'C'))
        ), ast)

    def test_negate(self):
        self.assertEqual(
            ('|', ('F', 'A'), 'B'),
            KnowledgeBase._negate(('|', ('~', ('~', ('F', 'A'))), 'B'), False)
        )
        self.assertEqual(
            ('|', ('~', 'A'), 'B'),
            KnowledgeBase._negate(('&', 'A', ('~', 'B')), True)
        )

    def test_distribute(self):
        self.assertEqual(
            (('A', ('~', 'C')), ('A', 'D'), (('~', 'B'), ('~', 'C')), (('~', 'B'), 'D')),
            KnowledgeBase._distribute(('|', ('&', 'A', ('~', 'B')), ('&', ('~', 'C'), 'D')))
        )

    def test_standardize_vars_apart(self):
        kb = KnowledgeBase()
        self.assertEqual(
            (('F', 0), ('~', ('F', 1))),
            kb._standardize_vars_apart((('F', 'x'), ('~', ('F', 'y'))))
        )

    def test_unify(self):
        sub = {}
        self.assertTrue(KnowledgeBase._unify(('F', 0, ('G', 0)), ('F', ('G', 1), 2), sub))
        self.assertEqual({0: ('G', 1), 2: ('G', ('G', 1))}, sub)

        sub = {}
        self.assertTrue(KnowledgeBase._unify(('F', 0, 1, 2, 3), ('F', 1, 2, 3, 4), sub))
        self.assertEqual({0: 4, 1: 4, 2: 4, 3: 4}, sub)

        self.assertFalse(KnowledgeBase._unify(('F', 0), ('F', ('F', 0)), {}))
        self.assertFalse(KnowledgeBase._unify(
            ('F', 0, ('G', 0)), ('F', ('G', 1), 1), {}
        ))


if __name__ == '__main__':
    unittest.main()
