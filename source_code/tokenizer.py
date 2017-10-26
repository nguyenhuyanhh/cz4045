"""Tokenizer."""

from __future__ import print_function, division

import re

# regexes
# TAG_REG = re.compile(r'(<\/?(a|p|pre|h[1-6]).*?>)')
TAG_REG = re.compile(
    r'(</?(?!code)(?:[a-zA-Z]+[1-6]?)\s*(?:\w+?="[\W\w]+?")?\s*>)')
CODE_REG = re.compile(r'<code>[\W\w]*?</code>')
URL_REG = re.compile(
    r'(?:https?://)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b(?:[-a-zA-Z0-9@:%_\+.~#?&//=]*)')
TOK_REG = re.compile(
    r'((?:\d+\.\d+)|(?:\w+)(?:n\'t)|(?:n\'t)|(?:\'s)|(?:[^\s\w]+)|(?:\w+)|(?:\w+\.\w+))')


def tokenize(in_string, tag_reg, code_reg, url_reg, tok_reg):
    """Tokenize a string using our rules."""
    no_tags = tag_reg.sub(' ', in_string)  # remove html tags
    code_snippets = code_reg.findall(no_tags)  # take out the code snippets
    no_code = code_reg.sub(' ', no_tags)  # remove code snippet
    url_tokens = url_reg.findall(no_code)  # take out urls
    no_url = url_reg.sub(' ', no_code)  # remove urls
    word_tokens = tok_reg.findall(no_url)  # tokenize! :)
    print(code_snippets + url_tokens + word_tokens)


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
                lcs_arr[i][j] = max(lcs_arr[i, j - 1], lcs_arr[i - 1, j])
    # evaluation stats
    accr_len = start_end_sim_cnt + \
        lcs_arr[len(tokens_new) - 1][len(truth_new) - 1]
    precision = accr_len / len(tokens)
    recall = accr_len / len(truth)
    f1_score = 2 * precision * recall / (precision + recall)
    print('precision: {:.3f}, recall: {:.3f}, f1: {:.3f}'.format(
        precision, recall, f1_score))


if __name__ == '__main__':
    test_string = '<p>my string.</p><code>sfdsfdsfds\n\n\n\n\n\n(sdfdsfd)</code> http:google.com google.com test.com fdsfg <code> 2nd code</code><a href="sdgdsfdsfds">fdsfsdfdsf</a>'
    test_string_2 = "<blockquote> 3<a and b>5 </a></blockquote> hello \n world <h1></h1>"
    tokenize(test_string, TAG_REG, CODE_REG, URL_REG, TOK_REG)
    tokenize(test_string_2, TAG_REG, CODE_REG, URL_REG, TOK_REG)

    tokens = ['1', '3', 'a', 'hdytuiwegduig', '<code></code>']
    truth = ['1', '3', 'ahdytuiwegduig', '<code></code>']
    evaluate(tokens, truth)
