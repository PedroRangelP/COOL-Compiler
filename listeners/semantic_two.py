from util.exceptions import *
from util.structure import *
from util.structure import _allClasses
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.utils import utils

class semanticTwoListener(coolListener):
    def __init__(self):
        # Clearing classes before every new test
        _allClasses.clear()
        setBaseKlasses()

    def enterKlass(self, ctx: coolParser.KlassContext):
        class_type1 = ctx.TYPE(0).getText()

        if class_type1 in _allClasses:
            raise redefinedclass()

        # If an inherits exists
        if ctx.TYPE(1):
            class_type2 = ctx.TYPE(1).getText()
            
            # Checking if it inherits from non existing class
            if class_type2 not in _allClasses:
                raise missingclass()
            else:
                k = Klass(class_type1, class_type2)
        else:
            k = Klass(class_type1)

        symbolTable = SymbolTableWithScopes(k)

        ctx.current_klass = k

        for feature in ctx.feature():
            feature.current_klass = k
            feature.symbol_table = symbolTable
    
    def enterAttribute(self, ctx: coolParser.AttributeContext):
        name = ctx.ID().getText()
        type = ctx.TYPE().getText()

        if ctx.expr():
            try:
            # If the method does not exist for the given class it will raise a KeyError
                expr = ctx.expr()
                ctx.current_klass.lookupAttribute(expr)
            except:
                raise attrbadinit()
        
        override = False
        try:
            # Check if the attribute already exists and store its type
            type_lookup = ctx.current_klass.lookupAttribute(name)
            
            # Check if is overriding the attribute type
            if type != type_lookup:
                override = True
        except:
            # Add the attribute if not exists
            ctx.current_klass.addAttribute(name, type)
        
        # If overriding raise the exeption
        if(override): raise attroverride()

    def enterCase_stat(self, ctx: coolParser.Case_statContext):
        name = ctx.ID().getText()
        type = ctx.TYPE().getText()
        
        symbol_table = utils.getScope(ctx)
        symbol_table[name] = type

    def exitCase_of(self, ctx: coolParser.Case_ofContext):
        used_types = []
        
        for case_stat in ctx.case_stat():
            case_type = case_stat.TYPE().getText()

            # Check if there are multiple branches with the same type
            if case_type in used_types:
                raise caseidenticalbranch()
            else:
                used_types.append(case_type)

    # def exitDispatch(self, ctx: coolParser.DispatchContext):
    #     if len(ctx.params) > 0:
    #         for param in ctx.params:
    #             try:
    #                 print(param.type)
    #             except:
    #                 print('No type')