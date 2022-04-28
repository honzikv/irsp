# Generated from C:/dev/ir/irsp/resources/anltr\BooleanGrammar.g4 by ANTLR 4.10.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .BooleanGrammarParser import BooleanGrammarParser
else:
    from BooleanGrammarParser import BooleanGrammarParser

# This class defines a complete generic visitor for a parse tree produced by BooleanGrammarParser.

class BooleanGrammarVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by BooleanGrammarParser#start.
    def visitStart(self, ctx:BooleanGrammarParser.StartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BooleanGrammarParser#termChain.
    def visitTermChain(self, ctx:BooleanGrammarParser.TermChainContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BooleanGrammarParser#not.
    def visitNot(self, ctx:BooleanGrammarParser.NotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BooleanGrammarParser#or.
    def visitOr(self, ctx:BooleanGrammarParser.OrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BooleanGrammarParser#and.
    def visitAnd(self, ctx:BooleanGrammarParser.AndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BooleanGrammarParser#queryTerm.
    def visitQueryTerm(self, ctx:BooleanGrammarParser.QueryTermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by BooleanGrammarParser#parenthesis.
    def visitParenthesis(self, ctx:BooleanGrammarParser.ParenthesisContext):
        return self.visitChildren(ctx)



del BooleanGrammarParser