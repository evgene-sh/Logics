import unittest
from main import algorithm


class TestAlgorithm(unittest.TestCase):

    def go(self, lm, path):
        for n, res in enumerate(algorithm(path)):
            with self.subTest(i=n):
                self.assertEqual(lm(res[0], res[1]), res[2], str(res[0]) + ' vs ' + str(res[1]))

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

        self.go(lm, 'testing/data/LevinMikenberg/')

    def test_LM_15_16(self):

        def lm(l1, l2):
            l1 = [int(l1[-3]), int(l1[-1])]
            l2 = [int(l2[-3]), int(l2[-1])]

            if l1 in [[3, 4], [4, 3]] and l2 in [[3, 4], [4, 3]]:
                return 'equivalent'

            return 'non-comparable'

        self.go(lm, 'testing/data/LM1516/')

    def test_LM_115(self):

        def lm(l1, l2):
            l1 = [l1[-3], l1[-1]]
            l2 = [l2[-3], l2[-1]]

            if l1 == ['1', '3']:
                return 'embeds'
            if l2 == ['1', '3']:
                return 'embedded'

            return 'equivalent'

        self.go(lm, 'testing/data/LM115/')

    def test_LM_17(self):

        def lm(l1, l2):
            return 'non-comparable'

        self.go(lm, 'testing/data/LM17/')

    def test_compare_LM(self):
        import csv
        with open('testing/results/LM.csv', 'r') as a, open('testing/results/LMalt.csv', 'r') as b:
            ra = csv.reader(a, delimiter=',')
            rb = csv.reader(b, delimiter=',')
            for rowa, rowb in zip(ra, rb):
                with self.subTest():
                    self.assertEqual(rowa[2], rowb[2], rowa[0] + ' ' + rowa[1])
