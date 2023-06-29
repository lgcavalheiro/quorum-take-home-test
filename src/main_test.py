import unittest
from .main import basic_init


class MainTest(unittest.TestCase):
    def test_basic_init(self):
        self.assertEqual(basic_init(), "Main.py ran")
