"""Tokenizer."""

from __future__ import print_function

import re

# regexes
# TAG_REG = re.compile(r'(<\/?(a|p|pre|h[1-6]).*?>)')
TAG_REG = re.compile(
    r'(</?(?!code)(?:[a-zA-Z]+[1-6]?)\s*(?:\w+?="[\W\w]+?")?\s*>)')
CODE_REG = re.compile(r'<code>[\W\w]*?</code>')
URL_REG = re.compile(
    r'(?:https?://)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b(?:[-a-zA-Z0-9@:%_\+.~#?&//=]*)(?!\()')
FILE_REG = re.compile(
    r'((?:(?:/[A-z0-9\_\-\.]+)+)|(?:(?:[A-z]:)?(?:\\[A-z0-9\.]+)+))')
EXCEPTION_REG = re.compile(
    r'((?:[A-z0-9]+-[A-z0-9]+)|(?:\[.*?\])|(?:\{.*?\})|(?:i\.e\.?)|(?:e\.g\.?)|(?:(?:\w[\S]*?\.)?\w+\([\S]*?\))|(?:(?:\w[\S]*?\.)?\w+[\S]*?)|(?:_+[A-z0-9]+(?:_[A-z0-9]*)+)|(?:\$[A-z][A-z0-9]+))')
TOK_REG = re.compile(
    r'((?:\d+\.\d+)|(?:\w+)(?:n\'t)|(?:n\'t)|(?:\'s)|(?:[^\s\w]+)|(?:\w+)|(?:\w+\.\w+))')


def tokenize(in_string, tag_reg, code_reg, url_reg, file_reg, exception_reg, tok_reg):
    """Tokenize a string using our rules."""
    no_tags = tag_reg.sub(' ', in_string)               # remove html tags
    code_snippets = code_reg.findall(no_tags)           # take out the code snippets
    no_code = code_reg.sub(' ', no_tags)                # remove code snippet
    file_token = file_reg.findall(no_code)              # extract paths
    no_file = file_reg.sub(' ',no_code)                 # remove paths
    url_tokens = url_reg.findall(no_file)               # take out urls
    no_url = url_reg.sub(' ', no_file)                  # remove urls
    exception_tokens = exception_reg.findall(no_url)    # take out exceptions
    no_exception = exception_reg.sub(" ", no_url)       # remove exceptions
    word_tokens = tok_reg.findall(no_exception)         # tokenize! :)
    print(code_snippets + url_tokens + file_token + exception_tokens + word_tokens)


if __name__ == '__main__':
    test_string = '<p>my string.</p><code>sfdsfdsfds\n\n\n\n\n\n(sdfdsfd)</code> function() length-2 _test /nfs/an/disks/jj/home/dir/file.txt /dev/test/file.txt _test_test $1.00 _test_ test_test $interpolateProvider ash6.sad34sdf 555 obj.func() func(arg) oodp.method(arg) [hello] {world} [{testingdfig}] [e.g.] e.g i.e i.e. http:google.com google.com test.com fdsfg <code> 2nd code</code><a href="sdgdsfdsfds">fdsfsdfdsf</a>'
    test_string_2 = "<blockquote> 3<a and b>5 </a></blockquote> /public \\file\\name\\test.txt /nfs/an/disks/jj/home/dir/file.txt C:\\Users\\Deon\\SchoolWork hello \n world <h1></h1>"
    tokenize(test_string, TAG_REG, CODE_REG, URL_REG, FILE_REG, EXCEPTION_REG, TOK_REG)
    tokenize(test_string_2, TAG_REG, CODE_REG, URL_REG, FILE_REG, EXCEPTION_REG, TOK_REG)
