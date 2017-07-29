# -*- coding: utf-8 -*-
"""
Query a font for info about the characters it includes.
"""
from __future__ import unicode_literals
from builtins import filter
import os.path
from itertools import chain
from fontTools.ttLib import TTFont
from . import ord, chr, name, category, block

class CharInfo(object):
    def __init__(self, code, glid, glyphs=None):
        self.code = code
        self.char = chr(code)
        self.name = name(self.char, '')
        self.category = category(self.char)
        self.block = block(self.char)[2]

        # replace control and whitespace chars with something printable.
        #if self.category[0] in ('C', 'Z'):
        #    self.char = '&nbsp;'
        # give combining marks some blanks to combine with.
        #if self.category[0] == 'M':
        #    self.char = ' %s '%self.char

        # calc glyph metrics
        self.glyphid = glid
        self.glyph = None
        if glyphs:
            self.glyph = glyphs[self.glyphid]
            self.glyph._glyph.recalcBounds(glyphs._glyphs)

    def __str__(self):
        return '0x%x|%s|%s'%(self.code, self.name, self.char)
    def __eq__(self, o):
        return self.code == o.code
    def __lt__(self, o):
        return self.code < o.code
    def __le__(self, o):
        return self.code <= o.code
    def __gt__(self, o):
        return self.code > o.code
    def __ge__(self, o):
        return self.code >= o.code
    def __hash__(self):
        return hash(self.code)
    def __cmp__(self, o):
        return cmp(self.code, o.code)

def query_font(fn, filterf=None):
    """
    Get supported code points out of a font file.

    `fn` is the path to the file.

    `filterf` is a function f(code) that returns True if we really want the char.

    Returns a 3-tuple (font name, list of glyphs, list of CharInfos)

    cf. http://stackoverflow.com/a/19438403
    """

    if not filterf:
        filterf = lambda u: True
    fn = os.path.realpath(fn)
    if not os.path.exists(fn):
        raise OSError('File [{}] does not exist'.format(fn))

    fontname = os.path.splitext(os.path.basename(fn))[0]
    chars = []
    glyphs = None

    try:
        font = TTFont(fn, 0, allowVID=0, ignoreDecompileErrors=True, fontNumber=0)
        names = filter(lambda n: n.nameID == 4, font['name'].names)
        fontname = next(names).string.decode('utf-8')

        if 'glyf' in font:
            glyphs = font.getGlyphSet()

        cmap = chain.from_iterable(
            (i
             for i in t.cmap.items()
             if filterf(i[0]))
            for t in font['cmap'].tables)

        for code, glyphid in cmap:
            chars.append(CharInfo(code, glyphid, glyphs=glyphs))

    finally:
        font.close()

    chars.sort(key=lambda c: c.code)
    return fontname, glyphs, chars

# ============================================================================

if __name__ == '__main__':
    import argparse
    from collections import defaultdict
    from . import BLOCKS, CATEGORIES

    parser = argparse.ArgumentParser()
    parser.add_argument('fontfile', help='Path to font file to inspect.')
    args = parser.parse_args()

    print(args.fontfile)
    fname, _, chars = query_font(args.fontfile)
    print(fname)
    mincode = min(c.code for c in chars)
    maxcode = max(c.code for c in chars)
    print('{} chars, codes from [0x{:04x}]-[0x{:04x}]'.format(len(chars), mincode, maxcode))

    blockcounts = defaultdict(int)
    catcounts = defaultdict(int)
    for c in chars:
        blockcounts[c.block] += 1
        catcounts[c.category] += 1

    print('Category counts:')
    for catid, catdesc in CATEGORIES.items():
        cct = catcounts[catid]
        if cct > 0:
            print('\t{}: {}'.format(catdesc, cct))
        
    print('Block counts:')
    for block in BLOCKS:
        k = block[2]
        bct = blockcounts[k]
        if bct > 0:
            print('\t{}: {}'.format(k, bct))

