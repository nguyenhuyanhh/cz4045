"""Tokenizer."""

from __future__ import print_function, division

import re

# regexes

#HTML Tag filtering regex
TAG_REG = re.compile(
    r'</?(?!code)(?:[a-zA-Z]+[1-6]?)\s*(?:\w+?="[\W\w]+?")?\s*>')

#Code block regex
CODE_REG = re.compile(r'<code>[\W\w]*?</code>')

#Regex to recognise URL patterns, file paths for both linux and windows
URL_FILE_REG = re.compile(
    r'(?:\.{3})|' + #recognise "..." here, else it will be treated as linux command ".." and "."
    r'(?:https?://)?[-@:%.\+~#=\w]{2,256}\.[a-z]{2,6}\b(?:[-@:%\+\w.~#?&/=]*)(?!\()|' + #URL extractor
    r'(?:(?:\.?\.)?(/(?:(?:\.\.?)|[\w][\w\.-_]*))+)|' + #Linux paths
    r'(?:\.(?:(?:\./?)|(?:/\.?\.?)))|' + # combinations of .. and . and /.. and /.
    r'(?:(?:[A-z]:)(?:\\[^<>\:"/\\\|\?\*]+ ?[^<>\:"/\\\|\?\* ]+)*\\(?:[^<>\:"/\\\|\?\*]+(?: [^<>\:"/\\\|\?\* ]+)*\.[\w]+\b))|' +    #windows path recognizer
    r'(?:[A-z]:\\)')    #windows path which only contains drive, e.g C:\

#Regex to recognise exceptions
EXCEPTION_REG = re.compile(
    r'(?:[A-z0-9]+-[A-z0-9]+)|' +   #tokens such as "h3ll0-w0rld"
    r'(?:\[.*?\])|' +   #tokens such as [{(this is a token)}]
    r'(?:\{.*?\})|' +   #tokens such as {[(this is a token)]}
    r'(?:i\.e\.?)|' +   #i.e(.)
    r'(?:e\.g\.?)|' +   #e.g(.)
    r'(?:(?:\w[\S]*?\.)?\w+\([ \S]*?\))|' +  #function calls such as "hello.world(args)", "world()"
    r'(?:[A-z0-9]+\.[A-z0-9]+)|' +    #attributes of objects such as "string.length"
    r'(?:_+[A-z0-9]+(?:_[A-z0-9]*)+)|' +    #words with underscore at the start, between or at the end
    r'(?:\$[A-z][A-z0-9]+)')    #Words such as $interpolatorTest

#Regex to recognise common language words
TOK_REG = re.compile(
    r'(?:\d+\.?\d+)|' +      #recognise numbers such as 100, 100.00
    r'(?:\w+)(?=n\'t)|' +   #taking words with "n't" at the end without the "n't"
    r'(?:n\'t)|' +          #taking out the "n't" seperately
    r'(?:\'((?:ve)|(?:d)|(?:s)|(?:re)))|' +           #contractions in english language
    r'(?:[^\s\w])|' +       #punctuations
    r'(?:\w+)')             #normal words


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
print(tokenize_v2("i've he'd"))
