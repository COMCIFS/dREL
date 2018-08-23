#!/usr/bin/env python3
# A simple python program to convert the EBNF used in the annotated grammar
# into the EBNF recognised by Lark

# The list of productions in single-list has a question mark placed in
# front of them so that they are dropped from the parse tree if they
# simply repeat the lower node.

single_list = ['power','primary','factor','term','arith','comparison','not_test',
               'and_test','or_test']

def do_filter(textstream):
    import re
    no_equals = re.sub(" = "," : ",textstream)
    no_semis = re.sub(r";\s", "\n", no_equals)
    no_braces,n = re.subn(r"[^\"]{([^{}]+)}",r" (\1)*",no_semis)
    print("//# Number of braces found %d" % n)
    while n > 0:
        no_braces,n = re.subn(r"[^\"]{([^{}]+)}",r" (\1)*",no_braces)
        print("//# Number of braces found %d" % n)
    droppers = re.sub(r'("[a-z]+")',r'\1i',no_braces)
    # now insert question marks
    for dropper in single_list:
        regexp = r'^[ ]*(%s)' % dropper 
        droppers,n = re.subn(regexp,r"?\1",droppers,flags=re.MULTILINE)
        print("//# %s found %d times using %s" % (dropper,n,regexp))
    return droppers
    
if __name__ == '__main__':
    import sys
    all_text = sys.stdin.read()
    result = do_filter(all_text)
    print(result)
