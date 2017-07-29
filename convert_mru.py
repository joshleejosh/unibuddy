# -*- coding: utf-8 -*-
"""
Convert MRU data from the old flat-file list to the new JSON format.
"""

from mrubuddy import MRU

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('infile', type=str)
parser.add_argument('outfile', type=str)
args = parser.parse_args()

mru = MRU()
with open(args.infile) as fp:
    lines = fp.readlines()
    if lines[0].startswith('^_^MRULEN='):
        maxlen = int(lines[0].split('=')[1].strip())
        mru.resize(maxlen)
        del lines[0]
    for line in lines:
        mru.add(line.strip())
    print('Peeking at old data:')
    print(maxlen)
    print(lines[:4])
    print(lines[-4:])

mru.filename = args.outfile
mru.save()

# double check
print('Checking new data:')
chk = MRU(args.outfile)
chk.load()
print(chk.maxlen)
print(len(chk))
print(list(chk.q)[:4])
print(list(chk.q)[-4:])

