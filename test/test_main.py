import unittest
import main


class TestBot(unittest.TestCase):

    def test_filter(self):
        self.assertEqual(main.filter('1(2*3%ab c'), main.filter('12%3ab &c'))

    def test_match(self):
        self.assertEqual(main.match('привет!', 'Привет'), True)

    def test_intent(self):
        self.assertEqual(main.get_intent('привет!!!'), 'hello')


if __name__ == '__main__':
    unittest.main()
