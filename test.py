import unittest

import fastcat

class FastcatTests(unittest.TestCase):
    
    def test_narrower(self):
        self.assertTrue("Functional languages" in fastcat.narrower("Functional programming"))

    def test_broader(self):
        self.assertTrue("Computing" in fastcat.broader("Computer programming"))

if __name__ == "__main__":
    unittest.main()
