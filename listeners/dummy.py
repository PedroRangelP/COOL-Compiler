from util.exceptions import *
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser

class dummyListener(coolListener):

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
        if ctx.TYPE(0).getText() == 'Main':
            self.main = True
        if ctx.TYPE(0).getText() == 'Int':
            self.klassInt = True
        if ctx.TYPE(0).getText() == 'Object':
            self.klassObject = True
        if ctx.TYPE(0).getText() == 'SELF_TYPE':
            self.klassSelfType = True
        if ctx.TYPE(1):
            if ctx.TYPE(1).getText() == 'Bool':
                self.klassInheritsBool = True
            if ctx.TYPE(1).getText() == 'SELF_TYPE':
                self.klassInheritsSelf = True
            if ctx.TYPE(1).getText() == 'String':
                self.klassInheritsString = True

    def exitKlass(self, ctx:coolParser.KlassContext):
        if not self.main: raise nomain()
        if self.klassInt: raise badredefineint()
        if self.klassObject: raise redefinedobject()
        if self.klassSelfType: raise selftyperedeclared()
        if self.klassInheritsBool: raise inheritsbool()
        if self.klassInheritsSelf: raise inheritsselftype()
        if self.klassInheritsString: raise inheritsstring()

    def enterFeature(self, ctx: coolParser.FeatureContext):
        if ctx.ID().getText() == 'self':
            self.hasNamedSelf = True

    def exitFeature(self, ctx: coolParser.FeatureContext):
        if self.hasNamedSelf:
            raise anattributenamedself()

    def enterExpr(self, ctx: coolParser.ExprContext):
        if ctx.ID():
            if(ctx.ID().getText() == 'self'):
                self.selfAssignment = True

    def exitExpr(self, ctx: coolParser.ExprContext):
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

