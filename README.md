# dREL
This repository is for developing comprehensive documentation for the dREL dictionary methods language.
dREL methods appear in dictionary data name definitions and are used to (re)calculate values that are
missing from data files based on other values in those data files.

The current canonical reference for dREL is Spadaccini, N., Castleden, I. R., du Boulay, D. and Hall, S. R.,
"dREL: A relational expression language for dictionary methods",  _J. Chem. Inf. Model._, 2012, **52** (8)
pp 1917-1925. https://dx.doi.org/10.1021/ci300076w, in particular the appendix.

A further source of information that extends the language compared to the paper are the methods contained in the 
DDLm version of the core cif dictionary.

Two implementations exist of dREL. One is included in the JsCifBrowser javascript software of Doug du Boulay (see 
https://github.com/COMCIFS/JsCifBrowser) and the other is bundled with the PyCIFRW software of James Hester 
(see https://bitbucket.org/jamesrhester/pycifrw). Neither can be considered to fully implement the specification
in the paper, but both handle most or all dREL methods in approved IUCr CIF dictionaries.

# Documentation

Documentation currently consists solely of `annotated_grammar.rst`, together with the paper mentioned above.

# Examples

All lines starting with 4 spaces or more in file `annotated_grammar.rst` can be extracted to create an
EBNF that is close to the ISO standard, with differences noted in the annotated grammar. The Makefile in the
Examples/Lark directory uses the annotated grammar and the Lark parser to create a fully-functional system
for translating dREL code to Python and recursively executing it when provided with a CIF data file.

A Julia implementation of dREL is available [here](https://github.com/jamesrhester/CIF_dREL.jl).

Further examples using different coding languages and CIF access libraries are welcome.
