# -*- coding: utf-8 -*-
"""
Dump information about a character.
"""
from __future__ import unicode_literals
import sys, argparse
from . import ord, name, category, block, CATEGORIES

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('chars', nargs='+', help='Character(s) to get info on.')
    args = parser.parse_args()
    for word in args.chars:
        if sys.version_info < (3, 0):
            word = word.decode('utf-8')
        for char in word:
            fmtstr = '[{code:d}/0x{code:x}]: [{name}] ({cat}) ({block}) [{char}]'
            info = {
                'char': char,
                'code': ord(char),
                'name': name(char, ''),
                'cat': CATEGORIES[category(char)],
                'block': block(char)[2],
            }
            print(fmtstr.format(**info))

