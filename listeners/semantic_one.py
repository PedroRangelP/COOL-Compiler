from util.exceptions import *
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser

class semanticOneListener(coolListener):

    def __init__(self):
        self.main = False
        self.klassInt = False
        self.klassObject = False
        self.klassSelfType = False
        self.hasNamedSelf = False
        self.klassInheritsBool = False
        self.klassInheritsSelf = False
        self.klassInheritsString = False
        self.letHasNamedSelf = False
        self.selfAssignment = False
        self.selfInformalParameter = False
        self.selfTypeInformalParameter = False

    def enterKlass(self, ctx:coolParser.KlassContext):
        class_type = ctx.TYPE(0).getText()

        if class_type == 'Main':
            self.main = True
        if class_type == 'Int':
            self.klassInt = True
        if class_type == 'Object':
            self.klassObject = True
        if class_type == 'SELF_TYPE':
            self.klassSelfType = True
        if ctx.TYPE(1):
            class_type = ctx.TYPE(1).getText()
            if class_type == 'Bool':
                self.klassInheritsBool = True
            if class_type == 'SELF_TYPE':
                self.klassInheritsSelf = True
            if class_type == 'String':
                self.klassInheritsString = True

    def exitKlass(self, ctx:coolParser.KlassContext):
        if not self.main: raise nomain()
        if self.klassInt: raise badredefineint()
        if self.klassObject: raise redefinedobject()
        if self.klassSelfType: raise selftyperedeclared()
        if self.klassInheritsBool: raise inheritsbool()
        if self.klassInheritsSelf: raise inheritsselftype()
        if self.klassInheritsString: raise inheritsstring()

    def enterAttribute(self, ctx: coolParser.AttributeContext):
        if ctx.ID().getText() == 'self':
            self.hasNamedSelf = True

    def exitAttribute(self, ctx: coolParser.AttributeContext):
        if self.hasNamedSelf:
            raise anattributenamedself()

    def enterAssignment(self, ctx: coolParser.AssignmentContext):
        if ctx.ID():
            if(ctx.ID().getText() == 'self'):
                self.selfAssignment = True

    def exitAssignment(self, ctx: coolParser.AssignmentContext):
        if self.selfAssignment:
            raise selfassignment()

    # Params
    def enterFormal(self, ctx: coolParser.FormalContext):
        if ctx.ID().getText() == 'self':
            self.selfInformalParameter = True
        if ctx.TYPE().getText() == 'SELF_TYPE':
            self.selfTypeInformalParameter = True
    
    def exitFormal(self, ctx: coolParser.FormalContext):
        if self.selfInformalParameter:
            raise selfinformalparameter()
        if self.selfTypeInformalParameter:
            raise selftypeparameterposition()

    def enterLet_decl(self, ctx: coolParser.Let_declContext):
        if ctx.ID().getText() == 'self':
            self.letHasNamedSelf = True

    def exitLet_decl(self, ctx: coolParser.Let_declContext):
        if self.letHasNamedSelf:
            raise letself()

