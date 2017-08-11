# -*- coding: utf-8 -*-
"""
Run unit test suite and report on source coverage.
"""

import os, unittest
import coverage

if __name__ == '__main__':
    tstd = os.path.realpath(os.path.dirname(__file__))
    srcd = os.path.realpath(os.path.join(tstd, '..', 'unibuddy'))

    coverer = coverage.Coverage(source=(srcd,),
                                omit=(os.path.join(srcd, '__main__.py'),))
    coverer.exclude('def main\(\):')
    coverer.exclude('if __name__ == \'__main__\':')
    coverer.start()

    # -----------------------------------------------
    loader = unittest.defaultTestLoader
    suite = loader.discover(tstd)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
    # -----------------------------------------------

    coverer.stop()
    coverer.save()
    coverer.report(show_missing=True)

