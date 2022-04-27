from util.exceptions import *
from util.structure import *
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser

class semanticTwoListener(coolListener):
    def __init__(self):
        setBaseKlasses()
