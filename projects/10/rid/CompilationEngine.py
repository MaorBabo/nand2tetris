"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

import Constant
import JackTokenizer


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: "JackTokenizer", output_stream: typing.TextIO) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        self.jack_tokenizer = input_stream
        self.output_stream = output_stream

    def write_to_output(self, *excepted):
        if isinstance(excepted[0], str):
            if self.jack_tokenizer.get_token() == excepted[0]:
                self.output_stream.write(self.jack_tokenizer.get_token_xml() + "\n")
        if isinstance(excepted[0], list):
            if self.jack_tokenizer.get_token() in excepted[0]:
                self.output_stream.write(self.jack_tokenizer.get_token_xml() + "\n")
        if self.jack_tokenizer.has_more_tokens():
            self.jack_tokenizer.advance()

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self.output_stream.write("<class>\n")
        self.write_to_output("class")
        self.write_to_output(self.jack_tokenizer.get_token())
        self.write_to_output("{")
        if self.jack_tokenizer.get_token() in ["field", "static"]:
            self.compile_class_var_dec()
        while self.jack_tokenizer.get_token() in ["constructor", "function", "method"]:
            self.compile_subroutine()
        self.write_to_output("}")
        self.output_stream.write("</class>\n")

    # def compile_class_var_dec(self) -> None:
    #     """Compiles a static declaration or a field declaration."""
    #     while self.jack_tokenizer.get_token() in ["static", "field"]:
    #         self.output_stream.write("<classVarDec>\n")
    #
    #         self.write_to_output(["static", "field"])
    #         self.write_to_output(self.jack_tokenizer.get_token())  # type
    #         while self.jack_tokenizer.get_token() != ";":
    #             self.write_to_output(self.jack_tokenizer.get_token())  # var name
    #         self.write_to_output(";")
    #         self.output_stream.write("</classVarDec>\n")

    def compile_class_var_dec(self):
        """Compiles a static declaration or a field declaration.
        classVarDec: ('static' | 'field') type varName (',' varName)* ';'
        - type: 'int' | 'char' | 'boolean' | className
        """
        self.output_stream.write("<classVarDec>\n")
        self.write_to_output(self.jack_tokenizer.get_token())

        self.compile_type_and_varName()

        self.output_stream.write("</classVarDec>\n")

    def compile_type_and_varName(self):
        if self.jack_tokenizer.token_type() == "KEYWORD":
            self.write_to_output(self.jack_tokenizer.get_token())
        elif self.jack_tokenizer.token_type() == "IDENTIFIER":
            self.write_to_output(self.jack_tokenizer.get_token())
        self.write_to_output(self.jack_tokenizer.get_token())
        while self.jack_tokenizer.symbol() == ",":
            self.write_to_output(self.jack_tokenizer.get_token())
            self.write_to_output(self.jack_tokenizer.get_token())

        self.write_to_output(self.jack_tokenizer.get_token())

    def compile_subroutine(self) -> None:
        """Compiles a complete method, function, or constructor."""
        self.output_stream.write("<subroutineDec>\n")
        self.write_to_output(["constructor", "function", "method"])
        self.write_to_output(
            self.jack_tokenizer.get_token())  # return type can be classes so we don't know what word to expect
        self.write_to_output(self.jack_tokenizer.get_token())  # method name
        self.write_to_output("(")
        self.compile_parameter_list()
        self.write_to_output(")")
        self.output_stream.write("<subroutineBody>\n")
        self.write_to_output("{")
        while self.jack_tokenizer.get_token() not in Constant.STATEMENT_TYPES:
            self.compile_var_dec()
        self.compile_statements()
        self.write_to_output("}")
        self.output_stream.write("</subroutineBody>\n")
        self.output_stream.write("</subroutineDec>\n")

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        self.output_stream.write("<parameterList>\n")
        while self.jack_tokenizer.get_token() != ")":
            self.write_to_output(self.jack_tokenizer.get_token())  # type
            self.write_to_output(self.jack_tokenizer.get_token())  # var name
            if self.jack_tokenizer.get_token() != ")":
                self.write_to_output([","])
        self.output_stream.write("</parameterList>\n")

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self.output_stream.write("<varDec>\n")
        self.write_to_output(self.jack_tokenizer.get_token())  # type
        while self.jack_tokenizer.get_token() != ";":
            self.write_to_output(self.jack_tokenizer.get_token())  # var name
        self.write_to_output(";")
        self.output_stream.write("</varDec>\n")

    def compile_var_dec(self):
        """Compiles a var declaration."""
        self.output_stream.write("<varDec>\n")

        self.write_to_output(self.jack_tokenizer.get_token())

        self.compile_type_and_varName()


        self.output_stream.write("</varDec>\n")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        self.output_stream.write("<statements>\n")
        while self.jack_tokenizer.get_token() in Constant.STATEMENT_TYPES:
            if self.jack_tokenizer.get_token() == Constant.LET_STATEMENT:
                self.compile_let()
            elif self.jack_tokenizer.get_token() == Constant.IF_STATEMENT:
                self.compile_if()
            elif self.jack_tokenizer.get_token() == Constant.DO_STATEMENT:
                self.compile_do()
            elif self.jack_tokenizer.get_token() == Constant.WHILE_STATEMENT:
                self.compile_while()
            elif self.jack_tokenizer.get_token() == Constant.RETURN_STATEMENT:
                self.compile_return()
        self.output_stream.write("</statements>\n")

    def compile_do(self) -> None:
        """Compiles a do statement."""
        self.output_stream.write("<doStatement>\n")
        self.write_to_output("do")
        self.write_to_output(self.jack_tokenizer.get_token())
        #  when subroutine called is either x() or x.y()
        if self.jack_tokenizer.get_token() == ".":
            self.write_to_output(".")
            self.write_to_output(self.jack_tokenizer.get_token())
        self.write_to_output("(")
        self.compile_expression_list()
        self.write_to_output(")")
        self.write_to_output(";")
        self.output_stream.write("</doStatement>\n")

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.output_stream.write("<letStatement>\n")
        self.write_to_output("let")
        self.write_to_output(self.jack_tokenizer.get_token())  # var name
        if self.jack_tokenizer.get_token() == "[":
            self.write_to_output("[")
            self.compile_expression()
            self.write_to_output("]")
        self.write_to_output("=")
        self.compile_expression()
        self.write_to_output(";")
        self.output_stream.write("</letStatement>\n")

    def compile_while(self) -> None:
        """Compiles a while statement."""
        self.output_stream.write("<whileStatement>\n")
        self.write_to_output("while")
        self.write_to_output("(")
        self.compile_expression()
        self.write_to_output(")")
        self.write_to_output("{")
        self.compile_statements()
        self.write_to_output("}")
        self.output_stream.write("</whileStatement>\n")

    def compile_return(self) -> None:
        """Compiles a return statement."""
        self.output_stream.write("<returnStatement>\n")
        self.write_to_output("return")
        # to do expression?
        if self.jack_tokenizer.get_token() != ";":
            self.compile_expression()
        self.write_to_output(";")
        self.output_stream.write("</returnStatement>\n")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        self.output_stream.write("<ifStatement>\n")
        self.write_to_output("if")
        self.write_to_output("(")
        self.compile_expression()
        self.write_to_output(")")
        self.write_to_output("{")
        self.compile_statements()
        self.write_to_output("}")
        if self.jack_tokenizer.get_token() == "else":
            self.write_to_output("else")
            self.write_to_output("{")
            self.compile_statements()
            self.write_to_output("}")
        self.output_stream.write("</ifStatement>\n")

    def compile_expression(self) -> None:
        """Compiles an expression."""
        self.output_stream.write("<expression>\n")
        # if self.jack_tokenizer.get_token() in Constant.UNARY_OP:
        #     self.compile_term()
        #     self.output_stream.write("</expression>\n")
        #     return
        self.compile_term()
        # 5 - 7
        # -1
        while self.jack_tokenizer.get_token() not in [")", ";", ",", "]"]:
            # if any({self.jack_tokenizer.get_token() in Constant.TERMS_TOKENS,
            #         self.jack_tokenizer.token_type() in Constant.TERMS_TYPES}):
            #     self.compile_term()
            # else:
            #     # compile op
            #     self.process(self.jack_tokenizer.get_token())
            self.write_to_output(self.jack_tokenizer.get_token())
            self.compile_term()
        self.output_stream.write("</expression>\n")

    def compile_term(self) -> None:
        """Compiles a term. 
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        self.output_stream.write("<term>\n")
        if self.jack_tokenizer.get_token() == "(":  # expression
            self.write_to_output("(")
            self.compile_expression()
            self.write_to_output(")")
            self.output_stream.write("</term>\n")
            return
        if self.jack_tokenizer.get_token() in Constant.UNARY_OP:
            self.write_to_output(Constant.UNARY_OP)
            self.compile_term()
            self.output_stream.write("</term>\n")
            return
        self.write_to_output(self.jack_tokenizer.get_token())
        if self.jack_tokenizer.get_token() == "(":  # subroutine call a(expression_list)
            self.write_to_output("(")
            self.compile_expression_list()
            self.write_to_output(")")
        elif self.jack_tokenizer.get_token() == "[":  # picking on array val like a[expression]
            self.write_to_output("[")
            self.compile_expression()
            self.write_to_output("]")
        elif self.jack_tokenizer.get_token() == ".":  # subroutine call like a.b(expression_list)
            self.write_to_output(".")
            self.write_to_output(self.jack_tokenizer.get_token())  # class or var name
            self.write_to_output("(")
            self.compile_expression_list()
            self.write_to_output(")")
        self.output_stream.write("</term>\n")

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        self.output_stream.write("<expressionList>\n")
        if self.jack_tokenizer.get_token() != ")":
            self.compile_expression()
        while self.jack_tokenizer.get_token() != ")":
            self.write_to_output(",")
            self.compile_expression()
        self.output_stream.write("</expressionList>\n")
