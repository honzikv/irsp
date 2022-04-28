# Generated from C:/dev/ir/irsp/resources/anltr\BooleanGrammar.g4 by ANTLR 4.10.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .BooleanGrammarParser import BooleanGrammarParser
else:
    from BooleanGrammarParser import BooleanGrammarParser

# This class defines a complete listener for a parse tree produced by BooleanGrammarParser.
class BooleanGrammarListener(ParseTreeListener):

    # Enter a parse tree produced by BooleanGrammarParser#start.
    def enterStart(self, ctx:BooleanGrammarParser.StartContext):
        pass

    # Exit a parse tree produced by BooleanGrammarParser#start.
    def exitStart(self, ctx:BooleanGrammarParser.StartContext):
        pass


    # Enter a parse tree produced by BooleanGrammarParser#termChain.
    def enterTermChain(self, ctx:BooleanGrammarParser.TermChainContext):
        pass

    # Exit a parse tree produced by BooleanGrammarParser#termChain.
    def exitTermChain(self, ctx:BooleanGrammarParser.TermChainContext):
        pass


    # Enter a parse tree produced by BooleanGrammarParser#not.
    def enterNot(self, ctx:BooleanGrammarParser.NotContext):
        pass

    # Exit a parse tree produced by BooleanGrammarParser#not.
    def exitNot(self, ctx:BooleanGrammarParser.NotContext):
        pass


    # Enter a parse tree produced by BooleanGrammarParser#or.
    def enterOr(self, ctx:BooleanGrammarParser.OrContext):
        pass

    # Exit a parse tree produced by BooleanGrammarParser#or.
    def exitOr(self, ctx:BooleanGrammarParser.OrContext):
        pass


    # Enter a parse tree produced by BooleanGrammarParser#and.
    def enterAnd(self, ctx:BooleanGrammarParser.AndContext):
        pass

    # Exit a parse tree produced by BooleanGrammarParser#and.
    def exitAnd(self, ctx:BooleanGrammarParser.AndContext):
        pass


    # Enter a parse tree produced by BooleanGrammarParser#queryTerm.
    def enterQueryTerm(self, ctx:BooleanGrammarParser.QueryTermContext):
        pass

    # Exit a parse tree produced by BooleanGrammarParser#queryTerm.
    def exitQueryTerm(self, ctx:BooleanGrammarParser.QueryTermContext):
        pass


    # Enter a parse tree produced by BooleanGrammarParser#parenthesis.
    def enterParenthesis(self, ctx:BooleanGrammarParser.ParenthesisContext):
        pass

    # Exit a parse tree produced by BooleanGrammarParser#parenthesis.
    def exitParenthesis(self, ctx:BooleanGrammarParser.ParenthesisContext):
        pass



del BooleanGrammarParser