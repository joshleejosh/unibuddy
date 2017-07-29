# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest
import unicodedata
import unibuddy

class UnibuddyTest(unittest.TestCase):
    def test_imports(self):
        self.assertEqual(unibuddy.unidata_version, unicodedata.unidata_version)
        self.assertEqual(unibuddy.name, unicodedata.name)
        self.assertEqual(unibuddy.category, unicodedata.category)
        # etc.

    def test_wideord(self):
        self.assertEqual(unibuddy.ord('c'), 0x63)
        self.assertEqual(unibuddy.ord('䷗'), 0x4DD7)
        # builtin ord() will fail in py2 if not compiled with the ucs4 option.
        self.assertEqual(unibuddy.ord('𐀀'), 0x10000)
        self.assertEqual(unibuddy.ord('🤓'), 0x1F913)

    def test_widechr(self):
        self.assertEqual(unibuddy.chr(0x63), 'c')
        self.assertEqual(unibuddy.chr(0x4DD7), '䷗')
        # builtin chr() will fail in py2 if not compiled with the ucs4 option.
        self.assertEqual(unibuddy.chr(0x10000), '𐀀')
        self.assertEqual(unibuddy.chr(0x1F913), '🤓')

    def test_block(self):
        self.assertEqual(unibuddy.block('c'), (0x0000, 0x007F, 'Basic Latin'))
        self.assertEqual(unibuddy.block('䷗'), (0x4DC0, 0x4DFF, 'Yijing Hexagram Symbols'))
        self.assertEqual(unibuddy.block('𐀀'), (0x10000, 0x1007F, 'Linear B Syllabary'))
        self.assertEqual(unibuddy.block('🤓'), (0x1F900, 0x1F9FF, 'Supplemental Symbols and Pictographs'))

        # edges
        self.assertEqual(unibuddy.block('\u0000'), (0x0000, 0x007F, 'Basic Latin', ))
        self.assertEqual(unibuddy.block('䶿'), (0x3400, 0x4DBF, 'CJK Unified Ideographs Extension A'))
        self.assertEqual(unibuddy.block('䷀'), (0x4DC0, 0x4DFF, 'Yijing Hexagram Symbols'))
        self.assertEqual(unibuddy.block('䷿'), (0x4DC0, 0x4DFF, 'Yijing Hexagram Symbols'))
        self.assertEqual(unibuddy.block('一'), (0x4E00, 0x9FFF, 'CJK Unified Ideographs'))
        self.assertEqual(unibuddy.block(unibuddy.chr(0x10FFFF)), ( 0x100000, 0x10FFFF, 'Supplementary Private Use Area-B', ))

    def test_category(self):
        for i in range(0x10FFFF):
            cat = unibuddy.category(unibuddy.chr(i))
            self.assertIn(cat, unibuddy.CATEGORIES)

