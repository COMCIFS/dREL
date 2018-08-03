#!/usr/bin/env python3
# A simple python program to convert the EBNF used in the annotated grammar
# into the EBNF recognised by Lark

def do_filter(textstream):
    import re
    no_equals = re.sub(" = "," : ",textstream)
    no_semis = re.sub(r";\s", "\n", no_equals)
    no_braces,n = re.subn(r"[^\"]{([^{}]+)}",r"(\1)*",no_semis)
    print("//# Number of braces found %d" % n)
    while n > 0:
        no_braces,n = re.subn(r"[^\"]{([^{}]+)}",r"(\1)*",no_braces)
        print("//# Number of braces found %d" % n)
    case_insensitive = re.sub(r'("[a-z]+")',r'\1i',no_braces)
    return case_insensitive
    
if __name__ == '__main__':
    import sys
    all_text = sys.stdin.read()
    result = do_filter(all_text)
    print(result)
