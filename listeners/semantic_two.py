from util.exceptions import *
from util.structure import *
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser

class semanticTwoListener(coolListener):
    def __init__(self):
        setBaseKlasses()

    def exitExpr_primary(self, ctx: coolParser.Expr_primaryContext):
        ctx.type = ctx.getChild(0).type

    def enterPrimary(self, ctx: coolParser.PrimaryContext):
        if ctx.ID():
            ctx.type = 'Id'
        if ctx.INTEGER():
            ctx.type = 'Int'
        if ctx.STRING():
            ctx.type = 'String'
        if ctx.TRUE() or ctx.FALSE():
            ctx.type = 'Bool'

    def enterArith(self, ctx: coolParser.ArithContext):
        if ctx.expr(0).type != 'Int' or ctx.expr(1).type != 'Int':
            raise badarith()
