#!/usr/bin/env python3
# Use the dREL EBNF to produce a parser using Lark, then
# test dREL code from the COMCIFS dictionary

from lark import Lark
from CifFile import CifDic

# Constants
grammar_file = "lark_grammar.ebnf"
dic_file = "/home/jrh/COMCIFS/cif_core/cif_core.dic"


def get_drel_parser(grammar_file):
    grammar = open(grammar_file).read()
    parser = Lark(grammar,start="input",parser="lalr",lexer="contextual")
    return parser

# if that succeeds, let's do dREL

def get_all_methods(dic_file):
    p = CifDic("/home/jrh/COMCIFS/cif_core/cif_core.dic",do_minimum=True)
    # extract all dREL methods
    has_meth = list([n for n in p.keys() if '_method.expression' in p[n]])
    has_meth.sort()
    return [(n,p[n]['_method.expression']) for n in has_meth]

def test_all_methods(parser,meth_list):
    for mn,(name,one_m) in enumerate(meth_list):
        for n,om in enumerate(one_m):   #multiple methods possible
            print("=== %s(%d) ===" % (name,mn))
            print(om)
            parser.lex(om+"\n")
            tree = parser.parse(om+"\n")
            print(tree.pretty())
        
if __name__=="__main__":
    p = get_drel_parser(grammar_file)
    m = get_all_methods(dic_file)
    test_all_methods(p,m)  
