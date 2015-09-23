import nltk
import os
import re

from nltk import wordpunct_tokenize as tokenizer

INTERVAL = re.compile('^([0-9]+)?\-([0-9]+)?$')

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
    
    args = args[1:]
    while args:
        arg = args.pop(0)
        if arg[0] == '-' and len(arg) > 2:
            pargs = ['-%s' % char for char in arg[1:]]
        else:
            pargs = [arg]
        for arg in pargs:
            interval = INTERVAL.match(arg)
            if arg == '-c':
                arguments['ignorecase'] = False
            elif arg == '-l':
                arguments['left'] = int(args.pop(0))
            elif arg == '-r':
                arguments['right'] = int(args.pop(0))
            elif os.path.exists(arg):
                arguments['input'] = arg
            elif arg == '-x':
                arguments['targets'].append((True, args.pop(0)))
            elif arg == '-q':
                arguments['counts'] = True
            elif interval:
                arguments['targets'].append((False, interval))
            else:
                arguments['targets'].append((True, wrap_word(arg)))
    
    compile(arguments)
    
    return arguments


def wrap_word(string):
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
