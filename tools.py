import nltk
import os
import re

from nltk import wordpunct_tokenize as tokenizer

INTERVAL = re.compile(r'^([0-9]+)?-([0-9]+)?$')

def parseargs(args):
    #    file             arg1
    #    consider case    -c
    #     counts              -q
    #    left, right      -l, -r
    #    words            ''
    #    regex            -x
    
    arguments = {
        'input': '',
        'targets': [],
        'left': 2,
        'right': 2,
        'ignorecase': True,
        'counts': False
    }
    
    args = list(args[1:])

    def next_value(flag):
        if not args:
            raise SystemExit("error: option '%s' requires an argument" % flag)
        return args.pop(0)

    while args:
        arg = args.pop(0)
        if arg[:1] == '-' and len(arg) > 2:
            pargs = ['-%s' % char for char in arg[1:]]
        else:
            pargs = [arg]
        for parg in pargs:
            interval = INTERVAL.match(parg)
            if parg == '-c':
                arguments['ignorecase'] = False
            elif parg == '-l':
                arguments['left'] = to_int(next_value('-l'), '-l')
            elif parg == '-r':
                arguments['right'] = to_int(next_value('-r'), '-r')
            elif os.path.exists(parg):
                arguments['input'] = parg
            elif parg == '-x':
                arguments['targets'].append((True, next_value('-x')))
            elif parg == '-q':
                arguments['counts'] = True
            elif interval:
                arguments['targets'].append((False, interval))
            else:
                arguments['targets'].append((True, wrap_word(parg)))
    
    compile(arguments)
    
    return arguments


def to_int(value, flag):
    try:
        return int(value)
    except ValueError:
        raise SystemExit("error: option '%s' expects an integer, got %r" % (flag, value))


def wrap_word(string):
    if not string:
        return string
    if string[0] != '^':
        string = '^%s' % string
    if string[-1] != '$':
        string = '%s$' % string
    return string


def compile(arguments):
    ignoring = arguments['ignorecase']
    compiled = []
    for boolean, target in arguments['targets']:
        if boolean:
            _regex = regex(target, ignoring)
        else:
            _regex = target
        compiled.append((boolean, _regex))
    arguments['targets'] = compiled
    return arguments


def regex(string, ignoring):
    if ignoring:
        return (string, re.compile(string, re.IGNORECASE))
    else:
        return (string, re.compile(string))
