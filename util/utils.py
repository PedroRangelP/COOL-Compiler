class utils():
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