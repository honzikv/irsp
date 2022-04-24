import pyparsing as pp

term = pp.Regex(r'\b(?![and|AND|or|OR|\(\)]\b)\w+')

bool_expr = pp.infixNotation(
    term, []
)

