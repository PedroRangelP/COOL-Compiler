from util.exceptions import *
from util.structure import *
from util.structure import _allClasses
from util.utils import utils
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser

class semanticThreeListener(coolListener):
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

        if (type(ctx.parentCtx) is coolParser.PrimaryContext):
            ctx.type = klass_name
        else:
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

    def enterMethod(self, ctx: coolParser.MethodContext):
        # Appending a new dictionary to the array (Opening a scope)
        ctx.symbol_table.openScope()
        
        # Adding the params to the symboltable of this scope
        for name, type in ctx.method.params.items():
            ctx.symbol_table[name] = type
        
        # print(ctx.symbol_table)
    
    def exitMethod(self, ctx: coolParser.MethodContext):
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
    
    def enterMethod_call(self, ctx: coolParser.Method_callContext):
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

        # Get the class either by the symbol table or by the attribute of the node
        try:
            klass_type = symbol_table[name]
        except:
            klass_type = ctx.expr(0).type

        print("KLASS TYPE: " + klass_type)
        method_name = ctx.ID().getText()

        try:
            # If the method does not exist for the given class it will raise a KeyError
            method_lookup = _allClasses[klass_type].lookupMethod(method_name)
        except:
            raise baddispatch()
        
        param_idx = 0
        for name in method_lookup.params:
            # Check if the types of the dispatch argss are the same as the method signature
            if (not method_lookup.params[name] == ctx.params[param_idx].type):
                raise badargs1()
    
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