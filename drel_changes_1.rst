Proposed changes to dREL, part I
================================

Introduction
------------

dREL is a machine-actionable language describing data relationships
and designed to be embedded in DDLm dictionaries. The language is
defined both explicitly in the dREL publication [1] and implicitly by
the dREL code appearing in the DDLm core CIF dictionary. Note that
the code in the core CIF dictionary significantly expands the language
presented in the paper, for example, by adding category methods.

The present changes are relatively trivial and intended to simplify
and clarify the syntax. Following proposals will be more substantial.

Proposal 1: underscores
-----------------------

The proposal: A leading underscore in front of a variable is optional,
and has no significance. Its use is deprecated.

Explanation
~~~~~~~~~~~

The dREL paper states that the value of a data name from a Set
category can be accessed by using the form `<category>.<name>` in a
dREL script, for example `cell.volume` (p 1919, "Data References in
dREL").  However, the dREL methods in the current core CIF dictionary
and the dREL paper almost always use a form with a leading underscore,
i.e. `_<category>.<name>`.

Discussion
~~~~~~~~~~

The paper does not explain the appearance of the underscore in the
example methods presented there. It is possible that the underscore is
provided as a way to disambiguate ordinary variables from dictionary
items; however, as a period character must appear in a dictionary
reference, and may not appear in a variable, such disambiguation is
unnecessary.  It is also important to note that the period character
is an operator in dREL, so the construction `cell.volume` is formally
referring to the `volume` column in the current packet of the `cell`
category.  In this context, the leading underscore is potentially
misleading.

The `with` statement is available to alias category names in any
situation where a category name may collide with a language keyword.

Proposal 2: newline is not significant
--------------------------------------

The proposal: newline should be treated as ordinary whitespace.

Explanation
~~~~~~~~~~~~

If newline is treated as ordinary whitespace it is not significant for
separating expressions.  However, the dREL paper Appendix, Section 4,
states that "dREL supports the following expression terminators:
... newline closes a line unless a balancing [bracket] is missing",
which may be construed as allowing newline to terminate an expression.

Discussion
~~~~~~~~~~

The draft dREL grammar at the COMCIFS/drel repository assumes that
newline is whitespace.  The example parser based on this grammar does
not identify any problems with the grammar.  Nick Spadaccini
has advised me that newline was not meant to be significant in the
dREL grammar.

[1] Spadaccini et. al,
(2012) *J. Chem. Inf. Model.* **52**(8) pp 1917-1925
