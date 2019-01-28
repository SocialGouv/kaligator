import unittest
import os
dirname = os.path.dirname(__file__)
tests_dir = os.path.join(dirname, 'kali_extractor', 'tests')

if __name__ == '__main__':
    testsuite = unittest.TestLoader().discover(tests_dir, pattern="*tests.py")
    unittest.TextTestRunner(verbosity=1).run(testsuite)
