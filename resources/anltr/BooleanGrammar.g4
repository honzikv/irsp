grammar BooleanGrammar;


// Data types
AND: 'AND';
OR: 'OR';
NOT: 'NOT';
LPAR: '(';
RPAR: ')';
WHITESPACE: [\r\t ]+;

QUERY_TERM: [A-Za-z0-9\u0080-\uFFFF]+;

start: expression;

termChain: QUERY_TERM | QUERY_TERM WHITESPACE termChain;

expression:
    LPAR expression RPAR #parenthesis
    | expression WHITESPACE AND WHITESPACE expression #and
    | expression WHITESPACE OR WHITESPACE expression #or
    | NOT WHITESPACE expression #not
    | termChain #queryTerm
    ;

