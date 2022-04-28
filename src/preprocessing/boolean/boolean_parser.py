from enum import Enum
from io import StringIO

from antlr4 import CommonTokenStream, InputStream

from src.preprocessing.boolean.parser.BooleanGrammarLexer import BooleanGrammarLexer
from src.preprocessing.boolean.parser.BooleanGrammarParser import BooleanGrammarParser
from src.preprocessing.boolean.parser.BooleanGrammarVisitor import BooleanGrammarVisitor


class BooleanOperator(Enum):
    AND = 0
    OR = 1
    NOT = 2


class QueryItem:

    def __init__(self, items, operator: BooleanOperator):
        self.items = items
        self.operator = operator


class BooleanQueryVisitor(BooleanGrammarVisitor):

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


lexer = BooleanGrammarLexer(InputStream("I am                 really smurfing OR not"))
stream = CommonTokenStream(lexer)
parser = BooleanGrammarParser(stream)
tree = parser.start()
ans = BooleanQueryVisitor().visit(tree)
