"""Tokenizer."""

from __future__ import print_function, division

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


def tokenize(in_string):
    """Tokenize a string using our rules."""
    no_tags = TAG_REG.sub(' ', in_string)               # remove html tags
    # take out the code snippets
    code_snippets = CODE_REG.findall(no_tags)
    no_code = CODE_REG.sub(' ', no_tags)                # remove code snippet
    file_token = FILE_REG.findall(no_code)              # extract paths
    no_file = FILE_REG.sub(' ', no_code)                 # remove paths
    url_tokens = URL_REG.findall(no_file)               # take out urls
    no_url = URL_REG.sub(' ', no_file)                  # remove urls
    exception_tokens = EXCEPTION_REG.findall(no_url)    # take out exceptions
    no_exception = EXCEPTION_REG.sub(" ", no_url)       # remove exceptions
    word_tokens = TOK_REG.findall(no_exception)         # tokenize! :)
    print(code_snippets + url_tokens + file_token +
          exception_tokens + word_tokens)


def evaluate(tokens, truth):
    """Evaluate the tokenization based on a truth, using precision-recall-f1."""
    # calculate length of longest common subsequence
    start = 0
    start_end_sim_cnt = 0
    tok_end = len(tokens)
    truth_end = len(truth)
    # match tokens at beginning of both sequences
    while start < tok_end and start < truth_end and tokens[start] == truth[start]:
        start_end_sim_cnt += 1
        start += 1
    # match tokens at end of both sequences
    while start < tok_end and start < truth_end and tokens[tok_end - 1] == truth[truth_end - 1]:
        tok_end -= 1
        truth_end -= 1
        start_end_sim_cnt += 1
    # find the LCS length of the middle
    tokens_new = tokens[start:tok_end]
    truth_new = truth[start:truth_end]
    lcs_arr = [[0 for j in range(len(truth_new))]
               for i in range(len(tokens_new))]
    for i in range(1, len(tokens_new)):
        for j in range(1, len(truth_new)):
            if tokens_new[i] == truth_new[j]:
                lcs_arr[i][j] = lcs_arr[i - 1][j - 1] + 1
            else:
                lcs_arr[i][j] = max(lcs_arr[i][j - 1], lcs_arr[i - 1][j])
    # evaluation stats
    accr_len = start_end_sim_cnt + \
        lcs_arr[len(tokens_new) - 1][len(truth_new) - 1]
    precision = accr_len / len(tokens)
    recall = accr_len / len(truth)
    f1_score = 2 * precision * recall / (precision + recall)
    print('precision: {:.3f}, recall: {:.3f}, f1: {:.3f}'.format(
        precision, recall, f1_score))


if __name__ == '__main__':
    test_string = '<p>my string.</p><code>sfdsfdsfds\n\n\n\n\n\n(sdfdsfd)</code> function() length-2 _test /nfs/an/disks/jj/home/dir/file.txt /dev/test/file.txt _test_test $1.00 _test_ test_test $interpolateProvider ash6.sad34sdf 555 obj.func() func(arg) oodp.method(arg) [hello] {world} [{testingdfig}] [e.g.] e.g i.e i.e. http:google.com google.com test.com fdsfg <code> 2nd code</code><a href="sdgdsfdsfds">fdsfsdfdsf</a>'
    test_string_2 = "<blockquote> 3<a and b>5 </a></blockquote> /public \\file\\name\\test.txt /nfs/an/disks/jj/home/dir/file.txt C:\\Users\\Deon\\SchoolWork hello \n world <h1></h1>"
    tokenize(test_string)
    tokenize(test_string_2)
    
    tok = ['1', '3', 'a', 'hdytuiwegduig',
           '<code></code>', 'hello', 'x', 'b']
    tru = ['1', '3', 'ahdytuiwegduig', '<code></code>', 'hello', 'a']
    evaluate(tok, tru)
