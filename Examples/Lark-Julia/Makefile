ALL: lark-grammar.ebnf jl_transformer.py 

%.py: %.nw
	notangle $< > $@
#
validation_builtins.jl: jl_transformer.nw
	notangle -RValidation_functions $< > $@
#
# We should replace the conversion to ebnf using python to one using Julia for
# cleanliness
lark-grammar.ebnf:  ../../annotated-grammar.rst
	egrep '^ {4,}' $< | ../Lark-Python/ebnf_to_lark.py > lark_grammar.ebnf
#
