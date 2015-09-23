import copy

from copy import deepcopy as cp

class Concordancer:
    def __init__(self, args):
        self.args = args
        self.negations = set([])
        self.intervals = []
        self.pattern = []
        self.indexes = set([])
        deduction = 0
        for i, (boolean, target) in enumerate(self.args['targets']):
            if not boolean:
                at_least, up_to = self.__get_interval(target)
                deduction += 1
                self.intervals.append((i - deduction, at_least, up_to))
            else:
                self.indexes.add(len(self.pattern))
                self.pattern.append(target)
        self.__fill_missing_intervals()
        self.matches = []
    
    def __fill_missing_intervals(self):
        covered = set([i for i, _, _ in self.intervals])
        for j in sorted(list(self.indexes))[:-1]:
            if j not in covered:
                self.intervals.append((j, 0, 1))
        self.intervals.sort()

    def __get_interval(self, interval):
        at_least = interval.group(1)
        up_to = interval.group(2)
        if at_least:
            at_least = int(at_least)
        else:
            at_least = 2
        if up_to:
            up_to = int(up_to)
        else:
            up_to = 3
        return at_least, up_to

    def __call__(self, tokens):
        focus = 0
        target = self.pattern[focus]
        _, regex = target
        matches = []
        for i, token in enumerate(tokens):
            if regex.match(token):
                onset = i + 1
                match = [(i, token)]
                _matches = self.concordance(
                    cp(match), focus + 1, onset, tokens
                )
                for _match in _matches:
                    start = _match[0][0]
                    end = _match[-1][0]
                    window = self.frame(tokens, start, end)
                    matches.append(' '.join(window))
        return matches
    
    def frame(self, tokens, start, end):
        _start = start - self.args['left']
        _end = end + self.args['right'] + 1
        if _start < 0:
            _start = 0
        if _end > len(tokens):
            _end = len(tokens)
        return tokens[_start:_end]
    
    def concordance(self, matches, focus, prev_onset, space):
        if focus == len(self.pattern):
            return [matches]
        _, regex = self.pattern[focus]
        _, start, end = self.intervals[focus - 1]
        area = space[prev_onset + start:prev_onset + end]
        new_matches = []
        for i, token in enumerate(area):
            if regex.match(token):
                new_match = [(i + prev_onset + start, token)]            
                if self.is_last_position(focus):
                    new_matches.append(cp(matches) + new_match)
                else:
                    forward_matches = cp(matches) + new_match
                    onset = prev_onset + i + 1
                    newer_matches = self.concordance(
                        forward_matches, focus + 1, onset, space
                    )
                    new_matches += newer_matches
        return new_matches
    
    def is_last_position(self, focus):
        if focus == len(self.pattern) - 1:
            return True
        else:
            return False
        
