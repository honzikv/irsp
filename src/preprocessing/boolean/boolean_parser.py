from enum import Enum

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

from src.preprocessing.boolean.parser.BooleanGrammarLexer import BooleanGrammarLexer
from src.preprocessing.boolean.parser.BooleanGrammarParser import BooleanGrammarParser
from src.preprocessing.boolean.parser.BooleanGrammarVisitor import BooleanGrammarVisitor


class BooleanOperator(Enum):
    """
    Enum for boolean operators
    """
    AND = 0,
    OR = 1,
    NOT = 2,


class QueryItem:
    """
    Tree-like structure which holds operator and items its being applied to.
    Items can either be strings or other QueryItems.
    """

    def __init__(self, items, operator: BooleanOperator):
        self.items = items
        self.operator = operator

    def __str__(self):
        if isinstance(self.items, str):
            return '{ item: ' + f'{self.items} {self.operator.name}' + '}'

        items = '{ items: [\n'
        for idx, item in enumerate(self.items):
            if idx == len(self.items) - 1:
                items += f'{item}\n],\n operator: {self.operator.name}'
            else:
                items += f'{item}, '
        return items + ' }'

    def is_empty(self):
        if isinstance(self.items, str) and self.items == '':
            return True
        if isinstance(self.items, list) and len(self.items) == 0:
            return True
        for item in self.items:
            if isinstance(item, str) and item == '' or isinstance(item, QueryItem) and item.is_empty():
                continue
            return False

        return True


class BooleanErrorListener(ErrorListener):

    def __init__(self):
        super(BooleanErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise ValueError()

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        raise ValueError()

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        raise ValueError()

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        raise ValueError()


class BooleanQueryVisitor(BooleanGrammarVisitor):
    """
    ANTLR4 visitor implementation
    """

    def __init__(self):
        self.query = []

    def clear(self):
        self.query = []

    def visitStart(self, ctx: BooleanGrammarParser.StartContext):
        return self.visit(ctx.expression())

    def visitQueryTerm(self, ctx: BooleanGrammarParser.QueryTermContext):
        return self.visit(ctx.termChain())

    def visitAnd(self, ctx: BooleanGrammarParser.AndContext):
        return QueryItem([self.visit(ctx.expression(0)), self.visit(ctx.expression(1))], BooleanOperator.AND)

    def visitOr(self, ctx: BooleanGrammarParser.OrContext):
        return QueryItem([self.visit(ctx.expression(0)), self.visit(ctx.expression(1))], BooleanOperator.OR)

    def visitNot(self, ctx: BooleanGrammarParser.NotContext):
        return QueryItem([self.visit(ctx.expression())], BooleanOperator.NOT)

    def visitTermChain(self, ctx: BooleanGrammarParser.TermChainContext):
        term = str(ctx.QUERY_TERM())  # get the first token - a string
        # If there is no term chain present return the term itself
        if not ctx.termChain():
            return term

        # Get value of the rest - this will either be a QueryItem or a string
        chained_terms = self.visitTermChain(ctx.termChain())

        if isinstance(chained_terms, str):
            # If its string build a new QueryItem and return it
            return QueryItem([term, chained_terms], BooleanOperator.AND)

        # Otherwise, it's a QueryItem, so we can just append our term to it
        chained_terms.items.append(term)
        return chained_terms

    def visitParenthesis(self, ctx: BooleanGrammarParser.ParenthesisContext):
        return self.visit(ctx.expression())


def parse_boolean_query(query: str):
    """
    Parse a boolean query and return a QueryItem object
    :param query: a boolean query - string
    :return: a QueryItem object
    """
    lexer = BooleanGrammarLexer(InputStream(query))
    lexer.removeErrorListeners()
    lexer.addErrorListener(BooleanErrorListener())
    stream = CommonTokenStream(lexer)
    parser = BooleanGrammarParser(stream)
    parser.addErrorListener(BooleanErrorListener())
    tree = parser.start()
    return BooleanQueryVisitor().visit(tree)
