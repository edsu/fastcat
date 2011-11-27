import unittest

import fastcat

class FastcatTests(unittest.TestCase):

    def test_narrower(self):
        f = fastcat.FastCat()
        self.assertTrue("Functional languages" in f.narrower("Functional programming"))

    def test_broader(self):
        f = fastcat.FastCat()
        self.assertTrue("Computing" in f.broader("Computer programming"))

if __name__ == "__main__":
    f = fastcat.FastCat()
    f.load()
    unittest.main()
