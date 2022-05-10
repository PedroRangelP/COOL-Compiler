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


class semanticTwoListener(coolListener):
    def __init__(self):
        # Clearing classes before every new test
        _allClasses.clear()
        setBaseKlasses()

    def exitExpr_primary(self, ctx: coolParser.Expr_primaryContext):
        ctx.type = ctx.getChild(0).type

    def enterPrimary(self, ctx: coolParser.PrimaryContext):
        if ctx.ID():
            name = ctx.ID().getText()
            # Going up the nodes until we find one which contains a symbol table (scope)
            symbol_table, current_klass = getScope(ctx)

            if name == "self":
                ctx.type = current_klass.name
            
            # Once we find the symbol table we search the name of the variable (It is a dictionary)
            # and we obtain its type so we can assign it to our ctx.type
            if name in symbol_table:
                ctx.type = symbol_table[name]
            else:
                raise outofscope()
        
        if ctx.INTEGER():
            ctx.type = 'Int'
        if ctx.STRING():
            ctx.type = 'String'
        if ctx.TRUE() or ctx.FALSE():
            ctx.type = 'Bool'

    def exitArith(self, ctx: coolParser.ArithContext):
        if ctx.expr(0).type != 'Int' or ctx.expr(1).type != 'Int':
            raise badarith()
    
    def exitEquals(self, ctx: coolParser.EqualsContext):
        left = ctx.children[0].type
        right = ctx.children[2].type

        print(f"EQUALS: Left {left}, Right {right}")
        
        if left == 'Int':
            if right == 'String':
                raise badequalitytest()
            elif right == 'Bool':
                raise badequalitytest2()


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
    
    def enterFunction(self, ctx: coolParser.FunctionContext):
        function_type = ctx.TYPE().getText()

        # If we set the return type to be a non existant class/type
        if function_type != 'SELF_TYPE':
            if function_type not in _allClasses:
                raise returntypenoexist()
        
        # When we return a SELF_TYPE it should have the following structure
        # foo() : SELF_TYPE { self }
        # Using the new keyword to instantiate the class is not valid
        # foo() : SELF_TYPE { new Class }
        if function_type == 'SELF_TYPE':
            if ctx.expr().getText() != 'self':
                raise selftypebadreturn()
        
        params = []
        # Saving params if they exist in the function
        if len(ctx.params) > 0:
            for param in ctx.params:
                id = param.ID().getText()
                function_type = param.TYPE().getText()
                params.append((id, function_type))
            
            method = Method(function_type, params=params)
        else:
            method = Method(function_type)

        name = ctx.ID().getText()
        ctx.current_klass.addMethod(name, method)

        # Appending a new dictionary to the array (Opening a scope)
        ctx.symbol_table.openScope()
        
        # Adding the params to the symboltable of this scope
        for id, function_type in params:
            ctx.symbol_table[id] = function_type
        
    
    def exitFunction(self, ctx: coolParser.FunctionContext):
        # Pop the last dictionary in the array (Close a scope)
        ctx.symbol_table.closeScope()

    # def exitCase_of(self, ctx: coolParser.Case_ofContext):
    #     if ctx.case_stat(0).type == ctx.case_stat(1).type:
    #         raise  caseidenticalbranch()  
