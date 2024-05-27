import unittest

from src.org.mugbook.firearm import NullFirearm
from src.org.mugbook.mugbook import Mugbook


class MugbookTest(unittest.TestCase):
    mugbook = Mugbook("some/directory")
    def test_something(self):

        result = self.mugbook.path_to_firearm("some/path")
        self.assertEqual(NullFirearm(), result)  # add assertion here


if __name__ == '__main__':
    unittest.main()
