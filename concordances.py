#!/usr/bin/env python
import sys

from tools import (
    parseargs,
    tokenizer
)

from Concordancer import Concordancer


def decode(line):
    if isinstance(line, bytes):
        try:
            return line.decode('utf-8')
        except UnicodeDecodeError:
            return line.decode('utf-8', errors='replace')
    return line


def main(argv):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass

    args = parseargs(argv)
    concordancer = Concordancer(args)
    lines = 0
    matches = 0

    if args['input']:
        rd = open(args['input'], 'r', encoding='utf-8')
    else:
        rd = sys.stdin

    try:
        for line in rd:
            lines += 1
            tokens = tokenizer(decode(line).strip())
            concordances = concordancer(tokens)
            for concordance in concordances:
                matches += 1
                sys.stdout.write('%d:%s\n' % (lines, concordance))
    finally:
        if args['input']:
            rd.close()

    if args['counts']:
        print('records:%d matches:%d' % (lines, matches))


if __name__ == '__main__':
    main(sys.argv)
