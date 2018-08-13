ALL: lark-grammar py_transformer.py

%.py : %.nw
	notangle $< > $@
#
lark-grammar:  annotated-grammar.rst
	pandoc -f rst -t plain --filter pandoc-cod-filter.py annotated-grammar.rst | ./ebnf_to_lark.py > lark_grammar.ebnf
#
