# Generated from C:/dev/ir/irsp/resources/anltr\BooleanGrammar.g4 by ANTLR 4.10.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,7,41,2,0,7,0,2,1,7,1,2,2,7,2,1,0,1,0,1,1,1,1,1,1,1,1,3,1,13,
        8,1,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,3,2,24,8,2,1,2,1,2,1,2,1,
        2,1,2,1,2,1,2,1,2,1,2,1,2,5,2,36,8,2,10,2,12,2,39,9,2,1,2,0,1,4,
        3,0,2,4,0,0,42,0,6,1,0,0,0,2,12,1,0,0,0,4,23,1,0,0,0,6,7,3,4,2,0,
        7,1,1,0,0,0,8,13,5,7,0,0,9,10,5,7,0,0,10,11,5,6,0,0,11,13,3,2,1,
        0,12,8,1,0,0,0,12,9,1,0,0,0,13,3,1,0,0,0,14,15,6,2,-1,0,15,16,5,
        4,0,0,16,17,3,4,2,0,17,18,5,5,0,0,18,24,1,0,0,0,19,20,5,3,0,0,20,
        21,5,6,0,0,21,24,3,4,2,4,22,24,3,2,1,0,23,14,1,0,0,0,23,19,1,0,0,
        0,23,22,1,0,0,0,24,37,1,0,0,0,25,26,10,3,0,0,26,27,5,6,0,0,27,28,
        5,1,0,0,28,29,5,6,0,0,29,36,3,4,2,4,30,31,10,2,0,0,31,32,5,6,0,0,
        32,33,5,2,0,0,33,34,5,6,0,0,34,36,3,4,2,3,35,25,1,0,0,0,35,30,1,
        0,0,0,36,39,1,0,0,0,37,35,1,0,0,0,37,38,1,0,0,0,38,5,1,0,0,0,39,
        37,1,0,0,0,4,12,23,35,37
    ]

class BooleanGrammarParser ( Parser ):

    grammarFileName = "BooleanGrammar.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'AND'", "'OR'", "'NOT'", "'('", "')'" ]

    symbolicNames = [ "<INVALID>", "AND", "OR", "NOT", "LPAR", "RPAR", "WHITESPACE", 
                      "QUERY_TERM" ]

    RULE_start = 0
    RULE_termChain = 1
    RULE_expression = 2

    ruleNames =  [ "start", "termChain", "expression" ]

    EOF = Token.EOF
    AND=1
    OR=2
    NOT=3
    LPAR=4
    RPAR=5
    WHITESPACE=6
    QUERY_TERM=7

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.10.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class StartContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(BooleanGrammarParser.ExpressionContext,0)


        def getRuleIndex(self):
            return BooleanGrammarParser.RULE_start

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStart" ):
                listener.enterStart(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStart" ):
                listener.exitStart(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStart" ):
                return visitor.visitStart(self)
            else:
                return visitor.visitChildren(self)




    def start(self):

        localctx = BooleanGrammarParser.StartContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_start)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 6
            self.expression(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TermChainContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def QUERY_TERM(self):
            return self.getToken(BooleanGrammarParser.QUERY_TERM, 0)

        def WHITESPACE(self):
            return self.getToken(BooleanGrammarParser.WHITESPACE, 0)

        def termChain(self):
            return self.getTypedRuleContext(BooleanGrammarParser.TermChainContext,0)


        def getRuleIndex(self):
            return BooleanGrammarParser.RULE_termChain

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTermChain" ):
                listener.enterTermChain(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTermChain" ):
                listener.exitTermChain(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTermChain" ):
                return visitor.visitTermChain(self)
            else:
                return visitor.visitChildren(self)




    def termChain(self):

        localctx = BooleanGrammarParser.TermChainContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_termChain)
        try:
            self.state = 12
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 8
                self.match(BooleanGrammarParser.QUERY_TERM)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 9
                self.match(BooleanGrammarParser.QUERY_TERM)
                self.state = 10
                self.match(BooleanGrammarParser.WHITESPACE)
                self.state = 11
                self.termChain()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return BooleanGrammarParser.RULE_expression

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class NotContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BooleanGrammarParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NOT(self):
            return self.getToken(BooleanGrammarParser.NOT, 0)
        def WHITESPACE(self):
            return self.getToken(BooleanGrammarParser.WHITESPACE, 0)
        def expression(self):
            return self.getTypedRuleContext(BooleanGrammarParser.ExpressionContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNot" ):
                listener.enterNot(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNot" ):
                listener.exitNot(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNot" ):
                return visitor.visitNot(self)
            else:
                return visitor.visitChildren(self)


    class OrContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BooleanGrammarParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BooleanGrammarParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(BooleanGrammarParser.ExpressionContext,i)

        def WHITESPACE(self, i:int=None):
            if i is None:
                return self.getTokens(BooleanGrammarParser.WHITESPACE)
            else:
                return self.getToken(BooleanGrammarParser.WHITESPACE, i)
        def OR(self):
            return self.getToken(BooleanGrammarParser.OR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOr" ):
                listener.enterOr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOr" ):
                listener.exitOr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOr" ):
                return visitor.visitOr(self)
            else:
                return visitor.visitChildren(self)


    class AndContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BooleanGrammarParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BooleanGrammarParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(BooleanGrammarParser.ExpressionContext,i)

        def WHITESPACE(self, i:int=None):
            if i is None:
                return self.getTokens(BooleanGrammarParser.WHITESPACE)
            else:
                return self.getToken(BooleanGrammarParser.WHITESPACE, i)
        def AND(self):
            return self.getToken(BooleanGrammarParser.AND, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAnd" ):
                listener.enterAnd(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAnd" ):
                listener.exitAnd(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAnd" ):
                return visitor.visitAnd(self)
            else:
                return visitor.visitChildren(self)


    class QueryTermContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BooleanGrammarParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def termChain(self):
            return self.getTypedRuleContext(BooleanGrammarParser.TermChainContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQueryTerm" ):
                listener.enterQueryTerm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQueryTerm" ):
                listener.exitQueryTerm(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitQueryTerm" ):
                return visitor.visitQueryTerm(self)
            else:
                return visitor.visitChildren(self)


    class ParenthesisContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BooleanGrammarParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAR(self):
            return self.getToken(BooleanGrammarParser.LPAR, 0)
        def expression(self):
            return self.getTypedRuleContext(BooleanGrammarParser.ExpressionContext,0)

        def RPAR(self):
            return self.getToken(BooleanGrammarParser.RPAR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParenthesis" ):
                listener.enterParenthesis(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParenthesis" ):
                listener.exitParenthesis(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParenthesis" ):
                return visitor.visitParenthesis(self)
            else:
                return visitor.visitChildren(self)



    def expression(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = BooleanGrammarParser.ExpressionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 4
        self.enterRecursionRule(localctx, 4, self.RULE_expression, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 23
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [BooleanGrammarParser.LPAR]:
                localctx = BooleanGrammarParser.ParenthesisContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 15
                self.match(BooleanGrammarParser.LPAR)
                self.state = 16
                self.expression(0)
                self.state = 17
                self.match(BooleanGrammarParser.RPAR)
                pass
            elif token in [BooleanGrammarParser.NOT]:
                localctx = BooleanGrammarParser.NotContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 19
                self.match(BooleanGrammarParser.NOT)
                self.state = 20
                self.match(BooleanGrammarParser.WHITESPACE)
                self.state = 21
                self.expression(4)
                pass
            elif token in [BooleanGrammarParser.QUERY_TERM]:
                localctx = BooleanGrammarParser.QueryTermContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 22
                self.termChain()
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 37
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,3,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 35
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
                    if la_ == 1:
                        localctx = BooleanGrammarParser.AndContext(self, BooleanGrammarParser.ExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 25
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 26
                        self.match(BooleanGrammarParser.WHITESPACE)
                        self.state = 27
                        self.match(BooleanGrammarParser.AND)
                        self.state = 28
                        self.match(BooleanGrammarParser.WHITESPACE)
                        self.state = 29
                        self.expression(4)
                        pass

                    elif la_ == 2:
                        localctx = BooleanGrammarParser.OrContext(self, BooleanGrammarParser.ExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 30
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 31
                        self.match(BooleanGrammarParser.WHITESPACE)
                        self.state = 32
                        self.match(BooleanGrammarParser.OR)
                        self.state = 33
                        self.match(BooleanGrammarParser.WHITESPACE)
                        self.state = 34
                        self.expression(3)
                        pass

             
                self.state = 39
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,3,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[2] = self.expression_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expression_sempred(self, localctx:ExpressionContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 2)
         




