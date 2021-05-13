import unittest
from main import algorithm


class TestAlgorithm(unittest.TestCase):

    def test_LM_1to4(self):

        def lm(l1, l2):
            l1 = [int(l1[-3]), int(l1[-1])]
            l2 = [int(l2[-3]), int(l2[-1])]

            if l1[0] == l1[1] and l2[0] == l2[1]:
                return 'non-comparable'
            if l1[0] == l1[1] and (l1[0] in l2 or l2 in [[3, 4], [4, 3]]):
                return 'embeds'
            if l2[0] == l2[1] and (l2[0] in l1 or l1 in [[3, 4], [4, 3]]):
                return 'embedded'
            if l1[0] == l2[1] and l2[0] == l1[1]:
                return 'equivalent'
            if l1 in [[3, 4], [4, 3]]:
                return 'embedded'
            if l2 in [[3, 4], [4, 3]]:
                return 'embeds'
            return 'non-comparable'

        for n, res in enumerate(algorithm('testing/data/LevinMikenberg/')):
            with self.subTest(i=n):
                self.assertEqual(lm(res[0], res[1]), res[2], str(res[0]) + ' vs ' + str(res[1]))

    def test_LM_15_16(self):

        def lm(l1, l2):
            l1 = [int(l1[-3]), int(l1[-1])]
            l2 = [int(l2[-3]), int(l2[-1])]

            if l1 in [[3, 4], [4, 3]] and l2 in [[3, 4], [4, 3]]:
                return 'equivalent'

            return 'non-comparable'

        for n, res in enumerate(algorithm('testing/data/LM1516/')):
            with self.subTest(i=n):
                self.assertEqual(lm(res[0], res[1]), res[2], str(res[0]) + ' vs ' + str(res[1]))

    def test_LM_115(self):

        def lm(l1, l2):
            l1 = [l1[-3], l1[-1]]
            l2 = [l2[-3], l2[-1]]

            if l1 == ['1', '3']:
                return 'embeds'
            if l2 == ['1', '3']:
                return 'embedded'

            return 'equivalent'

        for n, res in enumerate(algorithm('testing/data/LM115/')):
            with self.subTest(i=n):
                self.assertEqual(lm(res[0], res[1]), res[2], str(res[0]) + ' vs ' + str(res[1]))

# TODO make subtest printing right after its completion
