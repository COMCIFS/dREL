ALL: lark-grammar.ebnf py_transformer.py validation_builtins.py

%.py : %.nw
	notangle $< > $@
#
validation_builtins.py: py_transformer.nw
	notangle -RValidation_functions $< > $@
#
lark-grammar.ebnf:  ../../annotated-grammar.rst
	egrep '^ {4,}' $< | ./ebnf_to_lark.py > lark_grammar.ebnf
#
# Very complicated version
#
#pandoc -f rst -t plain --filter pandoc-cod-filter.py annotated-grammar.rst | ./ebnf_to_lark.py > lark_grammar.ebnf
