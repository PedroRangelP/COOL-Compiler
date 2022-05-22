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

    def exitExpr_primary(self, ctx: coolParser.Expr_primaryContext):
        ctx.type = ctx.getChild(0).type

    def enterPrimary(self, ctx: coolParser.PrimaryContext):
        if ctx.ID():
            name = ctx.ID().getText()
            # Going up the nodes until we find one which contains a symbol table (scope)
            symbol_table = utils.getScope(ctx)
            current_klass = utils.getKlass(ctx)

            # print(symbol_table)
            # print(name)

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
                
                # If the formal param has already been defined
                if any(id in param for param in params):
                    raise dupformals()
                
                params.append((id, function_type))
            
            method = Method(function_type, params=params)
        else:
            method = Method(function_type)

        name = ctx.ID().getText()

        override = False
        method_lookup = Method(function_type)
        
        try:
            # Check if the method already exists
            method_lookup = ctx.current_klass.lookupMethod(name)
            
            # Check if is overriding the method
            if method != method_lookup:
                override = True
        except:
            # Add the method if not exists
            ctx.current_klass.addMethod(name, method)

        # If the params are different
        if override:
            # If the number of params differs
            if len(method_lookup.params) != len(method.params):
                raise signaturechange()
            
            # If the type of the params differs
            raise overridingmethod4()

        # Appending a new dictionary to the array (Opening a scope)
        ctx.symbol_table.openScope()
        
        # Adding the params to the symboltable of this scope
        for id, function_type in params:
            ctx.symbol_table[id] = function_type
        
        # print(ctx.symbol_table)
    
    
    def exitFunction(self, ctx: coolParser.FunctionContext):
        # Pop the last dictionary in the array (Close a scope)
        ctx.symbol_table.closeScope()

    def exitWhile(self, ctx: coolParser.WhileContext):
        while_condition = ctx.expr(0)
        while_body = ctx.expr(1)

        if while_condition.type != 'Bool':
            raise badwhilecond()

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
    
    def enterLet_in(self, ctx: coolParser.Let_inContext):
        symbol_table = utils.getScope(ctx)
        current_klass = utils.getKlass(ctx)

        # Assign the symbol table to the context of LET_IN
        ctx.symbol_table = symbol_table
        ctx.current_klass = current_klass

        # Appending a new dictionary to the array (Opening a scope)
        ctx.symbol_table.openScope()
        
        # Adding the params to the symboltable of this scope
        for decl in ctx.let_decl():
            decl_id = decl.ID().getText()
            decl_type = decl.TYPE().getText()
            ctx.symbol_table[decl_id] = decl_type

    
    def exitLet_in(self, ctx: coolParser.Let_inContext):
        # Pop the last dictionary in the array (Close a scope)
        ctx.symbol_table.closeScope()

    def enterDispatch(self, ctx: coolParser.DispatchContext):
        symbol_table = utils.getScope(ctx)
        
        # Class name: cow
        klass_name = ctx.expr(0).getText()
        # Klass type: Animal
        klass_type = symbol_table[klass_name]
        # Method name: moo
        method_name = ctx.ID().getText()

        try:
            # If the method does not exist for the given class it will raise a KeyError
            _allClasses[klass_type].lookupMethod(method_name)
        except:
            keyErr = True

        if(keyErr): raise baddispatch()
    
    def enterNew_type(self, ctx: coolParser.New_typeContext):
        ctx.type = ctx.TYPE().getText()

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
    
    def enterMethod(self, ctx: coolParser.MethodContext):
        ctx.name = ctx.ID().getText()