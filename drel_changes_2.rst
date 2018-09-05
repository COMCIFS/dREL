Proposed changes to dREL, part II
=================================

Introduction
------------

dREL is a machine-actionable language describing data relationships
and designed to be embedded in DDLm dictionaries. The language is
defined both explicitly in the dREL publication [1] and implicitly by
the dREL code appearing in the DDLm core CIF dictionary. Note that
the code in the core CIF dictionary significantly expands the language
presented in the paper, for example, by adding category methods.

The present changes were foreshadowed in the discussion about allowing
set methods to become looped [2].  They are aimed at removing the
current dREL-imposed requirement that all categories must have a
single data name that acts as a key.

Proposal 3: compound key specification
--------------------------------------

dREL as published permits a particular row in a loop to be specified
by providing the value of the key for that loop using the syntax
`<category>[keyvalue]`, so for example, `atom_site['O1']` would be the
row in the atom_site loop for which `_atom_site.label` (the key data
name for category `atom_site`) is 'O1'.  We propose expanding
this syntax to allow multiple key values to be specified:
`<category>[name1=value1,name2=value2]` would specify the row of
`<category>` for which category objects `name1` and `name2` take
values of `value1` and `value2` respectively.

Explanation
~~~~~~~~~~~

The current core CIF dictionary treats multi-key categories by
defining a synthetic data name for each such category. These synthetic
data names are currently just a list of the values of the multiple
keys. Having such single-dataname keys allows the dREL syntax to
be unambiguous for all Loop categories.

This approach is suboptimal because:
(1) The synthetic data names have no scientific relevance
(2) A considerable amount of DDLm machinery has been developed simply
    because of the resulting inhomogeneous lists. Without
    these synthetic data names, there would be *no* need in the current
    core dictionary for ragged and nested dimensions and multiple
    data types within a single list, and therefore no requirement
    for DDLm and dREL implementors to cope with such structures.
(3) dREL methods wishing to index into a multi-key category have to
    construct the synthetic keys from the individual values; the new
    syntax would save that line of boilerplate
(4) If a set category becomes looped, a number of looped categories
    will acquire a new key data name. If single-key loops remain a
    dREL requirement, previously single-key loops will require a new,
    synthetic data name to be created. Note that it could be argued
    that this is the way the system was designed to work.

The previous syntax will still be acceptable in those situations where
there is a single key, or where the values of the remaining keys are
unambiguous in context (see next proposal).

This proposed syntax has been included in the example EBNF for dREL
and the transformation to Python code implements the proposed semantics.

Proposal 4: elide keys where they are clear from context
--------------------------------------------------------

If category A contains data names which are parents or children of key
data names in category B, dREL methods in category A do not need to
explicitly specify the key values of category B when accessing rows of
category B.

Explanation
~~~~~~~~~~~

If b.k1 and b.k2 are the keys of category B, and data names A.a1 and
A.a2 are linked through `_name.linked_item_id` DDLm declarations to
those keys, then any dREL method in category A can simply write `b.d3`
to access a specific value of dataname d3 in category b.  This is
equivalent to writing `b[k1=a.a1,k2=a.a2].d3` under proposal 3.

Note that this short cut is not possible where more than one data name
is linked to the same category key, for example, in `geom_bond`
two data names are linked to `atom_site.label`.

Note that partial resolution of data names is also possible, so that
key references that are missing from the original form may be resolved
using linked data names.

Discussion
----------

The net result of the above two proposals is to make looping Set
categories relatively painless. A dREL reference like `cell.vector_a`
may remain untouched when multiple cells are present, as long as the
category within which the dREL method appears has only a single
data name that is a child of the single key data name of `cell`.

However, in situations where the `<category>[value]` syntax has
been used and `<category>` acquires a new key data name because
some other category has become looped, dREL methods will need
to be rewritten to explicitly specify the key data name that
`value` corresponds to.  Going forward, the `[key=value]`
syntax should be preferred to minimise the need to rewrite
methods in advanced looping applications.

We should also be aware the dREL methods in our dictionaries are
curated, and therefore we can apply style guidelines to prefer the
explicit notation of proposal 3 as we see fit.

[1] Spadaccini et. al,
(2012) *J. Chem. Inf. Model.* **52**(8) pp 1917-1925

[2] https://github.com/COMCIFS/comcifs.github.io/blob/master/looping_proposal.md
