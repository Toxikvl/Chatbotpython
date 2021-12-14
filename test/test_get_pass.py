import unittest
from pass_gen import GoodGenPassword


class TestGenPass(unittest.TestCase):

    def test_10(self):
        gen = GoodGenPassword(10)
        self.assertEqual(len(gen.generate()), 10)

    def test_25(self):
        gen = GoodGenPassword(25)
        self.assertEqual(len(gen.generate()), 25)


if __name__ == '__main__':
    unittest.main()
