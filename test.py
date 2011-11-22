import unittest

import cat

class CatTests(unittest.TestCase):
    
    def test_narrower(self):
        self.assertTrue("Functional languages" in cat.narrower("Functional programming"))

    def test_broader(self):
        self.assertTrue("Computing" in cat.broader("Computer programming"))

if __name__ == "__main__":
    unittest.main()
