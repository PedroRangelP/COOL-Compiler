from antlr4 import *
from antlr.coolLexer import coolLexer
from antlr.coolParser import coolParser

from listeners.semantic_one import semanticOneListener
from listeners.semantic_two import semanticTwoListener
from listeners.semantic_three import semanticThreeListener

def compile(file):
    parser = coolParser(CommonTokenStream(coolLexer(FileStream(file))))
    tree = parser.program()

    walker = ParseTreeWalker()
    
    walker.walk(semanticOneListener(), tree)
    walker.walk(semanticTwoListener(), tree)
    walker.walk(semanticThreeListener(), tree)

if __name__ == '__main__':
    compile('resources/semantic/input/badargs1.cool')
