class utils():
    terminal_symbols = [";", "}", ")"]

    def getKlass(ctx):
        parent = ctx.parentCtx

        # Getting the parent nodes until we reach the cuerrent class
        while parent and (not hasattr(parent, "current_klass")):
            parent = parent.parentCtx
        return parent.current_klass

    def getScope(ctx):
        parent = ctx.parentCtx

        # Getting the parent nodes until we reach the symbol table of the scope
        while parent and (not hasattr(parent, "symbol_table")):
            parent = parent.parentCtx
        return parent.symbol_table

    def getKlasses(ctx):
        parent = ctx.parentCtx

        while parent and (not hasattr(parent, "klasses_dict")):
            parent = parent.parentCtx
        return parent.klasses_dict
    
    def getInheritanceNonDefined(klasses_dic, _allClasses, klass):
        nonDefinedKlasses = []
        inheritance = klasses_dic[klass]

        while inheritance != 'Object':
            if inheritance not in _allClasses:
                nonDefinedKlasses.append(inheritance)
            inheritance = klasses_dic[inheritance]
        
        return nonDefinedKlasses