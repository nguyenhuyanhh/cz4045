import re

url_reg = re.compile(r'(?:https?://)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b(?:[-a-zA-Z0-9@:%_\+.~#?&//=]*)')

code_reg = re.compile(r'<code>[\W\w]*?<\/code>')

tag_reg = re.compile(r'(<\/?(a|p|pre|h[1-6]).*?>)')

tok_reg = re.compile(r'((?:\d+\.\d+)|(?:\w+)(?:n\'t)|(?:n\'t)|(?:\'s)|(?:[^\s\w]+)|(?:\w+)|(?:\w+\.\w+))')

test_string = "<p>my string.</p><code>sfdsfdsfds\n\n\n\n\n\n(sdfdsfd)</code> http:google.com google.com test.com fdsfg <code> 2nd code</code><a href=sdgdsfdsfds>fdsfsdfdsf</a>"

def tokenize(in_string, url_reg, code_reg, tag_reg, tok_reg):
    no_tags = tag_reg.sub(' ', in_string) #remove html tags
    code_snippets = code_reg.findall(no_tags) #take out the code snippets
    no_code = code_reg.sub(' ', no_tags) #remove code snippet
    url_tokens = url_reg.findall(no_code) #take out urls
    no_url = url_reg.sub(' ', no_code) #remove urls
    word_tokens = tok_reg.findall(no_url) #tokenize! :)
    print(code_snippets+url_tokens+word_tokens)


tokenize(test_string, url_reg, code_reg, tag_reg, tok_reg)
