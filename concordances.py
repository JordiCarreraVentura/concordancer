#!/usr/bin/env python
import sys

from tools import (
    parseargs,
    tokenizer
)

from Concordancer import Concordancer

def decode(line):
    try:
        return line.decode('utf-8')
    except Exception:
        return line
    

if __name__ == '__main__':
    args = parseargs(sys.argv)
    concordancer = Concordancer(args)
    lines = 0
    matches = 0
    if args['input']:
        rd = open(args['input'], 'rb')
    else:
        rd = sys.stdin
    for line in rd:
        lines += 1
        tokens = tokenizer(decode(line).strip())
        concordances = concordancer(tokens)
        for concordance in concordances:
            matches += 1
            sys.stdout.write('%d:%s\n' % (lines, concordance.encode('utf-8')))

    if args['counts']:
        print 'records:%d matches:%d' % (lines, matches)
