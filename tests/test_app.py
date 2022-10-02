import unittest

from app import app, hola_mundo

class AppTestCase(unittest.TestCase):
    def test_prueba(self):
        self.assertEqual(0,0)