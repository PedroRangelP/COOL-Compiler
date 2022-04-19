from util.exceptions import *
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser

class dummyListener(coolListener):

    def __init__(self):
        self.main = False

    def enterKlass(self, ctx:coolParser.KlassContext):
        if ctx.TYPE(0).getText() == 'Main':
            self.main = True

        if ctx.TYPE(0).getText() == 'Int':
            self.klassInt = True

    def exitKlass(self, ctx:coolParser.KlassContext):
        if (not self.main):
            raise nomain()
        if(self.klassInt):
            raise badredefineint()

    def enterFeature(self, ctx: coolParser.FeatureContext):
        if ctx.ID().getText() == 'self':
            self.hasNamedSelf = True

    def exitFeature(self, ctx: coolParser.FeatureContext):
        if (self.hasNamedSelf):
            raise anattributenamedself()

