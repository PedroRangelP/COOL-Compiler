from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.structure import _allClasses as allClasses, lookupClass
from util.utils import utils

import util.asm as asm

class DataGenerator(coolListener):
    def __init__(self):
        self.result = ''
        self.constants = 0

    def enterProgram(self, ctx: coolParser.ProgramContext):
        self.result += asm.tpl_start_data

    def enterAttribute(self, ctx: coolParser.AttributeContext):
        ctx_type = ctx.type
        ctx_value = 0
        ctx_varname = ctx.ID().getText()

        if(ctx.expr()):
            ctx_value = ctx.expr().getText()

        if ctx_type == 'Int':
            self.result += asm.tpl_attribute.substitute(
                varname=ctx_varname,
                value=ctx_value
            )
        if ctx_type == 'String':
            self.result += asm.tpl_attribute_string.substitute(
                varname=ctx_varname,
                value= '""' if ctx_value == 0 else ctx_value
            )
        if ctx_type == 'Bool':
            self.result += asm.tpl_attribute.substitute(
                varname=ctx_varname,
                value = 0 if (ctx_value == 'false' or ctx_value == 0) else 1
            )
        ctx.code = ''
     
    def createDispatchTable (self):
        for name in allClasses.keys():
            self.result += asm.tpl_dispatch_table.substitute(
                name = name, 
                methods = getMethods(lookupClass(name).methods)
            )
    
    def createClassNameTable (self):
        for name in allClasses.keys():
            self.result += asm.tpl_classname_table.substitute(
                name = name
                )
            
     
    def exitProgram(self, ctx: coolParser.ProgramContext):
        self.createClassNameTable()
        self.createDispatchTable()
        self.genGlobalData()
        self.heapStart()

def createPrototype(self):
    for klass_name in allClasses.keys():
        print(klass_name)
        # offset 0 Class tag
        # offset 4 Object size (in 32-bit words)
        # offset 8 Dispatch pointer
        # offset 12. . . Attributes 

        self.result += asm.tpl_prot_obj.substitute(
            Klass_tag=klass_name,
            object_size=getObjSize(lookupClass(klass_name)),
            dispatch_pointer=klass_name + "_dipatch"
        )

        attributes = lookupClass(klass_name).attributes
        
        for attr_name in attributes.keys():
            # Assembly template
            self.result += asm.tpl_prot_obj_attribute.substitute(
                attribute = attr_name
            )

        # Get all of the object attributes and methods

def getMethods (methodTable):
    methods = []
    for method in methodTable.keys():
        methods.append(method)
        
    return methods

def getObjSize (klass):
    sizes_by_klass = {
        'Object': 3,
        'IO': 3,
        'Int': 4,
        'Bool': 4,
        'String': 4,
    }
    
    size = 0
    current_klass = klass
    
    # Size based in number of attributes
    while current_klass.name not in sizes_by_klass:
        size += len(current_klass.attributes)
        current_klass = allClasses(current_klass.inherits)

    size += sizes_by_klass[current_klass.name]

    return size

def heapStart(self):
    self.result += """
        .globl heap_start
            heap_start
            .word 0
    """