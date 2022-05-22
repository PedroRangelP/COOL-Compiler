from turtle import right
from util.exceptions import *
from util.structure import *
from util.structure import _allClasses
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.utils import utils

class semanticThreeListener(coolListener):
    def exitAssignment(self, ctx: coolParser.AssignmentContext):
        symbol_table = utils.getScope(ctx)
        
        left_type = symbol_table[ctx.ID().getText()]
        right_type = ctx.expr().type

        if left_type in _allClasses:
            l_klass = _allClasses[left_type]

        if right_type in _allClasses:
            r_klass = _allClasses[right_type]

        if not l_klass.conforms(r_klass):
            raise assignnoconform()

    def exitLet_decl(self, ctx: coolParser.Let_declContext):
        let_type = ctx.TYPE().getText()
        expr_type = ctx.expr().type

        if(let_type != expr_type):
            raise letbadinit()
    
    def enterMethod(self, ctx: coolParser.MethodContext):
        name = ctx.ID().getText()

        if len(ctx.params) > 0:
            for param in ctx.params:
                paramName = ''

                try:
                    paramName = param.ID().getText()
                except:
                    paramName = ''

                if (paramName == name): raise badmethodcallsitself()