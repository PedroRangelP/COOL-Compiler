from util.exceptions import *
from util.structure import *
from util.structure import _allClasses
from util.utils import utils
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser

class semanticOneListener(coolListener):
    def __init__(self):
        # Clearing classes before every new test
        _allClasses.clear()
        setBaseKlasses()

    def enterProgram(self, ctx: coolParser.ProgramContext):
        ctx.klasses_dict = SymbolTable()
        
        # Adding base classes to the dictionary
        ctx.klasses_dict['Object'] = 'Object'
        ctx.klasses_dict['IO'] = 'Object'
        ctx.klasses_dict['Int'] = 'Object'
        ctx.klasses_dict['String'] = 'Object'
        ctx.klasses_dict['Bool'] = 'Object'
    
    def exitProgram(self, ctx: coolParser.ProgramContext):
        if 'Main' not in ctx.klasses_dict:
            raise nomain()
        
        for klass in ctx.klasses_dict:
            inherits = ctx.klasses_dict[klass]
            # if (inherits != 'Object'):
                # Checking if it inherits from non existing class
            if inherits not in ctx.klasses_dict:
                raise missingclass()
    
    def enterKlass(self, ctx:coolParser.KlassContext):
        klass_type = ctx.TYPE(0).getText()
        klasses_dict = utils.getKlasses(ctx)

        if klass_type == 'Int':
            raise badredefineint()
        if klass_type == 'Object':
            raise redefinedobject()
        if klass_type == 'SELF_TYPE':
            raise selftyperedeclared()
        
        if klass_type in klasses_dict:
            raise redefinedclass()

        if ctx.TYPE(1):
            inherits_type = ctx.TYPE(1).getText()
            if inherits_type == 'Bool':
                raise inheritsbool()
            if inherits_type == 'SELF_TYPE':
                raise inheritsselftype()
            if inherits_type == 'String':
                raise inheritsstring()
            
            klasses_dict[klass_type] = inherits_type
        else:
            klasses_dict[klass_type] = 'Object'

    def enterAttribute(self, ctx: coolParser.AttributeContext):
        if ctx.ID().getText() == 'self':
            raise anattributenamedself()

    def enterAssignment(self, ctx: coolParser.AssignmentContext):
        if ctx.ID():
            if(ctx.ID().getText() == 'self'):
                raise selfassignment()

    # Params
    def enterFormal(self, ctx: coolParser.FormalContext):
        if ctx.ID().getText() == 'self':
            raise selfinformalparameter()
        if ctx.TYPE().getText() == 'SELF_TYPE':
            raise selftypeparameterposition()

    def enterLet_decl(self, ctx: coolParser.Let_declContext):
        if ctx.ID().getText() == 'self':
            raise letself()