# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys, os.path
import unittest
import unibuddy.fontquery

class FontqueryText(unittest.TestCase):
    def setUp(self):
        if sys.version_info < (3, 0):
            self.assertCountEqual = self.assertItemsEqual

    def test_charinfo(self):
        # dummy glyph IDs here, see test_read for real tests
        c7 = unibuddy.fontquery.CharInfo(0x4DD7, '')
        c7b = unibuddy.fontquery.CharInfo(0x4DD7, 'uniXXXX')
        c6 = unibuddy.fontquery.CharInfo(0x4DD6, '')
        c8 = unibuddy.fontquery.CharInfo(0x4DD8, '')

        self.assertEqual(c7.char, '䷗')
        self.assertEqual(c7.name, 'HEXAGRAM FOR RETURN')
        self.assertEqual(c7.category, 'So')
        self.assertEqual(c7.block, 'Yijing Hexagram Symbols')

        # comparisons only check the unicode value, not any other attributes
        self.assertEqual(c7, c7b)
        self.assertLess(c6, c7)
        self.assertGreater(c7, c6)
        a = [c7, c6, c8]
        self.assertCountEqual(sorted(a), [c6, c7, c8])

    def test_read(self):
        fn = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'FSEX300.ttf'))
        fname, glyphs, chars = unibuddy.fontquery.query_font(fn)
        self.assertEqual(fname, 'Fixedsys Excelsior 3.01')
        self.assertEqual(len(glyphs.keys()), 5993)
        self.assertEqual(len(chars), 6172)

        ci = chars[4128]
        self.assertEqual(ci.code, 19927)
        self.assertEqual(ci.name, 'HEXAGRAM FOR RETURN')
        self.assertEqual(ci.category, 'So')
        self.assertEqual(ci.block, 'Yijing Hexagram Symbols')
        self.assertEqual(ci.glyphid, 'uni4DD7')
        self.assertIsNotNone(ci.glyph)

    def test_filter(self):
        ffilter = lambda code: 0x4DC0 <= code <= 0x4DFF
        fn = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'FSEX300.ttf'))
        fname, glyphs, chars = unibuddy.fontquery.query_font(fn, ffilter)
        self.assertEqual(len(chars), 64)
        self.assertEqual(min(c.code for c in chars), 0x4DC0)
        self.assertEqual(max(c.code for c in chars), 0x4DFF)
        # Glyph set is the full set regardless of the filter
        self.assertEqual(len(glyphs.keys()), 5993)
        self.assertEqual(fname, 'Fixedsys Excelsior 3.01')

