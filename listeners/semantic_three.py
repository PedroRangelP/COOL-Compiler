from util.exceptions import *
from util.structure import *
from util.structure import _allClasses
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.utils import utils

class semanticThreeListener(coolListener):
    def enterPrimary(self, ctx: coolParser.PrimaryContext):
        print("PRIMARY: " + ctx.getText())

        if ctx.ID():
            name = ctx.ID().getText()
            # Going up the nodes until we find one which contains a symbol table (scope)
            symbol_table = utils.getScope(ctx)
            current_klass = utils.getKlass(ctx)

            # print(symbol_table)
            # print(name)

            if name == "self":
                ctx.type = current_klass.name
            else:
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

    def exitPrimary(self, ctx: coolParser.PrimaryContext):
        if ctx.expr():
            ctx.type = ctx.expr().type
    
    def exitExpr_primary(self, ctx: coolParser.Expr_primaryContext):
        ctx.type = ctx.getChild(0).type

    def enterNew_type(self, ctx: coolParser.New_typeContext):
        klass_name = ctx.TYPE().getText()
        up_klass = _allClasses[klass_name].lookupInheritance()

        ctx.type = klass_name if up_klass == 'Object' else up_klass

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
    
    def enterLet_in(self, ctx: coolParser.Let_inContext):
        symbol_table = utils.getScope(ctx)

        # Assign the symbol table to the context of LET_IN
        ctx.symbol_table = symbol_table

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

    def exitLet_decl(self, ctx: coolParser.Let_declContext):
        let_type = ctx.TYPE().getText()
        
        if (ctx.expr()):
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
    
    def exitWhile(self, ctx: coolParser.WhileContext):
        while_condition = ctx.expr(0)
        while_body = ctx.expr(1)

        if while_condition.type != 'Bool':
            raise badwhilecond()
    
    def exitDispatch(self, ctx: coolParser.DispatchContext):
        symbol_table = utils.getScope(ctx)
        
        name = ctx.expr(0).getText()
        try:
            klass_type = symbol_table[name]
        except:
            klass_type = ctx.expr(0).type

        method_name = ctx.ID().getText()

        try:
            # If the method does not exist for the given class it will raise a KeyError
            _allClasses[klass_type].lookupMethod(method_name)
        except:
            keyErr = True

        if(keyErr): raise baddispatch()
    
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