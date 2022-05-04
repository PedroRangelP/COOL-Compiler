from antlr4 import *
from antlr.coolLexer import coolLexer
from antlr.coolParser import coolParser

from listeners.semantic_one import semanticOneListener
from listeners.semantic_two import semanticTwoListener

def compile(file):
    parser = coolParser(CommonTokenStream(coolLexer(FileStream(file))))
    tree = parser.program()

    walker = ParseTreeWalker()
    
    walker.walk(semanticOneListener(), tree)
    walker.walk(semanticTwoListener(), tree)

if __name__ == '__main__':
    compile('resources/semantic/input/missingclass.cool')
