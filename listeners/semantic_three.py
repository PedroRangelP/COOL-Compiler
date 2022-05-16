from turtle import right
from util.exceptions import *
from util.structure import *
from util.structure import _allClasses
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser

def getScope(ctx):
    parent = ctx.parentCtx

    # Getting the parent nodes until we reach the symbol table of the scope
    while parent and (not hasattr(parent, "symbol_table")) and (not hasattr(parent, "current_klass")):
        parent = parent.parentCtx
    return parent.symbol_table, parent.current_klass

class semanticThreeListener(coolListener):
    def exitAssignment(self, ctx: coolParser.AssignmentContext):
        symbol_table, current_klass = getScope(ctx)
        
        left_type = symbol_table[ctx.ID().getText()]
        right_type = ctx.expr().type

        if left_type in _allClasses:
            l_klass = _allClasses[left_type]

        if right_type in _allClasses:
            r_klass = _allClasses[right_type]

        if not l_klass.conforms(r_klass):
            raise assignnoconform()