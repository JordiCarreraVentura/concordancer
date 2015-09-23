##	Summary

Python script for extracting concordances (in the keyword-in-context sense of the term used in e.g. publishing[1]).

A linguistic concordance of a term (or sequence of terms) consists in each of its occurrences in a text sample, together with some fixed context of words preceding and following the match[2].


##	Description and Examples

This script provides an efficient dynamic-programming implementation for extracting concordances in Python. The script

1. can read both from text files and standard input (which allows to pipe data in and out in the context of BASH scripting workflows),
2. supports regular expressions[3], 
3. and offers the possibility to search using discrete word intervals, i.e., a span of undetermined words defined only by a minimum and maximum number of token slots that must be filled, for example:

	great 2-4 cinema

will match any sequences
- starting with *great*,
- followed by at least 2 words and at most 4 words, 
- and immediately followed by *cinema*.

For instance: *great night at the cinema* and *great for that cinema*, but not **great for cinema*.

For detailed usage instructions, please see below.

The script requires NLTK[4]'s 'wordpunct_tokenize' function; if unavailable, the code can be modified to use an alternative word tokenization method that takes a string as input and returns a list of strings (word tokens) as output.


###	References

[1] https://en.wikipedia.org/wiki/Key_Word_in_Context

[2] Conventionally, the matches are displayed so that the search term occupies always a central column (and the same), for readability. However, the present script is mainly focused on context extraction as free text and does not initially implement centered display.

[3] The regular expressions are evaluated against single tokens, not full lines, i.e., a regular expressions matching the whitespace character will not be matched during search. Instead, two consecutive regular expressions may be used to achieve a similar effect.

[4] http://www.nltk.org





##	Usage

###	Basic usage

If reading from standard input:

	concordances.py string[( interval)( -r) string, (...)]

Where *interval* has the form:
int-int


###	Options

flag | argument | description
--- | --- | ---
-c| None | Consider case (case is ignored by default)
-l| int| Specifies a window of 'int' words preceding the match to be returned as part of the concordance.
-r| int| Like '-l' for words following the match.
-q| None| Prints total number of input records and matches when EOF is reached.
-x| string| Does *not* wrap the next argument as '^argument$' when compiling it as a regular expression (i.e., if this option is not used, the search terms *will be* wrapped and matched from beginning to end, with no partial matches).
