A DRAFT annotated grammar for dREL
====================================

The following grammar is based on the dREL publication combined with
the dREL examples found in the core CIF dictionary.  A few changes
have been included that require approval from COMCIFS.  In particular:

1. Leading underscores in front of identifiers are no longer significant. This
   is justified on the grounds that there is no useful semantic difference between
   ``_category.object`` and ``category.object``

2. Subscriptions can now include lists of embedded assignments of the form ``.id = <value>``. This
   is part of an update to allow multi-key categories.


Note that this file is laid out to allow automatic production of the Lark parser. The
EBNF used here differs from the ISO standard as follows:

1. Sequences of characters may be denoted by strings
2. The expression separator is a space, not a comma
3. Character ranges may be included in tokens to save space
4. Regular expressions are used to create tokens.

Postprocessing of this file changes '=' to ':' in productions and removes trailing
semicolons.

TODO: include whitespace.  Whitespace in only significant where it is necessary
to disambiguate productions.
    
Tokens
------

These are the productions for all capitalised items above. Note that keywords are
case-insensitive, but this has been left out of the productions below for brevity.
As this list is intended to be input into a system, the most specific values must
come first. ::

    NEWLINE = /[\r\n]+/
    ISEQUAL = "=="
    PWR = "**"
    NEQ = "!="
    GTE = ">=" 
    LTE = "<="
    GT = ">"
    LT = "<"
    APPEND = "++="
    AUGADD = "+="
    AUGMIN = "-="
    AUGMUL = "*="
    AUGDROP = "--="
    ELLIPSIS = "..." 
    BADOR = "|"
    BADAND = "&&"
    LEFTPAREN = "("
    RIGHTPAREN = ")"
    LEFTBRACE = "{"
    RIGHTBRACE = "}"
    PLUS = "+"
    MINUS = "-"
    MULT = "*"
    DIV = "/"
    PERIOD = "."
    CROSS = "^"
    EQUALS = "="
    COMMA = ","
    LSQUAREB = "["
    RSQUAREB = "]"
    COLON = ":"
    SEMI = ";"
    INTEGER = /[0-9]+/
    OCTINT = /0o[0-7]+/
    HEXINT = /0x[0-9A-Fa-f]+/
    BININT = /0b[0-1]+/

A real number must contain a decimal point, and may be
optionally followed by an exponent after the letter "E". A digit before the
decimal point is not required. ::
    
    REAL = /(([0-9]+\.[0-9]*)|(\.[0-9]+))[Ee][+-]?[0-9]+/

An imaginary number is a real or integer followed by the letter "j". ::
    
    IMAGINARY = /((([0-9]+\.[0-9]*)|(\.[0-9]+))[Ee][+-]?[0-9]+)|([0-9]+)[jJ]/

A longstring is enclosed in triple quotes or triple double quotes, and
may contain NEWLINE. TODO: check that backslashes work properly.::

    LONGSTRING = /'''[^\\][.\n]*'''|"""[^\\][.\n]*"""/
    SHORTSTRING = /'[^']*'|"[^"]"/

Keywords. These are case insensitive, but this is ignored below.::

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

Whitespace is not often significant. ::

    WHITESPACE = /[ \t]+/
    %ignore WHITESPACE

    
Literals
--------
Literals are either identifiers, string literals or numbers ::

    literal = SHORTSTRING | LONGSTRING | INTEGER | HEXINT | OCTINT | BININT | REAL | IMAGINARY ;
    
Atoms
-----

An atom is either a literal, an identifier, or an enclosure ::

    atom = ID | literal | enclosure ;

An enclosure is either a list, a table or a list of expressions enclosed in round brackets. ::

    enclosure = parenth_form | list_display | table_display ;
    parenth_form = "("  expression_list  ")" ;

A list is formed by comma-delimited expressions inside square brackets, with
optional NEWLINEs anywhere inside the brackets. Trailing commas are not allowed. ::
    
    list_display = "["  { NEWLINE }   expression_list  { NEWLINE }  "]" ;
    expression_list = expression | ( expression_list  ","  { NEWLINE }  expression ) ;

A table is formed from a comma-delimited list of key:value pairs enclosed in braces. A
trailing comma is not allowed. NEWLINEs are allowed outside the key:value pairs. ::
    
    table_display = "{"  {NEWLINE}  table_contents  {NEWLINE}  "}" ;
    table_contents = table_entry | (table_contents "," {NEWLINE}  table_entry ) ;
    table_entry = SHORTSTRING  ":"  expression ;

Primaries
---------

A primary is the most tightly bound expression: either an atom by itself, an
attribute reference, a subscription, a slicing, or a function call. ::

    primary = atom | attributeref | subscription | slicing | call ;

An attribute reference is created from a primary followed by a period and an
identifier. In this case the identifier may include digits. ::

    attributeref = primary  "."  ( ID | INTEGER ) ;

A subscription is formed from a primary followed by an expression or
a series of dotted assignments in square brackets. ::

    subscription = primary  "["  (dotlist | expression)  "]" ;
    dotlist = ("."  ID  "="  expression) | (dotlist  ","  "."  ID  "="  expression);
    
A slice is primary followed by a series of up to three expressions separated by colons
and/or commas inside square brackets.  The expressions should evaluate to integers. When one
colon appears inside the square brackets, it delimits the start and end coordinates of the
sliced object. When two colons appear (a `long_slice`) the final expression refers to
the slice step. ::

    slicing = primary  "["  (proper_slice | slice_list )  "]" ;
    proper_slice = short_slice | long_slice ;
    short_slice = ":" | (expression  ":"  expression) | (":"  expression) | (expression  ":") ;
    long_slice = short_slice  ":"  expression ;

`slice_lists` are composed of expressions and slices, where each entry
in the list refers to a separate dimension of the sliced object.::

    slice_list = slice_item | (slice_list  ","  slice_item) ;
    slice_item = expression | proper_slice ;
    
A function call is an identifier followed by round brackets enclosing a list of arguments
to the function. ::

    call = ID  "("  [expression_list]  ")" ;

Operators
---------

Operators act on primaries.
The power operator raises the primary to the power of the second expression,
which is essentially a signed power expression. ::

    power = primary  [ "**"  factor ] ;
    
A sign may optionally prefix a primary. ::

    factor = power |  ("-"| "+")  factor  ;

Multiplication, division and cross product operations. ::

    term = factor {  ("*"|"/"|"^")  factor } ;

Addition and subtraction. ::

    arith = term  {("+"|"-")  term } ;

We split the definition of comparison operators into two sets here so that
we can use a subset of comparison operations in compound statements
to test loops. ::

    restricted_comp_operator = "<" | ">" | GTE | LTE | NEQ | ISEQUAL ;

The full set of comparison operators. ::

    comp_operator = restricted_comp_operator | IN | (NOT IN) ;

A comparison is performed between two mathematical expressions. ::

    comparison = arith  { comp_operator  arith } ;

The resulting logical value can be tested using logical operations. Logical
negation using "NOT" can be repeated arbitrarily many times. ::

    not_test = comparison | (NOT  not_test) ;

Logical AND has lower precedence than NOT, followed by logical OR. TODO: can
we construct an expression that has an or_test in second position?::

    and_test = not_test  {  (AND | BADAND )  not_test } ;
    or_test  = and_test  { (OR | BADOR )  and_test } ;

The OR test is the least-tightly bound operation on primaries, so becomes the same
production as that for an expression. ::

    expression = or_test ;

Statements
-----------------

Expressions by themselves yield values. In order to act on these values, statements
are constructed from expressions and keywords.  Statements may be either simple,
or compound. Simple statements do not contain
other statements. A series of simple statements may be separated by NEWLINEs, and
may also be separated by semicolons, but compound statements require no such
separators. TODO - surely this can be cleaned up?::

    statements = statement | (statements statement) ;
    statement = (simple_statement  [";"]  NEWLINE  { NEWLINE }) | compound_statement ;
    simple_statement = small_statement | (simple_statement  ";"  small_statement) ;

Simple statements include one-word statements as well as expression lists, and
augmented assignment statements. TODO: shouldn"t we include assignments separately?::

    small_statement = expr_stmt | BREAK | NEXT ;
    expr_stmt = (expression_list  [ (augop | "=")  expression_list ] ) | dotlist_assign ;

Dotted assignments are list of assignments to dotted identifiers, used for assigning to
multiple columns of a category object at the same time, that is, using the same row. The
production for `dotlist` is presented above in the Primaries section.::

    dotlist_assign = ID "("  dotlist  ")" ;

Compound statements contain other statements. dREL defines if, for, do, loop, with, repeat
and function definition compound statements. ::

    compound_statement = if_stmt | if_else_stmt | for_stmt | do_stmt | loop_stmt
                         | with_stmt | repeat_stmt | funcdef ;

Compound statements contain "suites" of statements. Where more than one statement
is included in a block, the statements must be enclosed in braces. ::

    suite = statement | "{"  {NEWLINE}  statements  "}"  {NEWLINE} ;
    
IF statements may contain multiple conditions separated by ELSEIF keywords, or a
single alternative action using the ELSE keyword. ::

    if_else_stmt = if_stmt  ELSE  suite ;
    if_stmt = ([if_stmt  ELSEIF] | IF)  "("  expression  ")"  {NEWLINE} suite ;

For statements perform simple loops over the items in `expression_list`, assigning
them in turn to the items in `id_list`. `id_list` can be optionally enclosed in
square brackets. ::

    for_stmt = FOR  (id_list | "[" id_list "]")  IN  expression_list  suite ;
    id_list = [id_list  ","]  ID ;
    
Loop statements loop over categories row by row, assigning each new row to the
identifier provided .::

    loop_stmt =  LOOP ID AS ID [":"  ID  [restricted_comp_operator  ID]] suite ;

Do statements perform simple loops in the same way as FOR statements. ::

    do_stmt = DO ID  "=" expression  ","  expression  [","  expression] suite ;

Repeat statements repeat the contents of `suite` until a `BREAK` statement is called. ::

    repeat_stmt = REPEAT suite ;

With statements bind a local variable to a category variable (aliasing). This is
required if a category name would be identical to a keyword. ::

    with_stmt = WITH  ID  AS  ID  {NEWLINE}  suite ;

Each argument in a function definition argument list is followed by a list with two
elements: the container type, and the type of the object in the container. ::

    funcdef = FUNCTION  ID  "("  arglist  ")"  suite ;
    arglist = ID  ":"  "["  expression  ","  expression  "]" ;

Complete dREL code
------------------

A complete dREL method is composed of a sequence of statements. ::

    input = [input | {NEWLINE}] statement ;

Literal productions
-------------------
Some more complex literal productions not included in tokens. ::
    
    augop = "++=" | "+=" | "-=" | "--=" | "*=" | "="; 
    
    ELSEIF = ELSE IF ;
