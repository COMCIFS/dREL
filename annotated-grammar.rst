An DRAFT annotated grammar for dREL
====================================

The following grammar is based on the dREL publication combined with
the dREL examples found in the core CIF dictionary.  A few changes
have been included that require approval from COMCIFS.  In particular:

1. Leading underscores in front of identifiers are no longer significant. This
   is justified on the grounds that there is no useful semantic difference between
   `_category.object` and `category.object`

2. Subscriptions can now include lists of embedded assignments of the form `.id = <value>`. This
   is part of an update to allow multi-key categories.


Note that the productions for the tokens (written in capitals) are given at the end.
TODO: include whitespace.  Whitespace in only significant where it is necessary
to disambiguate productions.

Literals
--------
Literals are either identifiers, string literals or numbers ::

    literal = string_literal | INTEGER | HEXINT | OCTINT | BININT | REAL | IMAGINARY ;
    
A string literal is a string delimited by single quotes or double quotes,
and not spanning a line, or a string delimited by triple quotes or
double quotes, and allowed to span more than one line. ::

    string_literal = SHORTSTRING | LONGSTRING ;

Atoms
-----

An atom is either a literal, an identifier, or an enclosure ::

    atom = ID | literal | enclosure ;

An enclosure is either a list, a table or a list of expressions enclosed in round brackets. ::

    enclosure = parenth_form | list_display | table_display ;
    parenth_form = '(' , expression_list , ')' ;

A list is formed by comma-delimited expressions inside square brackets, with
optional newlines anywhere inside the brackets. Trailing commas are not allowed. ::
    
    list_display = '[' , { newline }  , expression_list , { newline } , ']' ;
    expression_list = expression | ( expression_list , ',' , { newline } , expression ) ;

A table is formed from a comma-delimited list of key:value pairs enclosed in braces. A
trailing comma is not allowed. Newlines are allowed outside the key:value pairs. ::
    
    table_display = '{' , {newline} , table_contents , {newline} , '}' ;
    table_contents = table_entry | (table_contents ',' {newline} , table_entry ) ;
    table_entry = string_literal , ':' , expression ;

Primaries
---------

A primary is the most tightly bound expression: either an atom by itself, an
attribute reference, a subscription, a slicing, or a function call. ::

    primary = atom | attributeref | subscription | slicing | call ;

An attribute reference is created from a primary followed by a period and an
identifier. In this case the identifier may include digits. ::

    attributeref = primary , "." , ( ID | DIGITS ) ;

A subscription is formed from a primary followed by an expression or
a series of dotted assignments in square brackets. ::

    subscription = primary , "[" , (dotlist | expression) , "]" ;
    dotlist = ('.' , ID , '=' , expression) | (dotlist , "," , "." , ID , "=" , expression);
    
A slice is primary followed by a series of up to three expressions separated by colons
and/or commas inside square brackets.  The expressions should evaluate to integers. When one
colon appears inside the square brackets, it delimits the start and end coordinates of the
sliced object. When two colons appear (a `long_slice`) the final expression refers to
the slice step. ::

    slicing = primary , "[" , (proper_slice | slice_list ) , "]" ;
    proper_slice = short_slice | long_slice
    short_slice = ":" | (expression , ":" , expression) | (":" , expression) | (expression , ":")
    long_slice = short_slice , ":" , expression

`slice_lists` are composed of expressions and slices, where each entry
in the list refers to a separate dimension of the sliced object.::

    slice_list = slice_item | (slice_list , "," , slice_item)
    slice_item = expression | proper_slice
    
A function call is an identifier followed by round brackets enclosing a list of arguments
to the function. ::

    call = ID , "(" , [expression_list] , ")"

Operators
---------

Operators act on primaries. They are listed below in order of precedence.

The power operator raises the primary to the power of the second expression,
which is essentially a signed power expression. ::

    power = primary , [ POWER , u_expr ] ;

A sign may optionally prefix a primary ::

    u_expr = power | [("-"| "+") , power ] ;

Multiplication, division and cross product operations. ::

    m_expr = u_expr | [ m_expr , ('*'|'/'|'^') , u_expr];

Addition and subtraction. ::

    a_expr = m_expr | [ a_expr , ('+'|'-') , m_expr ];

We split the definition of comparison operators into two sets here so that
we can use a subset of comparison operations in compound statements
to test loops. ::

    restricted_comp_operator = "<" | ">" | GTE | LTE | NEQ | ISEQUAL ;

The full set of comparison operators. ::

    comp_operator = restricted_comp_operator | IN | (NOT , IN) ;

A comparison is performed between two mathematical expressions. ::

    comparison = a_expr , [ comp_operator , a_expr ] ;

The resulting logical value can be tested using logical operations. Logical
negation using 'NOT' can be repeated arbitrarily many times. ::

    not_test = comparison | (NOT , not_test) ;

Logical AND has lower precedence than NOT, followed by logical OR. TODO: can
we construct an expression that has an or_test in second position?::

    and_test = not_test | (and_test , (AND | BADAND ) , not_test ) ;
    or_test  = and_test | (or_test , (OR | BADOR ) , and_test );

The OR test is the least-tightly bound operation on primaries, so becomes the same
production as that for an expression. ::

    expression = or_test ;

Statements
-----------------

Expressions by themselves yield values. In order to act on these values, statements
are constructed from expressions and keywords.  Statements may be either simple,
or compound. Simple statements do not contain
other statements. A series of simple statements may be separated by newlines, and
may also be separated by semicolons, but compound statements require no such
separators. TODO - surely this can be cleaned up?::

    statements = statement | (statements statement)
    statement = (simple_statement , [";"] , newline , { newline }) | compound_statement ;
    simple_statement = small_statement | (simple_statement , ";" , small_statement) ;

Simple statements include one-word statements as well as expression lists, and
augmented assignment statements. TODO: shouldn't we include assignments separately?::

    small_statement = expr_stmt | BREAK | NEXT ;
    expr_stmt = (expression_list , [ (AUGOP | "=") , expression_list ] ) | dotlist_assign ;

Dotted assignments are list of assignments to dotted identifiers, used for assigning to
multiple columns of a category object at the same time, that is, using the same row. The
production for `dotlist` is presented above in the Primaries section.::

    dotlist_assign = ID, "(" , dotlist , ")"

Compound statements contain other statements. dREL defines if, for, do, loop, with, repeat
and function definition compound statements. ::

    compound_statement = if_stmt | if_else_stmt | for_stmt | do_stmt | loop_stmt
                         | with_stmt | repeat_stmt | funcdef ;

Compound statements contain 'suites' of statements. Where more than one statement
is included in a block, the statements must be enclosed in braces. ::

    suite = statement | "{" , {newline} , statements , "}" , {newline} ;
    
IF statements may contain multiple conditions separated by ELSEIF keywords, or a
single alternative action using the ELSE keyword. ::

    if_else_stmt = if_stmt , ELSE , suite ;
    if_stmt = ([if_stmt , ELSEIF] | IF) , "(" , expression , ")" , {newline} , suite ;

For statements perform simple loops over the items in `expression_list`, assigning
them in turn to the items in `id_list`. `id_list` can be optionally enclosed in
square brackets. ::

    for_stmt = FOR , (id_list | "[" id_list "]") , IN , expression_list , suite
    id_list = [id_list , ","] , ID ;
    
Loop statements loop over categories row by row, assigning each new row to the
identifier provided .::

    loop_stmt =  LOOP , ID, AS, ID , [":" , ID , [restricted_comp_operator , ID]] , suite ;

Do statements perform simple loops in the same way as FOR statements. ::

    do_stmt = DO, ID , "=", expression , "," , expression , ["," , expression] suite ;

Repeat statements repeat the contents of `suite` until a `BREAK` statement is called. ::

    repeat_stmt = REPEAT , suite ;

With statements bind a local variable to a category variable (aliasing). ::

    with_stmt = WITH , ID , AS , ID , {newline} , suite ;

Each argument in a function definition argument list is followed by a list with two
elements: the container type, and the type of the object in the container. ::

    funcdef = FUNCTION , ID , "(" , arglist , ")" , suite ;
    arglist = ID , ":" , "[" , expression , "," , expression , "]" ;

Complete dREL code
------------------

A complete dREL method is composed of a sequence of statements. ::

    input = [input | {newline}] statement ;

Literal productions
-------------------

These are the productions for all capitalised items above. Note that keywords are
case-insensitive, but this has been left out of the productions below for brevity. ::

    ALL = (* All characters. Not expanded here *)
    NEWLINE = ? Any end of line character ?
    ALLNOB = ALL - '\\' ; (* All characters, no backslash *)
    ALLNOQUOTENONL = ALL - "'" - NEWLINE ;
    ALLNODBLQNONL  = ALL - '"' - NEWLINE ;
    ALPHA = (* All ASCII alphabetic characters. Not expanded here *)
    POWER = 2 * '*';
    ISEQUAL = 2 * '=' ;
    NEQ = '!' , '=' ;
    GTE = '>' , '=' ;
    LTE = '<' , '=' ;
    ELLIPSIS = 3 * '.' ;
    BADOR = 2 * '|' ;
    BADAND = 2 * '&' ;
    AUGOP = (2 * '+' | '+' | '-' | 2 * '-' | '*' ) , '=' ;
    DIGIT = '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' ;
    OCTDIG = '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' ;
    HEXDIG = '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | 'A'
             'B' | 'C' | 'D' | 'E' | 'F' ;

An integer is a sequence of digits. ::
    
    INTEGER = DIGIT , {DIGIT} ;
    
A real number must contain a decimal point, and may be
optionally followed by an exponent after the letter 'E'. A digit before the
decimal point is not required. ::
    
    REAL = ((INTEGER, '.' , {DIGIT}) | ('.' , INTEGER))[('E'|'e') ,
           {'+'|'-'}, INTEGER] ;

An imaginary number is a real or integer followed by the letter 'j'. ::
    
    IMAGINARY = (REAL | INTEGER) , ('j' | 'J');

Binary, octal and hexadecimal integers are also allowed. Binary integers
are prefixed by '0b'.::

    BININT = '0' , ('b'|'B') , ('0'|'1') , {'0'|'1'} ;
    OCTINT = '0' , ('o'|'O') , OCTDIG , {OCTDIG} ;
    HEXINT = '0' , ('x'|'X') , HEXDIG , {HEXDIG} ;

A longstring is enclosed in triple quotes or triple double quotes, and
may contain newline. TODO: check that backslashes work properly.::
    
    LONGSTRING = (3 * "'" , {ALLNOB | ALL} , 3 * "'") |
                 (3 * '"', {ALLNOB | ALL} , 3 * '"') ;

    SHORTSTRING = ('"' , {ALLNODBLQNONL} , '"') | ("'", {ALLNOQUOTENONL} , "'") ;

Keywords. These are case insensitive, but this is ignored below.::

    ELSEIF = 'E','L','S','E', wspace , {wspace}, 'I','F' ;
    AND = 'A','N','D';
    OR = 'O','R';
    IN = 'I','N';
    NOT = 'N','O','T' ;
    DO = 'D','O';
    FOR = 'F','O','R',
    LOOP = 'L','O','O','P';
    AS = 'A','S';
    WITH = 'W','I','T','H';
    WHERE = 'W','H','E','R','E';
    ELSE = 'E','L','S','E';
    NEXT = 'N','E','X','T';
    BREAK = 'B','R','E','A','K';
    IF = 'I','F';
    FUNCTION = 'F','U','N','C','T','I','O','N';
    REPEAT = 'R','E','P','E','A','T';

Identifiers must begin with a letter and may contain alphanumerics, underscore and
the dollar sign. ::

    ID = ALPHA , {(ALPHA | DIGIT | '_' | '$' )}

Comments begin with a hash and continue to the end of the line. ::

    COMMENT = "#" , (ALL - NEWLINE)

Whitespace is not often significant. ::

    wspace = NEWLINE | ? ASCII TAB ? | ' ' ;
