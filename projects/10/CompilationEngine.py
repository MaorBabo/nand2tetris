"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""


OP_LIST = ["+", "-", "*", "/", "&", "|", "<", ">", "=", "&amp", "$lt", "$gt"]


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: "JackTokenizer", output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        self._indentation = 0
        self.input_stream = input_stream
        self.output_stream = output_stream

    def compile_class(self):
        """Compiles a complete class.
        class: 'class' className '{' classVarDec* subroutineDec* '}'
        - classVarDec: ('static' | 'field') type varName (',' varName)* ';'
        - type: 'int' | 'char' | 'boolean' | className
        - subroutineDec: ('constructor' | 'function' | 'method') ('void' | type)
        - subroutineName '(' parameterList ')' subroutineBody
        - parameterList: ((type varName) (',' type varName)*)?
        - subroutineBody: '{' varDec* statements '}'
        - varDec: 'var' type varName (',' varName)* ';'
        - className: identifier
        - subroutineName: identifier
        - varName: identifier
        """
        if self.input_stream.has_more_tokens():
            self.output_stream.write("<class>\n")
            self._indentation += 1

            self.write_keyword()

            self.input_stream.advance()
            self.write_identifier()

            self.input_stream.advance()
            self.write_symbol()

            self.input_stream.advance()
            while self.input_stream.keyword() == "static" or \
                    self.input_stream.keyword() == "field":
                self.compile_class_var_dec()
            while self.input_stream.keyword() == "constructor" or \
                    self.input_stream.keyword() == "function" \
                    or self.input_stream.keyword() == "method":
                self.compile_subroutine()

            self.write_symbol()

            self._indentation -= 1
            self.output_stream.write("</class>\n")



    def compile_class_var_dec(self):
        """Compiles a static declaration or a field declaration.
        classVarDec: ('static' | 'field') type varName (',' varName)* ';'
        - type: 'int' | 'char' | 'boolean' | className
        """
        self.output_stream.write("  " * self._indentation + "<classVarDec>\n")
        self._indentation += 1
        self.write_keyword()

        self.input_stream.advance()
        self.compile_type_and_varName()

        self._indentation -= 1
        self.output_stream.write("  " * self._indentation + "</classVarDec>\n")

    def compile_subroutine(self):
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        self.output_stream.write("  " * self._indentation + "<subroutineDec>\n")
        self._indentation += 1
        self.write_keyword()

        self.input_stream.advance()
        if self.input_stream.token_type() == "KEYWORD":
            self.write_keyword()
        elif self.input_stream.token_type() == "IDENTIFIER":
            self.write_identifier()

        self.input_stream.advance()
        self.write_identifier()

        self.input_stream.advance()
        self.write_symbol()

        self.input_stream.advance()
        self.compile_parameter_list()

        self.write_symbol()

        self.input_stream.advance()

        self.output_stream.write("  " * self._indentation + "<subroutineBody>\n")
        self._indentation += 1
        self.write_symbol()

        self.input_stream.advance()
        while self.input_stream.keyword() == "var":
            self.compile_var_dec()

        self.compile_statements()

        self.write_symbol()
        self._indentation -= 1
        self.output_stream.write("  " * self._indentation + "</subroutineBody>\n")
        self._indentation -= 1
        self.output_stream.write("  " * self._indentation + "</subroutineDec>\n")
        self.input_stream.advance()

    def compile_parameter_list(self):
        """Compiles a (possibly empty) parameter list, not including the
        enclosing "()".
        """
        self.output_stream.write("  " * self._indentation + "<parameterList>\n")
        self._indentation += 1
        while self.input_stream.token_type() != "SYMBOL":
            if self.input_stream.token_type() == "KEYWORD":
                self.write_keyword()
            elif self.input_stream.token_type() == "IDENTIFIER":
                self.write_identifier()
            self.input_stream.advance()
            self.write_identifier()
            self.input_stream.advance()
            if self.input_stream.symbol() == ",":
                self.write_symbol()
                self.input_stream.advance()

        self._indentation -= 1
        self.output_stream.write("  " * self._indentation + "</parameterList>\n")

    def compile_var_dec(self):
        """Compiles a var declaration."""
        self.output_stream.write("  " * self._indentation + "<varDec>\n")
        self._indentation += 1

        self.write_keyword()
        self.input_stream.advance()
        self.compile_type_and_varName()

        self._indentation -= 1
        self.output_stream.write("  " * self._indentation + "</varDec>\n")

    def compile_statements(self):
        """Compiles a sequence of statements, not including the enclosing
        "{}".
        """
        self.output_stream.write("  " * self._indentation + "<statements>\n")
        self._indentation += 1
        while self.input_stream.token_type() == "KEYWORD":
            if self.input_stream.keyword() == "let":
                self.compile_let()
            elif self.input_stream.keyword() == "if":
                self.compile_if()
            elif self.input_stream.keyword() == "while":
                self.compile_while()
            elif self.input_stream.keyword() == "do":
                self.compile_do()
            elif self.input_stream.keyword() == "return":
                self.compile_return()
        self._indentation -= 1
        self.output_stream.write("  " * self._indentation + "</statements>\n")

    def compile_do(self):
        """Compiles a do statement."""
        self.output_stream.write("  " * self._indentation + "<doStatement>\n")
        self._indentation += 1
        self.write_keyword()

        self.input_stream.advance()

        self.write_identifier()
        self.input_stream.advance()
        if self.input_stream.symbol() == ".":
            self.write_symbol()
            self.input_stream.advance()
            self.write_identifier()
            self.input_stream.advance()

        self.write_symbol()

        self.input_stream.advance()
        self.compile_expression_list()

        self.write_symbol()

        self.input_stream.advance()
        self.write_symbol()

        self._indentation -= 1
        self.output_stream.write("  " * self._indentation + "</doStatement>\n")
        self.input_stream.advance()

    def compile_let(self):
        """Compiles a let statement."""
        self.output_stream.write("  " * self._indentation + "<letStatement>\n")
        self._indentation += 1
        self.write_keyword()

        self.input_stream.advance()
        self.write_identifier()

        self.input_stream.advance()
        if self.input_stream.symbol() == "[":
            self.write_symbol()
            self.input_stream.advance()
            self.compile_expression()
            self.write_symbol()
            self.input_stream.advance()

        self.write_symbol()

        self.input_stream.advance()
        self.compile_expression()
        self.write_symbol()

        self._indentation -= 1
        self.output_stream.write("  " * self._indentation + "</letStatement>\n")
        self.input_stream.advance()

    def compile_while(self):
        """Compiles a while statement."""
        self.output_stream.write("  " * self._indentation + "<whileStatement>\n")
        self._indentation += 1
        self.write_keyword()

        self.input_stream.advance()
        self.write_symbol()

        self.input_stream.advance()
        self.compile_expression()

        self.write_symbol()

        self.input_stream.advance()
        self.write_symbol()

        self.input_stream.advance()
        self.compile_statements()

        self.write_symbol()

        self._indentation -= 1
        self.output_stream.write("  " * self._indentation + "</whileStatement>\n")
        self.input_stream.advance()

    def compile_return(self):
        """Compiles a return statement."""
        self.output_stream.write("  " * self._indentation + "<returnStatement>\n")
        self._indentation += 1
        self.write_keyword()
        self.input_stream.advance()

        if self.input_stream.symbol() != ";":
            self.compile_expression()

        self.write_symbol()
        self.input_stream.advance()

        self._indentation -= 1
        self.output_stream.write("  " * self._indentation + "</returnStatement>\n")

    def compile_if(self):
        """Compiles a if statement, possibly with a trailing else clause."""
        self.output_stream.write("  " * self._indentation + "<ifStatement>\n")
        self._indentation += 1
        self.write_keyword()

        self.input_stream.advance()
        self.write_symbol()

        self.input_stream.advance()
        self.compile_expression()

        self.write_symbol()

        self.input_stream.advance()
        self.write_symbol()

        self.input_stream.advance()
        self.compile_statements()

        self.write_symbol()

        self.input_stream.advance()
        if self.input_stream.token_type() == "KEYWORD" and \
                self.input_stream.keyword() == "else":
            self.write_keyword()

            self.input_stream.advance()
            self.write_symbol()

            self.input_stream.advance()
            self.compile_statements()

            self.write_symbol()
            self.input_stream.advance()

        self._indentation -= 1
        self.output_stream.write("  " * self._indentation + "</ifStatement>\n")

    def compile_expression(self):
        """Compiles an expression."""
        self.output_stream.write("  " * self._indentation + "<expression>\n")
        self._indentation += 1
        print(self.input_stream.current_line)
        self.compile_term()

        while self.input_stream.token_type() == "SYMBOL" and \
                self.input_stream.symbol() in OP_LIST:

            self.write_symbol()
            self.input_stream.advance()
            self.compile_term()

        self._indentation -= 1
        self.output_stream.write("  " * self._indentation + "</expression>\n")



    def compile_term(self):
        """Compiles a term.
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """


        sanity_check = True
        self.output_stream.write("  " * self._indentation + "<term>\n")
        self._indentation += 1
        if self.input_stream.token_type() == "INT_CONST":
            self.write_int_const()
        elif self.input_stream.token_type() == "STRING_CONST":
            self.write_str_const()
        elif self.input_stream.token_type() == "KEYWORD":
            self.write_keyword()
        elif self.input_stream.token_type() == "IDENTIFIER":
            self.write_identifier()

            self.input_stream.advance()
            sanity_check = False
            if self.input_stream.symbol() == "[":
                sanity_check = True
                self.write_symbol()
                self.input_stream.advance()
                self.compile_expression()
                self.write_symbol()
            elif self.input_stream.symbol() == ".":
                sanity_check = True
                self.write_symbol()
                self.input_stream.advance()
                self.write_identifier()
                self.input_stream.advance()
                self.write_symbol()
                self.input_stream.advance()
                self.compile_expression_list()
                self.write_symbol()
            elif self.input_stream.symbol() == "(":
                sanity_check = True
                self.write_symbol()
                self.input_stream.advance()
                self.compile_expression_list()
                self.write_symbol()

        elif self.input_stream.symbol() == "(":
            self.write_symbol()
            self.input_stream.advance()
            self.compile_expression()
            self.write_symbol()
        elif self.input_stream.symbol() == "~" or self.input_stream.symbol() == \
                "-":
            self.write_symbol()
            self.input_stream.advance()
            self.compile_term()
            sanity_check = False

        if sanity_check:
            self.input_stream.advance()

        self._indentation -= 1
        self.output_stream.write("  " * self._indentation + "</term>\n")
    # def compile_term(self) -> None:
    #     """Compiles a term.
    #     This routine is faced with a slight difficulty when
    #     trying to decide between some of the alternative parsing rules.
    #     Specifically, if the current token is an identifier, the routing must
    #     distinguish between a variable, an array entry, and a subroutine call.
    #     A single look-ahead token, which may be one of "[", "(", or "." suffices
    #     to distinguish between the three possibilities. Any other token is not
    #     part of this term and should not be advanced over.
    #     """
    #     self.output_stream.write("<term>\n")
    #     # write intVal:
    #     if self.input_stream.token_type() == "INT_CONST":
    #         self.write_int_const()
    #         self.input_stream.advance()
    #     # write stringVal:
    #     elif self.input_stream.token_type() == "STRING_CONST":
    #         self.write_str_const()
    #         self.input_stream.advance()
    #     # write keyword:
    #     elif self.input_stream.token_type() == "KEYWORD":
    #         self.write_keyword()
    #         self.input_stream.advance()
    #     # write unaryOp term:
    #     elif self.input_stream.symbol() in ['-', '~', '^', '#']:
    #         # '-', '~', '^', '#'
    #         self.write_symbol()
    #         self.input_stream.advance()
    #         # write term:
    #         self.compile_term()
    #     # write identifier:
    #     elif self.input_stream.token_type() == "IDENTIFIER":
    #         self.write_identifier()
    #         self.input_stream.advance()
    #         if self.input_stream.symbol() == "[":
    #             # write [:
    #             self.write_symbol()
    #             self.input_stream.advance()
    #             self.compile_expression()
    #             # write ]:
    #             self.write_symbol()
    #             self.input_stream.advance()
    #         elif self.input_stream.symbol() == ".":
    #             # write '.':
    #             self.write_symbol()
    #             self.input_stream.advance()
    #             # write subroutine:
    #             self.compile_subroutine()
    #         elif self.input_stream.symbol() == "(":
    #             # write (
    #             self.write_symbol()
    #             self.input_stream.advance()
    #             self.compile_expression_list()
    #             # write ):
    #             self.write_symbol()
    #             self.input_stream.advance()
    #     #  write expression
    #     elif self.input_stream.symbol() == "(":
    #         # write (:
    #         self.write_symbol()
    #         self.input_stream.advance()
    #         self.compile_expression()
    #         # write ):
    #         self.write_symbol()
    #         self.input_stream.advance()
    #     self.output_stream.write("</term>\n")

    def compile_expression_list(self):
        """Compiles a (possibly empty) comma-separated list of expressions."""
        self.output_stream.write("  " * self._indentation + "<expressionList>\n")
        self._indentation += 1

        if self.input_stream.token_type() != "SYMBOL" and \
                self.input_stream.symbol() != ")":
            self.compile_expression()
            while self.input_stream.token_type() == "SYMBOL" and \
                    self.input_stream.symbol() == ",":
                self.write_symbol()
                self.input_stream.advance()
                self.compile_expression()
        elif self.input_stream.symbol() == "(":
            self.compile_expression()
            while self.input_stream.token_type() == "SYMBOL" and \
                    self.input_stream.symbol() == ",":
                self.write_symbol()
                self.input_stream.advance()
                self.compile_expression()

        self._indentation -= 1
        self.output_stream.write("  " * self._indentation + "</expressionList>\n")

    def compile_type_and_varName(self):
        if self.input_stream.token_type() == "KEYWORD":
            self.write_keyword()
        elif self.input_stream.token_type() == "IDENTIFIER":
            self.write_identifier()
        self.input_stream.advance()
        self.write_identifier()
        self.input_stream.advance()
        while self.input_stream.symbol() == ",":
            self.write_symbol()
            self.input_stream.advance()
            self.write_identifier()
            self.input_stream.advance()
        self.write_symbol()
        self.input_stream.advance()

    def write_identifier(self):
        self.output_stream.write("  " * self._indentation + "<identifier> " +
                                 self.input_stream.identifier() + " </identifier>\n")

    def write_keyword(self):
        self.output_stream.write("  " * self._indentation + "<keyword> " +
                                 self.input_stream.keyword() + " </keyword>\n")

    def write_symbol(self):
        string_to_write = self.input_stream.symbol()
        if self.input_stream.symbol() == "<":
            string_to_write = "&lt;"
        elif self.input_stream.symbol() == ">":
            string_to_write = "&gt;"
        elif self.input_stream.symbol() == "&":
            string_to_write = "&amp;"
        self.output_stream.write("  " * self._indentation + "<symbol> " +
                                 string_to_write.strip('"') + " </symbol>\n")

    def write_int_const(self):
        self.output_stream.write("  " * self._indentation + "<integerConstant> " +
                                 self.input_stream.identifier() + " </integerConstant>\n")

    def write_str_const(self):
        self.output_stream.write("  " * self._indentation + "<stringConstant> " +
                                 self.input_stream.identifier().strip('"') + " </stringConstant>\n")
