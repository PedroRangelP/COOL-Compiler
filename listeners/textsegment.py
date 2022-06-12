from antlr.coolListener import coolListener
from antlr.coolParser import coolParser

import util.asm as asm

class TextGenerator(coolListener):
    def __init__(self):
        self.result = ''
        self.stack = []
        self.labels = 0

    def enterProgram(self, ctx: coolParser.ProgramContext):
        self.result += asm.tpl_start_text

    def exitProgram(self, ctx: coolParser.ProgramContext):
        for c in ctx.getChildren():
            self.result += c.code
        self.result += asm.tpl_end

    def exitPrimaria(self, ctx: coolParser.PrimariaContext):
        self.stack.append(
            asm.tpl_immediate.substitute(immediate=ctx.getText())
        )

    def exitPrimaria_string(self, ctx: coolParser.Primaria_stringContext):
        self.stack.append(
            asm.tpl_string_const.substitute(
                name=ctx.label
            )
        )

    def exitSuma(self, ctx: coolParser.SumaContext):
        self.stack.append(
            asm.tpl_suma.substitute(
                right=self.stack.pop(),
                left=self.stack.pop()
            )
        )

    def exitResta(self, ctx: coolParser.RestaContext):
        self.stack.append(
            asm.tpl_resta.substitute(
                right=self.stack.pop(),
                left=self.stack.pop()
            )
        )

    def exitAsignacion(self, ctx: coolParser.AsignacionContext):
        ctx.code = asm.tpl_asignacion.substitute(
            prev=self.stack.pop(),
            name=ctx.getChild(0).getText()
        )

    def exitVar(self, ctx: coolParser.VarContext):
        self.stack.append(
            asm.tpl_var.substitute(name=ctx.getText())
        )

    def exitPrintint(self, ctx: coolParser.PrintintContext):
        ctx.code = asm.tpl_print_int.substitute(
            prev=self.stack.pop()
        )

    def exitPrintstr(self, ctx: coolParser.PrintstrContext):
        ctx.code = asm.tpl_print_str.substitute(
            prev=self.stack.pop()
        )

    def exitIf(self, ctx: coolParser.IfContext):
        self.labels = self.labels = self.labels + 1
        ctx.code = asm.tpl_if.substitute(
            prev=self.stack.pop(),
            n=self.labels,
            stmt_true=ctx.statement(0).code
        )

    def exitIfelse(self, ctx: coolParser.IfelseContext):
        self.labels = self.labels = self.labels + 1
        ctx.code = asm.tpl_if_else.substitute(
            prev=self.stack.pop(),
            n=self.labels,
            stmt_true=ctx.statement(0).code,
            stmt_false=ctx.statement(1).code
        )

    def exitBlock(self, ctx: coolParser.BlockContext):
        ctx.code = ''
        for c in ctx.statement():
            ctx.code += c.code

    def exitWhile(self, ctx: coolParser.WhileContext):
        self.labels = self.labels + 1
        ctx.code = asm.tpl_while.substitute(
            test=self.stack.pop(),
            n=self.labels,
            stmt=ctx.statement().code
        )

    def exitProcedure(self, ctx: coolParser.ProcedureContext):
        # No me importan las variables ヽ(°〇°)ﾉ
        ctx.code = asm.tpl_procedure.substitute(
            name=ctx.name.text,
            code=ctx.statement().code
        )

    def exitCall(self, ctx: coolParser.CallContext):
        r = ''
        for c in ctx.expression():
            r += self.stack.pop()
            r += asm.tpl_push_arg

        self.stack.append(
            asm.tpl_call.substitute(
                push_arguments=r,
                name=ctx.Variable()
            )
        )

    def exitReturn(self, ctx: coolParser.ReturnContext):
        ctx.code = self.stack.pop()
