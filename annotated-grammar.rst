A DRAFT annotated grammar for dREL
====================================

The following grammar is based on the dREL publication (Spadaccini, N., Castleden,
I. R., du Boulay, D. and Hall, S. R.,"dREL: A relational expression language
for dictionary methods", *J. Chem. Inf. Model.* , 2012, **52** (8) pp 1917-1925.
https://dx.doi.org/10.1021/ci300076w ),  combined with
the dREL examples found in the core CIF dictionary.  A few changes
have been included that may require approval from COMCIFS.  In particular:

1. Leading underscores in front of identifiers are no longer significant. This
   is justified on the grounds that there is no useful semantic difference between
   ``_category.object`` and ``category.object``

2. Subscriptions can now include lists of embedded assignments of the form ``.id = <value>``. This
   allows rows in multi-key categories to be referenced.

3. Newlines are completely ignored. Certain readings of the original
   paper suggest that this was not the intention, but nevertheless the
   language presented in the paper does not need newlines in order to
   remove ambiguity.

4. Literal 'missing' ('?') and 'null' have been added to the language

The EBNF used here differs from the ISO standard as follows:

1. Sequences of characters may be presented as single strings
2. The expression separator is a space, not a comma
3. Character ranges may be included in tokens to save space
4. Regular expressions are used to create tokens.
5. Whitespace is handled outside the EBNF grammar. The appearance of whitespace terminates
a token unless whitespace is expected as part of the token.
    
Tokens
------

In the token descriptions below, expressions appearing between forward
slashes are regular expressions. The assumption in the grammar is that
the longest matching token is the one selected.

Delimiters
~~~~~~~~~~

Delimiters are discussed in the context of their use, below.
::

    LEFTPAREN = "("
    RIGHTPAREN = ")"
    LEFTBRACE = "{"
    RIGHTBRACE = "}"
    LSQUAREB = "["
    RSQUAREB = "]"
    COMMA = ","
    COLON = ":"
    SEMI = ";"

Operators
~~~~~~~~~

Operators are listed below in order of precedence. Multiplication, division
and cross product have equal precedence. When plus and minus are used to
give the sign of a number, their precedence is higher than multiplication.
Period is used for attribute reference.

::

    PERIOD = "."
    PWR = "**"
    MULT = "*"
    DIV = "/"
    CROSS = "^"
    PLUS = "+"
    MINUS = "-"
 

Logical operations
~~~~~~~~~~~~~~~~~~
::

    ISEQUAL = "=="
    NEQ = "!="
    GTE = ">=" 
    LTE = "<="
    GT = ">"
    LT = "<"

The following two operations (bitwise or and and) were
not defined in the paper but appear in the core dictionary. ::

    BADOR = "||"
    BADAND = "&&"
    
Assignment
~~~~~~~~~~
See the discussion of assignments in the relevant section of the grammar.
::

    EQUALS = "="
    APPEND = "++="
    AUGADD = "+="
    AUGMIN = "-="
    AUGMUL = "*="
    AUGDROP = "--=" 

For convenience all assignment operations are grouped into a single production. ::
    
    augop = APPEND | AUGADD | AUGMIN | AUGDROP | AUGMUL | EQUALS ; 
    
Literals
~~~~~~~~
::

    INTEGER = /[0-9]+/
    OCTINT = /0o[0-7]+/
    HEXINT = /0x[0-9A-Fa-f]+/
    BININT = /0b[0-1]+/
    MISSING = "?"
    NULL = "NULL"

A real number must contain a decimal point, and may be
optionally followed by an exponent after the letter "E". A digit before the
decimal point is not required. However, this means that the category-object
construction "t.12" could be tokenised as "ID REAL" instead of the
manageable "ID PERIOD INTEGER", so we write out the real and imaginary
productions using the INTEGER token to force the latter token sequence. ::
    
    real = ((INTEGER "." {INTEGER})|("." INTEGER))[("E"|"e") ["+"|"-"] INTEGER ]

An imaginary number is a real or integer followed by the letter "j". ::
    
    imaginary = (real | INTEGER) ("j"|"J")

A longstring is enclosed in triple quotes or triple double quotes, and
may contain newline characters. TODO: check that backslashes work properly. ::

    LONGSTRING = /'''[^\\][.\n]*'''|"""[^\\][.\n]*"""/
    SHORTSTRING = /'[^']*'|"[^"]*"/

Keywords. 
~~~~~~~~~

These are case insensitive, but for brevity this has not been
made explicit. ::

    AND = "and"
    OR = "or"
    IN = "in"
    NOT = "not"
    DO = "do"
    FOR = "for"
    LOOP = "loop"
    AS = "as"
    WITH = "with"
    WHERE = "where"
    ELSE = "else"
    ELSEIF = /"else if"|"elseif"/
    NEXT = "next"
    BREAK = "break"
    IF = "if"
    FUNCTION = "function"
    REPEAT = "repeat"

Identifiers must begin with a letter or underscore and may contain alphanumerics, underscore and
the dollar sign. ::

    ID = /[A-Za-z_][A-Za-z0-9_$]*/

Comments begin with a hash and continue to the end of the line. ::

    COMMENT = /#.*/
    %ignore COMMENT

Whitespace is not significant. ::

    WHITESPACE = /[ \t\r\n]+/
    %ignore WHITESPACE

The following grammar productions are roughly organised from most granular to the
top level. A complete dREL fragment is built from atoms, which become primaries that
appear in expressions which are structured into statements.
    
Literals
--------
Literals are either string literals, numbers, missing or null. ::

    literal = SHORTSTRING | LONGSTRING | INTEGER | HEXINT | OCTINT | BININT | NULL | MISSING | real | imaginary ;
    
Atoms
-----

We include a production for an identifier to allow generated parsers an entry point
to manipulate the representation of the identifier. ::

    ident = ID ;
    
The fundamental building blocks of expressions are identifiers, literals and
enclosures.  An enclosure is either a list, a table or a list of
expressions enclosed in round brackets. ::

    enclosure = parenth_form | list_display | table_display ;
    parenth_form = LEFTPAREN expression_list RIGHTPAREN ;

A list is formed by comma-delimited expressions inside square brackets. ::
    
    list_display = LSQUAREB  [ expression_list ] RSQUAREB ;
    expression_list = expression { COMMA expression } ;

A table is formed from a comma-delimited list of key:value pairs enclosed in braces.
The key of a table may not span a line. ::
    
    table_display = LEFTBRACE  table_contents RIGHTBRACE ;
    table_contents = table_entry { COMMA table_entry } ;
    table_entry = SHORTSTRING  COLON  expression ;

Primaries
---------

A primary is the most tightly bound expression: a literal, an
enclosure, an attribute reference, a subscription, or a function
call. In order to avoid ambiguities introduced by having real numbers
also containing a period, which is also used for attribute references,
we define a restricted subset of primaries for use with attribute
references. ::

    att_primary = ident | attributeref | subscription | call ;
    primary = att_primary | literal | enclosure ;

An attribute reference of form `<cat>.<object>` is created from a
primary followed by a period and string that identifies the object
name in the category.  As such object names can be composed of digits
(for example, matrix elements), we make sure to include both
identifiers and tokenised integers as candidates for `<object>`. An
attribute reference returns the value of the data name defined by
`<cat>.<object>` in the current row. It is an error to perform
attribute access on a non-category type. It is also an error to perform
attribute access when a specific row is not identifiable.  We use ``ID``
in the grammar rule to indicate that that this item is not something
that can be bound by the environment. ::

    attributeref = att_primary "."  ( ID | INTEGER )  ;

Square brackets are used to create a reference to an element in a list or
category. If `primary` is a category object and the explicit dotlist
notation is not used, the value in the square brackets must be a single-element
slice list (an expression) which is the value of the single key in this category.
A dotlist of the form `<category>[.id1 = x, .id2 = y, ...]` is used to
refer to the row of `<category>` for which `id1`, `id2`,... take the specified
values.

The result of applying a subscription to a category is an object which
has particular values for each column of the category. These values
are accessed using an attribute reference (see above). For
example, `atom_site['O1'].fract_x` gives the fractional x coordinate
for the row in in the `atom_site` loop for which the atom label is "O1".
This is equivalent to `atom_site[.label = 'O1'].fract_x`, but `.label`
may be omitted as it is the only key data name of category `atom_site`.

If the primary is a list or matrix, the item in the square brackets must be
a proper slice or slice list as for Python (see below). ::

    subscription = primary  "["  (proper_slice | slice_list | dotlist)  "]" ;
    dotlist =  dotlist_element {"," dotlist_element } ;
    dotlist_element = ("."  ident  "="  expression)
    
A slice is primary followed by a series of up to three expressions separated by colons
and/or commas inside square brackets.  The expressions should evaluate to integers. When one
colon appears inside the square brackets, it delimits the start and end coordinates of the
sliced object. When two colons appear (a `long_slice`) the final expression refers to
the slice step.

There is no ambiguity in the use of square brackets for slicing and
subscription, as category objects have no predefined ordering and therefore `<category>[0]`
must refer to the row of `<category>` for which the key data name is equal to 0,
rather than the "first" element of `<category`>. ::

    proper_slice = short_slice | long_slice ;
    short_slice = COLON | (expression  COLON  expression) | (COLON expression) | (expression  COLON) ;
    long_slice = short_slice  COLON  expression ;

`slice_lists` are composed of expressions and slices, where each entry
in the list refers to a separate dimension of the sliced object. ::

    slice_list = (expression | proper_slice) { COMMA (expression | proper_slice) } ;
    
A function call is an identifier followed by round brackets enclosing a list of arguments
to the function. ::

    call = ident  LEFTPAREN [expression_list] RIGHTPAREN ;

Operators
---------

Operators act on primaries.
The power operator raises the primary to the power of the second expression,
which is essentially a signed power expression.
TODO: check that precedence is actually correct. ::

    power = primary  [ PWR  factor ] ;
    
A sign may optionally prefix a primary. As this has lower precedence
than the power operation, `-1**2` equals -1. ::

    factor = power |  (PLUS|MINUS)  factor  ;

Multiplication, division and cross product operations. ::

    term = factor | (term (MULT|DIV|CROSS) factor ) ;

Addition and subtraction. ::

    arith = term | ( arith ( PLUS | MINUS ) term ) ;

We split the definition of comparison operators into two sets here so that
we can use a subset of comparison operations in compound statements that
allow only certain loop elements to be used. ::

    restricted_comp_operator = GT | LT | GTE | LTE | NEQ | ISEQUAL ;

The full set of comparison operators. ::

    comp_operator = restricted_comp_operator | IN | (NOT IN) ;

A comparison is performed between two mathematical expressions. ::

    comparison = arith | (comparison  comp_operator  arith ) ;

The resulting logical value can be tested using logical operations. Logical
negation using "NOT" can be repeated arbitrarily many times. ::

    not_test = comparison | (NOT  not_test) ;

Logical AND has lower precedence than NOT, followed by logical OR. TODO: can
we construct an expression that has an or_test in second position? ::

    and_test = not_test  {  (AND | BADAND )  not_test } ;
    or_test  = and_test  { (OR | BADOR )  and_test } ;

The OR test is the least-tightly bound operation on primaries, so becomes the same
production as that for an expression. ::

    expression = or_test ;

Statements
----------

Expressions by themselves yield values. In order to act on these
values, statements are constructed from expressions and keywords.
Statements may be either simple, or compound. Simple statements do not
contain other statements. A series of simple statements may be
separated by semicolons for readability. ::

    statements = statement | (statements statement) ;
    statement = simple_statement | compound_statement ;
    simple_statement = small_statement { ";"  small_statement } ;

Simple statements include one-word statements and assignments, where
assignment to multiple objects in a category using dotted lists is
included.

A `BREAK` statement exits from the nearest enclosing for, loop, repeat or do statement.
(see compound statements below). A `NEXT` statement jumps immediately to the
next iteration of the nearest enclosing for, loop, repeat or do statement. If the
current item is the final item, it exits the loop.

TODO: discuss assignments based on material in dREL paper.

Separate productions are provided for the left-hand and
right-hand side of the assignment so that parsers based on this
grammar can perform specialised operations depending on which side of
the assignment they are located.

An expression list is also allowed as
a statement on its own, mostly so that side-effect functions can be
called, although this is not recommended and may be deprecated. In the
current core CIF this is used only in a demonstration validation function
that calls an 'Alert' function.

(old) small_statement = expression_list | assignment | dotlist_assign | BREAK | NEXT ;

::

    small_statement = assignment | dotlist_assign | BREAK | NEXT ;
    assignment =  lhs augop rhs ;
    lhs = expression_list ;
    rhs = expression_list ;

Dotted assignments are list of assignments to dotted identifiers, used for assigning to
multiple columns of a category object at the same time in the same row. Such assignments
may only be performed in methods appearing in category definitions. The
production for `dotlist` is presented above in the Primaries section. ::

    dotlist_assign = ident "("  dotlist  ")" ;
    
Compound statements contain other statements. dREL defines if, for, do, loop, with, repeat
and function definition compound statements. ::

    compound_statement = if_stmt | for_stmt | do_stmt | loop_stmt
                         | with_stmt | repeat_stmt | funcdef ;

Compound statements contain "suites" of statements. Where more than one statement
is included in a suite, the statements must be enclosed in braces. ::

    suite = statement | "{" statements "}" ;
    
IF statements may contain multiple conditions separated by ELSEIF
keywords (which is like a switch statement), or a single alternative
action using the ELSE keyword. In practice `ELSE IF` is matched as
an if_stmt and only `ELSEIF` triggers the `else_if_stmt` production.
If `expression` evaluates to true, the following `suite` is executed,
otherwise the `suite` belonging to the `else_stmt` is executed, if
present.

::

    if_stmt = IF "(" expression ")" suite {else_if_stmt} [else_stmt];
    else_stmt = ELSE  suite ;
    else_if_stmt = ELSEIF  "("  expression  ")" suite ;

For statements perform simple loops over the items in `expression_list`, assigning
them in turn to the items in `id_list`. `id_list` can be optionally enclosed in
square brackets. ::

    for_stmt = FOR  (id_list | "[" id_list "]")  IN  expression_list  suite ;
    id_list = [id_list  ","]  ident ;
    
`Loop a as b` iterates over rows of category `b`, assigning them to
variable `a` and executing `suite`, which can then access the values
of particular data names within `a` using attribute access
(`a.c`). The form `Loop a as b : m` will additionally assign a
numerical row index to `m` within `suite`. The form `Loop a as b: m
cond n` will only perform the iteration for a particular row if the
condition `m cond n` is true. TODO: do we really need sequence
numbers in loops given that there is no canonical order?

The second ``ident`` cannot be replaced with a more liberal token (for example,
``primary`` or ``call``) as it introduces reduce conflicts in the syntax:
for example, is ``f(a,b)`` identifier ``f`` followed by enclosure (a,b), or
a function call?

::

    loop_stmt =  LOOP ident AS ident [":"  ident  [restricted_comp_operator  ident]] suite ;

Do statements perform simple loops in the same way as FOR statements. ::

    do_stmt = DO ident  "=" expression  ","  expression  [","  expression] suite ;

Repeat statements repeat the contents of `suite` until a `BREAK` statement is called. ::

    repeat_stmt = REPEAT suite ;

With statements bind a local variable to a category variable (aliasing). This is
required if a category name would be identical to a keyword. ::

    with_stmt = WITH  ident  AS  ident  suite ;

Each argument in a function definition argument list is followed by a list with two
elements: the container type, and the type of the object in the container. ::

    funcdef = FUNCTION  ident  "("  arglist  ")"  suite ;
    arglist = one_arg | (arglist COMMA one_arg) 
    one_arg = ident  ":"  "["  expression  ","  expression  "]" ;

Complete dREL code
------------------

A complete dREL method is composed of a sequence of statements. ::

    input = statements ;
