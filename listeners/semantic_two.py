from util.exceptions import *
from util.structure import *
from util.structure import _allClasses
from util.utils import utils
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser

class semanticTwoListener(coolListener):
    def enterKlass(self, ctx: coolParser.KlassContext):
        klasses_dict = utils.getKlasses(ctx)
        klass= ctx.TYPE(0).getText()

        nonDefinedKlasses = utils.getInheritanceNonDefined(klasses_dict, _allClasses, klass)

        while nonDefinedKlasses:
            name = nonDefinedKlasses.pop()
            inherits = klasses_dict[name]
            Klass(name, inherits)

        if klass in _allClasses:
            k = _allClasses[klass]
        else:
            k = Klass(klass, klasses_dict[klass])
        
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
    
    def enterMethod(self, ctx: coolParser.MethodContext):
        method_type = ctx.TYPE().getText()
        
        # If we set the return type to be a non existant class/type
        if method_type != 'SELF_TYPE':
            if method_type not in _allClasses:
                raise returntypenoexist()
            
        # When we return a SELF_TYPE it should have the following structure
        # foo() : SELF_TYPE { self } || foo() : SELF_TYPE { new SELF_TYPE }
        # Using the new keyword to instantiate the class is not valid
        # foo() : SELF_TYPE { new Class }
        if method_type == 'SELF_TYPE':
            if ctx.expr().getText() != 'self' or ctx.expr().getText() != 'newSELF_TYPE':
                raise selftypebadreturn()
        
        params = []
        # Saving params if they exist in the function
        if len(ctx.params) > 0:
            for param in ctx.params:
                param_name = param.ID().getText()
                param_type = param.TYPE().getText()
                
                # If the formal param has already been defined
                if any(param_name in param for param in params):
                    raise dupformals()
                
                params.append((param_name, param_type))
            
            method = Method(method_type, params=params)
        else:
            method = Method(method_type)

        name = ctx.ID().getText()
        params_override = False
        signature_override = False
        try:
            # Check if the method already exists
            method_lookup = ctx.current_klass.lookupMethod(name)

            # If the number of params differs
            if len(method_lookup.params) != len(method.params):
                signature_override = True
            
            # If the params are different
            if method_lookup.params != method.params:
                params_override = True
        except:
            # Add the method if not exists
            ctx.current_klass.addMethod(name, method)
        
        # If overriding raise the exeption
        if signature_override: raise signaturechange()
        if params_override: raise overridingmethod4()

        # Saving the method in this node
        ctx.method = method

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