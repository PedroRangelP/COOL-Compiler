from util.exceptions import *
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser

class dummyListener(coolListener):

    def __init__(self):
        self.main = False
        self.klassInt = False
        self.hasNamedSelf = False
        self.klassInheritsBool = False
        self.klassInheritsSelf = False
        self.klassInheritsString = False
        self.letHasNamedSelf = False
        self.klassObject = False
        self.selfAssignment = False

    def enterKlass(self, ctx:coolParser.KlassContext):
        if ctx.TYPE(0).getText() == 'Main':
            self.main = True
        if ctx.TYPE(0).getText() == 'Int':
            self.klassInt = True
        if ctx.TYPE(0).getText() == 'Object':
            self.klassObject = True
        if (ctx.TYPE(1)):
            if ctx.TYPE(1).getText() == 'Bool':
                self.klassInheritsBool = True
            if ctx.TYPE(1).getText() == 'SELF_TYPE':
                self.klassInheritsSelf = True
            if ctx.TYPE(1).getText() == 'String':
                self.klassInheritsString = True

    def exitKlass(self, ctx:coolParser.KlassContext):
        if(not self.main):
            raise nomain()
        if(self.klassInt):
            raise badredefineint()
        if(self.klassObject):
            raise redefinedobject
        if(self.klassInheritsBool):
            raise inheritsbool()
        if(self.klassInheritsSelf):
            raise inheritsselftype()
        if(self.klassInheritsString):
            raise inheritsstring()

    def enterFeature(self, ctx: coolParser.FeatureContext):
        if ctx.ID().getText() == 'self':
            self.hasNamedSelf = True
        if ctx.expr():
            if(ctx.expr().getText() == 'self'):
                self.selfAssignment = True                

        # if ctx.params:
        #     for param in ctx.param:
        #         if(param.ID().getText() == 'self'):
        #             self.selfAssignment = True

            

    def exitFeature(self, ctx: coolParser.FeatureContext):
        if self.hasNamedSelf:
            raise anattributenamedself()
        if self.selfAssignment:
            raise selfassignment()

    def enterLet_decl(self, ctx: coolParser.Let_declContext):
        if ctx.ID().getText() == 'self':
            self.letHasNamedSelf = True

    def exitLet_decl(self, ctx: coolParser.Let_declContext):
        if self.letHasNamedSelf:
            raise letself()

