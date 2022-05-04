from util.exceptions import *
from util.structure import *
from util.structure import _allClasses
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser

class semanticTwoListener(coolListener):
    def __init__(self):
        # Clearing classes before every new test
        _allClasses.clear()
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

    def exitArith(self, ctx: coolParser.ArithContext):
        if ctx.expr(0).type != 'Int' or ctx.expr(1).type != 'Int':
            raise badarith()

    def enterKlass(self, ctx: coolParser.KlassContext):
        class_type1 = ctx.TYPE(0).getText()

        if class_type1 in _allClasses:
            raise redefinedclass()

        # If an inherits exists
        if ctx.TYPE(1):
            class_type2 = ctx.TYPE(1).getText()
            
            if class_type2 not in _allClasses:
                raise missingclass()
            else:
                k = Klass(class_type1, class_type2)
        else:
            k = Klass(class_type1)
        
