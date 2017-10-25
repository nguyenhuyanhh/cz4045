"""Tokenizer."""

from __future__ import print_function

import re

# regexes
# TAG_REG = re.compile(r'(<\/?(a|p|pre|h[1-6]).*?>)')
TAG_REG = re.compile(
    r'(</?(?!code)(?:[a-zA-Z]+[1-6]?)\s*(?:\w+?="[\W\w]+?")?\s*>)')
CODE_REG = re.compile(r'<code>[\W\w]*?</code>')
URL_REG = re.compile(
    r'(?:https?://)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b(?:[-a-zA-Z0-9@:%_\+.~#?&//=]*)')
EXCEPTION_REG = re.compile(
    r'((?:\[.*?\])|(?:\{.*?\})|(?:i\.e\.?)|(?:e\.g\.?)|(?:(?:\w.*?\.)?\w+\(.*?\)))')
TOK_REG = re.compile(
    r'((?:\d+\.\d+)|(?:\w+)(?:n\'t)|(?:n\'t)|(?:\'s)|(?:[^\s\w]+)|(?:\w+)|(?:\w+\.\w+))')


def tokenize(in_string, tag_reg, code_reg, url_reg, exception_reg, tok_reg):
    """Tokenize a string using our rules."""
    no_tags = tag_reg.sub(' ', in_string)  # remove html tags
    code_snippets = code_reg.findall(no_tags)  # take out the code snippets
    no_code = code_reg.sub(' ', no_tags)  # remove code snippet
    url_tokens = url_reg.findall(no_code)  # take out urls
    no_url = url_reg.sub(' ', no_code)  # remove urls
    exception_tokens = exception_reg.findall(no_url)    #take out exceptions
    no_exception = exception_reg.sub(" ", no_url)
    word_tokens = tok_reg.findall(no_exception)  # tokenize! :)
    print(code_snippets + url_tokens + exception_tokens + word_tokens)


if __name__ == '__main__':
    test_string = '<p>my string.</p><code>sfdsfdsfds\n\n\n\n\n\n(sdfdsfd)</code> function() obj.func() func(arg) oodp.method(arg) [hello] {world} [{testingdfig}] [e.g.] e.g i.e i.e. http:google.com google.com test.com fdsfg <code> 2nd code</code><a href="sdgdsfdsfds">fdsfsdfdsf</a>'
    test_string_2 = "<blockquote> 3<a and b>5 </a></blockquote> hello \n world <h1></h1>"
    tokenize(test_string, TAG_REG, CODE_REG, URL_REG, EXCEPTION_REG, TOK_REG)
    tokenize(test_string_2, TAG_REG, CODE_REG, URL_REG, EXCEPTION_REG, TOK_REG)
