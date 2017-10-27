"""Tokenizer test suite."""

import unittest

from tokenizer import tokenize_v2, evaluate


class TokenizerTest(unittest.TestCase):
    """Test cases for tokenizer."""

    def test_remove_html_tags(self):
        self.assertEqual(tokenize_v2('<p>hello</p>'), ['hello'])

    def test_non_html_tags(self):
        self.assertEqual(tokenize_v2('a<3 h>1'), [
                         'a', '<', '3', 'h', '>', '1'])
        self.assertEqual(tokenize_v2('a<b h>1'), [
                         'a', '<', 'b', 'h', '>', '1'])

    def test_white_spaces(self):
        self.assertEqual(tokenize_v2(' \n \t \r '), [])

    def test_white_spaces_tokens(self):
        self.assertEqual(tokenize_v2('      hello       '), ['hello'])

    def test_code_block(self):
        self.assertEqual(tokenize_v2('<code>eval()</code>'),
                         ['<code>eval()</code>'])

    def test_code_block_white_space(self):
        self.assertEqual(tokenize_v2('<code> eval() </code>'),
                         ['<code> eval() </code>'])

    def test_code_block_tokens(self):
        self.assertEqual(tokenize_v2('code<code>eval()</code>'),
                         ['code', '<code>eval()</code>'])

    def test_word_tokens(self):
        self.assertEqual(tokenize_v2('hello world'), ['hello', 'world'])

    def test_number_tokens(self):
        self.assertEqual(tokenize_v2('123 123.15'), ['123', '123.15'])


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
