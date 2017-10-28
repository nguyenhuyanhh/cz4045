"""Tokenizer test suite."""

import unittest

from tokenizer import tokenize_v2, evaluate


class TokenizerTest(unittest.TestCase):
    """Test cases for tokenizer."""

    def test_remove_html_tags(self):
        """Test for removing simple html tags."""
        self.assertEqual(tokenize_v2('<b>hello</b>'), ['hello'])
        self.assertEqual(tokenize_v2(
            '<blockquote>hello</blockquote>'), ['hello'])
        self.assertEqual(tokenize_v2('<del>hello</del>'), ['hello'])
        self.assertEqual(tokenize_v2('<h1>hello</h1>'), ['hello'])
        self.assertEqual(tokenize_v2('<h2>hello</h2>'), ['hello'])
        self.assertEqual(tokenize_v2('<h3>hello</h3>'), ['hello'])
        self.assertEqual(tokenize_v2('<i>hello</i>'), ['hello'])
        self.assertEqual(tokenize_v2('<p>hello</p>'), ['hello'])
        self.assertEqual(tokenize_v2('<pre>hello</pre>'), ['hello'])

    def test_remove_html_tags_attr(self):
        """Test for removing html tags with attributes."""
        self.assertEqual(tokenize_v2(
            '<a href="https://google.com">hello</a>'), ['hello'])
        self.assertEqual(tokenize_v2(
            '<a href="https://google.com" rel="nofollow" >hello</a>'), ['hello'])

    def test_non_html_tags(self):
        """Test for not removing non-html (but look-alike) tags."""
        self.assertEqual(tokenize_v2('a<3 h>1'), [
            'a', '<', '3', 'h', '>', '1'])
        self.assertEqual(tokenize_v2('a<b h>1'), [
            'a', '<', 'b', 'h', '>', '1'])

    def test_white_spaces(self):
        """Test for recognizing white spaces."""
        self.assertEqual(tokenize_v2(' \n \t \r '), [])

    def test_white_spaces_tokens(self):
        """Test for recognizing tokens with white spaces."""
        self.assertEqual(tokenize_v2('      hello       '), ['hello'])

    def test_code_empty(self):
        """Test for recognizing empty code blocks."""
        self.assertEqual(tokenize_v2('<code></code>'), ['<code></code>'])

    def test_code_block(self):
        """Test for recognizing normal code blocks."""
        self.assertEqual(tokenize_v2('<code>eval()</code>'),
                         ['<code>eval()</code>'])

    def test_code_block_white_space(self):
        """Test for recognizing code blocks with white spaces."""
        self.assertEqual(tokenize_v2('<code> eval() </code>'),
                         ['<code> eval() </code>'])

    def test_code_block_tokens(self):
        """Test for recognizing code blocks with surrounding tokens."""
        self.assertEqual(tokenize_v2('code<code>eval()</code>more'),
                         ['code', '<code>eval()</code>', 'more'])

    def test_file_path_unix(self):
        """Test for recognizing Unix file paths."""
        self.assertEqual(tokenize_v2('/home/nhanh/hello.txt'),
                         ['/home/nhanh/hello.txt'])

    def test_file_path_unix_dir(self):
        """Test for Unix folder paths."""
        self.assertEqual(tokenize_v2('/home/nhanh/'), ['/home/nhanh/'])

    def test_file_path_unix_dots(self):
        """Test for Unix file paths using ."""
        self.assertEqual(tokenize_v2('.'), ['.'])
        self.assertEqual(tokenize_v2('./'), ['./'])
        self.assertEqual(tokenize_v2('./.'), ['./.'])
        self.assertEqual(tokenize_v2('/dev/.'), ['/dev/.'])
        self.assertEqual(tokenize_v2('./hello.txt'), ['./hello.txt'])

    def test_file_path_unix_double_dots(self):
        """Test for Unix file paths using .."""
        self.assertEqual(tokenize_v2('..'), ['..'])
        self.assertEqual(tokenize_v2('../'), ['../'])
        self.assertEqual(tokenize_v2('../..'), ['../..'])
        self.assertEqual(tokenize_v2('/dev/..'), ['/dev/..'])
        self.assertEqual(tokenize_v2('../hello.txt'), ['../hello.txt'])

    def test_file_path_unix_mixed_dots(self):
        """Test for Unix file paths using both . and .."""
        self.assertEqual(tokenize_v2('./..'), ['./..'])
        self.assertEqual(tokenize_v2('../.'), ['../.'])

    def test_file_path_unix_sent(self):
        """Test for recognizing Unix paths in a sentence."""
        self.assertEqual(tokenize_v2('open /dev/sda1 and write'),
                         ['open', '/dev/sda1', 'and', 'write'])

    def test_file_path_windows(self):
        """Test for recognizing Windows file paths."""
        self.assertEqual(tokenize_v2('C:\\WINDOWS\\Hello\\txt.exe'),
                         ['C:\\WINDOWS\\Hello\\txt.exe'])

    def test_file_path_windows_space(self):
        """Test for recognizing Windows file paths with spaces."""
        self.assertEqual(tokenize_v2('C:\\Program Files\\Hello\\txt.exe'),
                         ['C:\\Program Files\\Hello\\txt.exe'])

    def test_file_path_windows_sent(self):
        """Test for recognizing Windows file paths in a sentence."""
        self.assertEqual(tokenize_v2('open file: C:\\Program Files\\Hello\\txt.exe and do'), [
            'open', 'file', ':', 'C:\\Program Files\\Hello\\txt.exe', 'and', 'do'])

    def test_url(self):
        """Test for recognizing URLs."""
        self.assertEqual(tokenize_v2('https://google.com'),
                         ['https://google.com'])
        self.assertEqual(tokenize_v2('http://google.com'),
                         ['http://google.com'])

    def test_url_no_http(self):
        """Test for recognizing URLs without http(s)."""
        self.assertEqual(tokenize_v2('google.com'), ['google.com'])

    def test_url_attr(self):
        """Test for recognizing URLs with #, ?, &."""
        self.assertEqual(tokenize_v2(
            'google.com/query#div?q=hello&a=test'), ['google.com/query#div?q=hello&a=test'])

    def test_url_sent(self):
        """Test for recognizing URLs in a sentence."""
        self.assertEqual(tokenize_v2('browse https://google.com for news'),
                         ['browse', 'https://google.com', 'for', 'news'])

    def test_round_brackets(self):
        """Test for ()."""
        self.assertEqual(tokenize_v2('(hello)'), ['(', 'hello', ')'])

    def test_round_brackets_sent(self):
        """Test for () in a sentence."""
        self.assertEqual(tokenize_v2('his stuff is in (a bowl).'), [
            'his', 'stuff', 'is', 'in', '(', 'a', 'bowl', ')', '.'])

    def test_square_brackets(self):
        """Test for []."""
        self.assertEqual(tokenize_v2('[hello]'), ['[hello]'])

    def test_square_brackets_empty(self):
        """Test for empty []."""
        self.assertEqual(tokenize_v2('[]'), ['[]'])

    def test_square_brackets_sent(self):
        """Test for [] in a sentence."""
        self.assertEqual(tokenize_v2('declare a list [3,4]:'), [
            'declare', 'a', 'list', '[3,4]', ':'])

    def test_curly_brackets(self):
        """Test for {}."""
        self.assertEqual(tokenize_v2('{hello}'), ['{hello}'])

    def test_curly_brackets_sent(self):
        """Test for {} in a sentence."""
        self.assertEqual(tokenize_v2('declare a dict {3:4}:'), [
            'declare', 'a', 'dict', '{3:4}', ':'])

    def test_mixed_brackets(self):
        """Test for mixed brackets."""
        self.assertEqual(tokenize_v2('{3: [4,5]}'), ['{3: [4,5]}'])
        self.assertEqual(tokenize_v2('[4,{3:5}]'), ['[4,{3:5}]'])
        self.assertEqual(tokenize_v2('([4,5])'), ['(', '[4,5]', ')'])
        self.assertEqual(tokenize_v2('[(4,5)]'), ['[(4,5)]'])

    def test_word_tokens(self):
        """Test for normal word tokens."""
        self.assertEqual(tokenize_v2('hello world'), ['hello', 'world'])

    def test_simple_sentence(self):
        """Test a simple sentence with multiple punctuations."""
        self.assertEqual(tokenize_v2('"Hello, world!"'), [
            '"', 'Hello', ',', 'world', '!', '"'])

    def test_not_tokens(self):
        """Test for some n't tokens."""
        self.assertEqual(tokenize_v2("don't"), ['do', "n't"])
        self.assertEqual(tokenize_v2("doesn't"), ['does', "n't"])
        self.assertEqual(tokenize_v2("isn't"), ['is', "n't"])
        self.assertEqual(tokenize_v2("aren't"), ['are', "n't"])

    def test_contractions(self):
        """Test for 's contracttions."""
        self.assertEqual(tokenize_v2("he's"), ['he', "'s"])
        self.assertEqual(tokenize_v2("she's"), ['she', "'s"])
        self.assertEqual(tokenize_v2("it's"), ['it', "'s"])

    def test_possesive(self):
        """Test for possessive 's."""
        self.assertEqual(tokenize_v2("John's"), ['John', "'s"])

    def test_number_tokens(self):
        """Test for numerical tokens."""
        self.assertEqual(tokenize_v2('123 123.15'), ['123', '123.15'])

    def test_number_sent(self):
        """Test for numerical tokens inside a sentence."""
        self.assertEqual(tokenize_v2('we have 3 chickens'),
                         ['we', 'have', '3', 'chickens'])

    def test_currency(self):
        """Test for currency tokens."""
        self.assertEqual(tokenize_v2('$1.00'), ['$', '1.00'])
        self.assertEqual(tokenize_v2('$100'), ['$', '100'])

    def test_currency_sent(self):
        """Test for currency tokens in a sentence."""
        self.assertEqual(tokenize_v2('his salary is $10000 without commission'), [
            'his', 'salary', 'is', '$', '10000', 'without', 'commission'])

    def test_number_currency_sent(self):
        """Test for number and currency tokens in a sentence."""
        self.assertEqual(tokenize_v2('his 3 chickens cost $5 in total'), [
            'his', '3', 'chickens', 'cost', '$', '5', 'in', 'total'])

    def test_dollar_expr(self):
        """Test for $-expr that are not currencies (e.g. Bash variables)."""
        self.assertEqual(tokenize_v2('$test'), ['$test'])

    def test_dollar_expr_sent(self):
        """Test for $-expr in a sentence."""
        self.assertEqual(tokenize_v2('declare $test with a value of 3'), [
            'declare', '$test', 'with', 'a', 'value', 'of', '3'])

    def test_eg_ie(self):
        """Test for e.g. and i.e."""
        self.assertEqual(tokenize_v2('i.e.'), ['i.e.'])
        self.assertEqual(tokenize_v2('i.e'), ['i.e'])
        self.assertEqual(tokenize_v2('e.g.'), ['e.g.'])
        self.assertEqual(tokenize_v2('e.g'), ['e.g'])

    def test_eg_ie_sent(self):
        """Test for e.g. and i.e. in a sentence."""
        self.assertEqual(tokenize_v2('nouns e.g. Python i.e. the language'), [
            'nouns', 'e.g.', 'Python', 'i.e.', 'the', 'language'])

    def test_underscore(self):
        """Test for multi-word names with underscore."""
        self.assertEqual(tokenize_v2('hello_world'), ['hello_world'])

    def test_underscore_pre(self):
        """Test for names starting with underscore."""
        self.assertEqual(tokenize_v2('_hello'), ['_hello'])

    def test_underscore_post(self):
        """Test for names starting with underscore."""
        self.assertEqual(tokenize_v2('hello_'), ['hello_'])

    def test_underscore_all(self):
        """Test for names with underscore everywhere."""
        self.assertEqual(tokenize_v2('_hello_world_'), ['_hello_world_'])
        self.assertEqual(tokenize_v2('__main__'), ['__main__'])

    def test_underscore_sent(self):
        """Test for underscore names in a sentence."""
        self.assertEqual(tokenize_v2('declare variable hello_world of type string'), [
            'declare', 'variable', 'hello_world', 'of', 'type', 'string'])

    def test_function_simple(self):
        """Test for codes that live outside of <code> blocks."""
        self.assertEqual(tokenize_v2('eval()'), ['eval()'])
        self.assertEqual(tokenize_v2('str.replace()'), ['str.replace()'])

    def test_function_private(self):
        """Test for private functions."""
        self.assertEqual(tokenize_v2('_hello_world()'), ['_hello_world()'])

    def test_function_magic(self):
        """Test for magic functions."""
        self.assertEqual(tokenize_v2('__str__()'), ['__str__()'])

    def test_function_params_str(self):
        """Test for functions with string params."""
        self.assertEqual(tokenize_v2("str.replace('hello')"),
                         ["str.replace('hello')"])

    def test_function_params_int(self):
        """Test for functions with int params."""
        self.assertEqual(tokenize_v2('eval(1)'), ['eval(1)'])

    def test_function_params_name(self):
        """Test for functions with named params."""
        self.assertEqual(tokenize_v2('eval(int)'), ['eval(int)'])

    def test_function_params_list_dict(self):
        """Test for functions with list/dict params."""
        self.assertEqual(tokenize_v2('eval([1,2])'), ['eval([1,2])'])
        self.assertEqual(tokenize_v2('eval(["hello",2])'), [
            'eval(["hello",2])'])
        self.assertEqual(tokenize_v2('eval({1:2})'), ['eval({1:2})'])

    def test_function_params_keyword(self):
        """Test for functions with keyword params."""
        self.assertEqual(tokenize_v2('eval(key=1)'), ['eval(key=1)'])

    def test_function_sent(self):
        """Test for functions in a sentence."""
        self.assertEqual(tokenize_v2('declare functions fun1() and fun2() to'), [
            'declare', 'functions', 'fun1()', 'and', 'fun2()', 'to'])

    def test_class(self):
        """Test for classes."""
        self.assertEqual(tokenize_v2('TokenizerClass()'), ['TokenizerClass()'])
        self.assertEqual(tokenize_v2('TokenizerClass(object)'), [
            'TokenizerClass(object)'])
        self.assertEqual(tokenize_v2('TokenizerClass(object.Object)'), [
            'TokenizerClass(object.Object)'])

    def test_class_sent(self):
        """Test for classes in a sentence."""
        self.assertEqual(tokenize_v2('create class Token() to store tokens'), [
            'create', 'class', 'Token()', 'to', 'store', 'tokens'])

    def test_mixed_1(self):
        """Mixed test case 1."""
        in_string = '<p>my string.</p><code>sfdsfdsfds\n\n\n\n\n\n(sdfdsfd)</code> function()'
        res = ['my', 'string', '.',
               '<code>sfdsfdsfds\n\n\n\n\n\n(sdfdsfd)</code>', 'function()']
        self.assertEqual(tokenize_v2(in_string), res)

    def test_mixed_2(self):
        """Mixed test case 2."""
        in_string = 'length-2 _test /nfs/an/disks/jj/home/dir/file.txt /dev/test/file.txt'
        res = ['length-2', '_test',
               '/nfs/an/disks/jj/home/dir/file.txt', '/dev/test/file.txt']
        self.assertEqual(tokenize_v2(in_string), res)

    def test_mixed_3(self):
        """Mixed test case 3."""
        in_string = '_test_test $1.00 _test_ test_test $interpolateProvider ash6.sad34sdf'
        res = ['_test_test', '$', '1.00', '_test_',
               'test_test', '$interpolateProvider' 'ash6.sad34sdf']
        self.assertEqual(tokenize_v2(in_string), res)

    def test_mixed_4(self):
        """Mixed test case 4."""
        in_string = '555 obj.func() func(arg) oodp.method(arg) [hello] {world}'
        res = ['555', 'obj.func()', 'func(arg)', 'oodp.method(arg)',
               '[hello]', '{world}']
        self.assertEqual(tokenize_v2(in_string), res)

    def test_mixed_5(self):
        """Mixed test case 5."""
        in_string = '[{testingdfig}] [e.g.] e.g i.e i.e. http://google.com google.com'
        res = ['[{testingdfig}]', '[e.g.]', 'e.g', 'i.e',
               'i.e.', 'http://google.com', 'google.com']
        self.assertEqual(tokenize_v2(in_string), res)

    def test_mixed_6(self):
        """Mixed test case 6."""
        in_string = 'test.com fdsfg <code> 2nd code</code><a href="sdgdsfdsfds">fdsfsdfdsf</a>'
        res = ['test.com', 'fdsfg', '<code> 2nd code</code>', 'fdsfsdfdsf']
        self.assertEqual(tokenize_v2(in_string), res)

    def test_mixed_7(self):
        """Mixed test case 7 (a weird one)."""
        in_string = 'C:\\WINDOWS\\$Hello world\\-txt hahaha lol.exe testing c: d: 0: c:\\ 0:\\'
        res = ['C:\\WINDOWS\\$Hello world\\-txt hahaha lol.exe',
               'testing', 'c', ':', 'd', ':', '0', ':', 'c:\\', '0', ':', '\\']
        self.assertEqual(tokenize_v2(in_string), res)

    def test_mixed_8(self):
        """Mixed test case 8 (another weird one)."""
        in_string = 'C:\\.WINDOWS\\Hello world\\-txt.exe testing ... .. ../.. ../. ./.. . ./. ../'
        res = ['C:\\.WINDOWS\\Hello world\\-txt.exe', 'testing',
               '...', '..', '../..', '../.', './..', '.', './.', '../']
        self.assertEqual(tokenize_v2(in_string), res)

    def test_mixed_9(self):
        """Mixed test case 9."""
        in_string = 'C:\\WINDOWS\\Hello\\txt.exe testing /dev/test ../..' + \
            ' ../../test /../test http://google.com https://googl.com'
        res = ['C:\\WINDOWS\\Hello\\txt.exe', 'testing', '/dev/test', '../..',
               '../../test', '/../test', 'http://google.com', 'https://googl.com']
        self.assertEqual(tokenize_v2(in_string), res)

    def test_mixed_10(self):
        """Mixed test case 10."""
        in_string = 'https://google.com/query#div?q=hello&a=test' + \
            ' http://google.com/query#div?q=hello&a=test google.com/query#div?q=hello&a=test'
        res = ['https://google.com/query#div?q=hello&a=test',
               'http://google.com/query#div?q=hello&a=test', 'google.com/query#div?q=hello&a=test']
        self.assertEqual(tokenize_v2(in_string), res)


class EvaluateTest(unittest.TestCase):
    """Test cases for evaluation function."""

    def test_full_similarity(self):
        """Test for full similarity."""
        tokens = ['1', '3', 'a']
        truth = ['1', '3', 'a']
        self.assertEqual(evaluate(tokens, truth), (3, 1, 1, 1))

    def test_diff_start(self):
        """Test for two series with different starts."""
        tokens = ['x', '1', '3', 'a']
        truth = ['1', '3', 'a']
        test, _, _, _ = evaluate(tokens, truth)
        self.assertEqual(test, 3)

    def test_diff_end(self):
        """Test for two series with different ends."""
        tokens = ['1', '3', 'a', 'b']
        truth = ['1', '3', 'a']
        test, _, _, _ = evaluate(tokens, truth)
        self.assertEqual(test, 3)

    def test_diff_mid(self):
        """Test for two series with different parts in the middle."""
        tokens = ['1', '3', 'a', 'hello', 'b']
        truth = ['1', '3', 'ahello', 'b']
        test, _, _, _ = evaluate(tokens, truth)
        self.assertEqual(test, 3)


if __name__ == '__main__':
    unittest.main()
