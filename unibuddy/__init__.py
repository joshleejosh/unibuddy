# -*- coding: utf-8 -*-
"""
Extends the standard `unicodedata` module with additional helper functions.
"""
from __future__ import unicode_literals
from builtins import ord as _baseord
from builtins import chr as _basechr
import sys
from unicodedata import *
from .charts import BLOCKS, CATEGORIES

# ============================================================================

def ord(c):
    """
    Get the Unicode codepoint for a single character and/or fullwidth surrogate
    pair. Works in both python2 (with or without ucs4) and python3.
    cf. http://unicodebook.readthedocs.io/unicode_encodings.html
    """
    # If we're in py3, then we can handle whatever
    if sys.version_info >= (3, 0):
        return _baseord(c)

    # Or maybe py2 was compiled with ucs4 support
    if sys.maxunicode > 0xFFFF:
        return _baseord(c)

    # if this looks like a surrogate pair, then break it down
    if len(c) == 2 and \
            (0xD800 <= _baseord(c[0]) <= 0xDBFF) and \
            (0xDC00 <= _baseord(c[1]) <= 0xDFFF):
        oh = (_baseord(c[0]) & 0x03FF) << 10
        ol = (_baseord(c[1]) & 0x03FF)
        return 0x10000 + oh + ol

    return _baseord(c)

def chr(i):
    """
    Get the Unicode character for a codepoint, including fullwidth values above
    0xFFFF. Works in both python2 (with or without ucs4) and python3.
    cf. http://unicodebook.readthedocs.io/unicode_encodings.html
    """
    # If we're in py3, then chr will work for whatever
    if sys.version_info >= (3, 0):
        return _basechr(i)

    # Maybe we're lucky and py2 was compiled with ucs4 support for the full codespace
    if sys.maxunicode > 0xFFFF:
        return unichr(i)

    if i < 0x10000:
        return unichr(i)

    # Build a fullwidth character out of a surrogate pair
    i -= 0x10000
    ch = (i >> 10) | 0xD800
    cl = (i & 0x3FF) | 0xDC00
    return unichr(ch) + unichr(cl)


# ============================================================================

def block(c):
    """
    Get the Unicode block description for the character.

    Returns
        3-tuple: (min unicode value (int), max unicode value (int), block name (str))
    """
    u = ord(c)
    imin, imax = 0, len(BLOCKS)
    while imin < imax:
        i = (imin + imax) // 2
        b = BLOCKS[i]
        if b[0] > u:
            imax = i
        elif b[1] < u:
            imin = i + 1
        else:
            return b
    return (0, 0, '') # pragma: no cover (this line is unreachable/untestable unless BLOCKS is broken)

