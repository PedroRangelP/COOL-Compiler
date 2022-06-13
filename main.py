from antlr4 import *
from antlr.coolLexer import coolLexer
from antlr.coolParser import coolParser

from listeners.semantic_one import semanticOneListener
from listeners.semantic_two import semanticTwoListener
from listeners.semantic_three import semanticThreeListener
from listeners.semantic_tree import TreePrinter
from listeners.datasegment import DataGenerator
# from listeners.textsegment import TextGenerator

def compile(file):
    parser = coolParser(CommonTokenStream(coolLexer(FileStream(file))))
    tree = parser.program()

    # textGen = TextGenerator()
    dataGen = DataGenerator()

    walker = ParseTreeWalker()
    
    walker.walk(semanticOneListener(), tree)
    walker.walk(semanticTwoListener(), tree)
    walker.walk(semanticThreeListener(), tree)
    walker.walk(TreePrinter(), tree)

    # # Por las constantes, ahora dataGen debe ir ANTES
    # walker.walk(dataGen, tree)
    # # walker.walk(textGen, tree)

    # with open('test.asm', "w") as writer:
    #     writer.write(dataGen.result)
    #     # writer.write(textGen.result)

if __name__ == '__main__':
    compile('resources/semantic/input/hairyscary.cool')
