# -*- coding:utf-8 -*-
import unittest

if __name__ == '__main__':
    loader = unittest.TestLoader()
    ts = loader.discover("test", "test_*.py", ".")

    unittest.TextTestRunner(verbosity=2).run(ts)
