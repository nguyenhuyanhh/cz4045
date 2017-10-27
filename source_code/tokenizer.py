"""Tokenizer."""

from __future__ import print_function, division

import re

# regexes
# TAG_REG = re.compile(r'(<\/?(a|p|pre|h[1-6]).*?>)')
TAG_REG = re.compile(
    r'</?(?!code)(?:[a-zA-Z]+[1-6]?)\s*(?:\w+?="[\W\w]+?")?\s*>')
CODE_REG = re.compile(r'<code>[\W\w]*?</code>')
#URL_REG = re.compile(
   # r'(?:https?://)?[-@:%.\+~#=\w]{2,256}\.[a-z]{2,6}\b(?:[-@:%\+\w.~#?&/=]*)(?!\()')
#FILE_REG = re.compile(
   # r'(?:(?:[A-z]:)?(?:\\[ A-z0-9\.]+)+)')
#FILE_REG = re.compile(
    #r'(?:(/[\w.]))|(?:[a-zA-Z]:\\(((?![<>:"/\\|?*]).)+((?<![ .])\\)?)*)')
URL_FILE_REG = re.compile(
    r'(?:\.{3})|(?:https?://)?[-@:%.\+~#=\w]{2,256}\.[a-z]{2,6}\b(?:[-@:%\+\w.~#?&/=]*)(?!\()|(?:(?:\.?\.)?(/(?:(?:\.\.?)|[\w][\w\.-_]*))+)|(?:\.\./?)|(?:\.{1,2}/\.{0,2})|(?:[a-zA-Z]:\\(?:(?:(?![<>:"/\\|?*]).)+(?:(?<![ .])\\)?)*)')
EXCEPTION_REG = re.compile(
    r'(?:[A-z0-9]+-[A-z0-9]+)|(?:\[.*?\])|(?:\{.*?\})|(?:i\.e\.?)|(?:e\.g\.?)|(?:(?:\w[\S]*?\.)?\w+\([\S]*?\))|(?:[A-z][A-z0-9]*\.[A-z][A-z0-9]*)|(?:_+[A-z0-9]+(?:_[A-z0-9]*)+)|(?:\$[A-z][A-z0-9]+)')
TOK_REG = re.compile(
    r'(?:\d+\.\d+)|(?:\w+)(?=n\'t)|(?:n\'t)|(?:\'s)|(?:[^\s\w])|(?:\w+)|(?:\w+\.\w+)')


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

    return (code_snippets + url_tokens + file_token +
            exception_tokens + word_tokens)


def tokenize_op(in_string, reg_obj, pos_list, tokens):
    """An atom tokenization operation, using a single regex.

    Arguments:
        in_string: str - the source string to search for tokens
        reg_obj: SRE_Pattern - compiled regex
        pos_list: list(list(int,int)) - list of start/end indexes to search
        tokens: dict - tokens dictionary
    Returns:
        ret_pos_list: list of start/end indexes of non-matches
        tokens - tokens dictionary
    """
    ret_pos_list = []

    for index in pos_list:
        # init start and end index to search
        start = index[0]
        end = index[1]
        non_match_bounds = [start]
        # only search for matches from start to end
        for match in reg_obj.finditer(in_string[start:end]):
            tokens[start + match.start()] = match.group()
            non_match_bounds += [start + match.start(), start + match.end()]
        non_match_bounds += [end]
        # append non-match bounds to return list
        ret_pos_list += [[non_match_bounds[2 * i], non_match_bounds[2 * i + 1]] for i in range(
            len(non_match_bounds) // 2) if non_match_bounds[2 * i] != non_match_bounds[2 * i + 1]]
    return ret_pos_list, tokens


def tokenize_v2(in_string):
    """A better tokenizer that returns tokens in-order."""
    # remove html tags
    in_string = TAG_REG.sub(' ', in_string)

    # init
    tokens = {}
    pos_list = [[0, len(in_string)]]
    regexes = [CODE_REG, URL_FILE_REG, EXCEPTION_REG, TOK_REG]

    # operations, one-by-one in that order
    for reg in regexes:
        pos_list, tokens = tokenize_op(in_string, reg, pos_list, tokens)
    return [tokens[k] for k in sorted(tokens)]


def evaluate(tokens, truth):
    """Evaluate the tokenization based on a truth, using precision-recall-f1.

    Arguments:
        tokens: list(str) - list of tokens generated by tokenizer
        truth: list(str) - the gold standard

    Returns:
        accr_cnt: int - number of accurate tokens
        precision, recall, f1_score: float - metrics
    """
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
    if not tokens_new or not truth_new:
        lcs_len = 0
    else:
        lcs_arr = [[0 for j in range(len(truth_new))]
                   for i in range(len(tokens_new))]
        for i in range(1, len(tokens_new)):
            for j in range(1, len(truth_new)):
                if tokens_new[i] == truth_new[j]:
                    lcs_arr[i][j] = lcs_arr[i - 1][j - 1] + 1
                else:
                    lcs_arr[i][j] = max(lcs_arr[i][j - 1], lcs_arr[i - 1][j])
        lcs_len = lcs_arr[len(tokens_new) - 1][len(truth_new) - 1]
    # evaluation stats
    accr_cnt = start_end_sim_cnt + lcs_len
    precision = accr_cnt / len(tokens)
    recall = accr_cnt / len(truth)
    f1_score = 2 * precision * recall / (precision + recall)
    return accr_cnt, precision, recall, f1_score


if __name__ == '__main__':
    test_string = '<p>my string.</p><code>sfdsfdsfds\n\n\n\n\n\n(sdfdsfd)</code> function() length-2 _test /nfs/an/disks/jj/home/dir/file.txt /dev/test/file.txt _test_test $1.00 _test_ test_test $interpolateProvider ash6.sad34sdf 555 obj.func() func(arg) oodp.method(arg) [hello] {world} [{testingdfig}] [e.g.] e.g i.e i.e. http:google.com google.com test.com fdsfg <code> 2nd code</code><a href="sdgdsfdsfds">fdsfsdfdsf</a>'
    test_string_2 = "... .. ../.. ../. ./.. . ./. ../ C:\\WINDOWS\\Hello\\txt.exe /dev/test ../.. ../../test /../test http://google.com https://googl.com https://google.com/query#div?q=hello&a=test http://google.com/query#div?q=hello&a=test google.com/query#div?q=hello&a=test"
    #assert set(tokenize(test_string)) == set(tokenize_v2(test_string))
    #print(tokenize_v2(test_string))
    print(tokenize_v2(test_string_2))
