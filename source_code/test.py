"""Tokenizer test suite."""

import unittest

from tokenizer import tokenize_v2, evaluate


class TokenizerTest(unittest.TestCase):
    """Test cases for tokenizer."""

    def test_remove_html_tags(self):
        self.assertEqual(tokenize_v2('<p>hello</p>'), ['hello'])
        self.assertEqual(tokenize_v2('<h1>hello</h1>'), ['hello'])

    def test_non_html_tags(self):
        self.assertEqual(tokenize_v2('a<3 h>1'), [
                         'a', '<', '3', 'h', '>', '1'])
        self.assertEqual(tokenize_v2('a<b h>1'), [
                         'a', '<', 'b', 'h', '>', '1'])

    def test_white_spaces(self):
        self.assertEqual(tokenize_v2(' \n \t \r '), [])

    def test_white_spaces_tokens(self):
        self.assertEqual(tokenize_v2('      hello       '), ['hello'])

    def test_code_empty(self):
        self.assertEqual(tokenize_v2('<code></code>'), ['<code></code>'])

    def test_code_block(self):
        self.assertEqual(tokenize_v2('<code>eval()</code>'),
                         ['<code>eval()</code>'])

    def test_code_block_white_space(self):
        self.assertEqual(tokenize_v2('<code> eval() </code>'),
                         ['<code> eval() </code>'])

    def test_code_block_tokens(self):
        self.assertEqual(tokenize_v2('code<code>eval()</code>'),
                         ['code', '<code>eval()</code>'])

    def test_file_path_unix(self):
        self.assertEqual(tokenize_v2('/home/nhanh/hello.txt'),
                         ['/home/nhanh/hello.txt'])

    def test_file_path_windows(self):
        self.assertEqual(tokenize_v2('C:\\WINDOWS\\Hello\\txt.exe'),
                         ['C:\\WINDOWS\\Hello\\txt.exe'])

    def test_file_path_windows_space(self):
        self.assertEqual(tokenize_v2('C:\\Program Files\\Hello\\txt.exe'),
                         ['C:\\Program Files\\Hello\\txt.exe'])

    def test_url(self):
        self.assertEqual(tokenize_v2('https://google.com'),
                         ['https://google.com'])
        self.assertEqual(tokenize_v2('http://google.com'),
                         ['http://google.com'])

    def test_url_without_http(self):
        self.assertEqual(tokenize_v2('google.com'), ['google.com'])

    def test_round_brackets(self):
        self.assertEqual(tokenize_v2('(hello)'), ['(', 'hello', ')'])

    def test_square_brackets(self):
        self.assertEqual(tokenize_v2('[hello]'), ['[hello]'])

    def test_curly_brackets(self):
        self.assertEqual(tokenize_v2('{hello}'), ['{hello}'])

    def test_word_tokens(self):
        self.assertEqual(tokenize_v2('hello world'), ['hello', 'world'])

    def test_not_tokens(self):
        self.assertEqual(tokenize_v2("don't"), ['do', "n't"])
        self.assertEqual(tokenize_v2("doesn't"), ['does', "n't"])
        self.assertEqual(tokenize_v2("isn't"), ['is', "n't"])
        self.assertEqual(tokenize_v2("aren't"), ['are', "n't"])

    def test_contractions(self):
        self.assertEqual(tokenize_v2("he's"), ['he', "'s"])
        self.assertEqual(tokenize_v2("she's"), ['she', "'s"])
        self.assertEqual(tokenize_v2("it's"), ['it', "'s"])

    def test_possesive(self):
        self.assertEqual(tokenize_v2("John's"), ['John', "'s"])

    def test_number_tokens(self):
        self.assertEqual(tokenize_v2('123 123.15'), ['123', '123.15'])

    def test_currency(self):
        self.assertEqual(tokenize_v2('$1.00'), ['$', '1.00'])
        self.assertEqual(tokenize_v2('$100'), ['$', '100'])

    def test_dollar_expr(self):
        self.assertEqual(tokenize_v2('$test'), ['$test'])


class EvaluateTest(unittest.TestCase):
    """Test cases for evaluation function."""

    def test_full_similarity(self):
        tokens = ['1', '3', 'a']
        truth = ['1', '3', 'a']
        self.assertEqual(evaluate(tokens, truth), (3, 1, 1, 1))

    def test_diff_start(self):
        tokens = ['x', '1', '3', 'a']
        truth = ['1', '3', 'a']
        test, _, _, _ = evaluate(tokens, truth)
        self.assertEqual(test, 3)

    def test_diff_end(self):
        tokens = ['1', '3', 'a', 'b']
        truth = ['1', '3', 'a']
        test, _, _, _ = evaluate(tokens, truth)
        self.assertEqual(test, 3)

    def test_diff_mid(self):
        tokens = ['1', '3', 'a', 'hello', 'b']
        truth = ['1', '3', 'ahello', 'b']
        test, _, _, _ = evaluate(tokens, truth)
        self.assertEqual(test, 3)


if __name__ == '__main__':
    unittest.main()
