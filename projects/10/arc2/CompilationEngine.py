
from os import stat
import typing
import re

op = re.compile(r"[+\-*/&|<>=]")
unary_op = re.compile(r'[-~^#]')
keyword_constant = re.compile(r'true|false|null|this')


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: "JackTokenizer",
                 output_stream: typing.TextIO) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        # Your code goes here!
        self.token_file = input_stream.read().splitlines()
        self.out = output_stream
        # self.written = True
        self.index = 1
        self.token = self.token_file[1].split(' ')

    def write_next_keyword(self, labels):
        if 'keyword' == self.token[0][1:-1] and self.token[1] in labels:
            self.out.write(" ".join(self.token) + '\n')
            if self.index < len(self.token_file):
                self.token = self.token_file[self.index].split(' ')
                self.index += 1

    def write_next_id(self):
        if self.token[1] == ',' or 'identifier' == self.token[0][1:-1]:
            self.out.write(" ".join(self.token) + '\n')
            if self.index < len(self.token_file):
                self.token = self.token_file[self.index].split(' ')
                self.index += 1
            self.write_next_id()

    def write_next_symbol(self, elem):
        if 'symbol' == self.token[0][1:-1] and elem == self.token[1]:
            self.out.write(" ".join(self.token) + '\n')
            if self.index < len(self.token_file):
                self.token = self.token_file[self.index].split(' ')
                self.index += 1

    def compile_class(self) -> None:
        """Compiles a complete class."""
        # Your code goes here!
        self.out.write(f"<class>\n")
        if self.index < len(self.token_file):
            self.token = self.token_file[self.index].split(' ')
            self.index += 1
        self.write_next_keyword(['class'])
        self.write_next_id()
        self.write_next_symbol('{')
        self.compile_class_var_dec()
        self.compile_subroutine()
        self.write_next_symbol('}')
        self.out.write(f"</class>\n")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        # Your code goes here!
        while self.token[1] in ['field', 'static']:
            self.out.write(f"<classVarDec>\n")
            self.write_next_keyword(['field', 'static'])
            self.write_next_keyword(['int', 'char', 'boolean'])
            self.write_next_id()  # varName (',' varName)*
            self.write_next_symbol(';')  # ;
            self.out.write(f"</classVarDec>\n")

    def compile_subroutine(self) -> None:
        """Compiles a complete method, function, or constructor."""
        # Your code goes here!

        if len(self.token) > 1 and self.token[1] in ['constructor', 'function', 'method']:
            self.out.write(f"<subroutineDec>\n")
            self.write_next_keyword(['constructor', 'function', 'method'])
            self.write_next_keyword(['void', 'int', 'char', 'boolean'])
            self.write_next_id()
            self.write_next_symbol('(')
            self.out.write(f"<parameterList>\n")
            self.compile_parameter_list()
            self.out.write(f"</parameterList>\n")
            self.write_next_symbol(')')
            # subroutine body
            self.out.write(f"<subroutineBody>\n")
            self.write_next_symbol('{')
            self.compile_var_dec()
            self.out.write(f"<statements>\n")
            self.compile_statements()
            self.out.write(f"</statements>\n")
            self.write_next_symbol('}')
            self.out.write(f"</subroutineBody>\n")
            self.out.write(f"</subroutineDec>\n")
            self.compile_subroutine()

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the
        enclosing "()".
        """
        # Your code goes here!
        if self.token[1] == ',' or self.token[1] in ['int', 'char', 'boolean'] or "identifier" == self.token[0][1:-1]:
            self.write_next_keyword(['int', 'char', 'boolean'])
            self.write_next_id()
            self.compile_parameter_list()

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        # Your code goes here!
        if self.token[1] == 'var':
            self.out.write(f"<varDec>\n")
            self.write_next_keyword(['var'])
            self.write_next_keyword(['int', 'char', 'boolean'])
            self.write_next_id()
            self.write_next_symbol(';')
            self.out.write(f"</varDec>\n")
            self.compile_var_dec()

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing
        "{}".
        """
        # Your code goes here!

        statements = {'let': self.compile_let, 'if': self.compile_if,
                      'while': self.compile_while, 'do': self.compile_do,
                      'return': self.compile_return}

        if len(self.token) > 1 and self.token[1] in statements.keys():
            statements[self.token[1]]()
            self.compile_statements()

    def compile_do(self) -> None:
        """Compiles a do statement."""
        # Your code goes here!
        self.out.write(f"<doStatement>\n")
        self.write_next_keyword(['do'])
        self.write_identifier()
        self.write_next_symbol(';')
        self.out.write(f"</doStatement>\n")

    def write_identifier(self):
        next_token = self.token_file[self.index].split(' ')
        if next_token[1] == '(':
            self.write_next_id()  # subroutine name
            self.write_next_symbol('(')
            self.out.write(f"<expressionList>\n")
            self.compile_expression_list()
            self.out.write(f"</expressionList>\n")
            self.write_next_symbol(')')
        elif next_token[1] == '.':
            self.write_next_id()  # className|varName
            self.write_next_symbol('.')
            self.write_next_id()
            self.write_next_symbol('(')
            self.out.write(f"<expressionList>\n")
            self.compile_expression_list()
            self.out.write(f"</expressionList>\n")
            self.write_next_symbol(')')
        elif next_token[1] == '[':
            self.write_next_id()
            self.write_next_symbol('[')
            self.out.write(f"<expression>\n")
            self.compile_expression()
            self.out.write(f"</expression>\n")
            self.write_next_symbol(']')
        else:
            if self.token[0][1:-1] == 'identifier':
                self.out.write(" ".join(self.token) + '\n')
                if self.index < len(self.token_file):
                    self.token = self.token_file[self.index].split(' ')
                    self.index += 1

    def compile_let(self) -> None:
        """Compiles a let statement."""
        # letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
        # Your code goes here!
        self.out.write(f"<letStatement>\n")
        self.write_next_keyword(['let'])
        self.write_next_id()
        if self.token[1] == '[':
            self.write_next_symbol('[')
            self.out.write(f"<expression>\n")
            self.compile_expression()
            self.out.write(f"</expression>\n")
            self.write_next_symbol(']')
        self.write_next_symbol('=')
        self.out.write(f"<expression>\n")
        self.compile_expression()
        self.out.write(f"</expression>\n")
        self.write_next_symbol(';')
        self.out.write(f"</letStatement>\n")

    def compile_while(self) -> None:
        """Compiles a while statement."""
        # Your code goes here!
        self.out.write(f"<whileStatement>\n")
        self.write_next_keyword(['while'])
        self.write_next_symbol('(')
        self.out.write(f"<expression>\n")
        self.compile_expression()
        self.out.write(f"</expression>\n")
        self.write_next_symbol(')')
        self.write_next_symbol('{')
        self.out.write(f"<statements>\n")
        self.compile_statements()
        self.out.write(f"</statements>\n")
        self.write_next_symbol('}')
        self.out.write(f"</whileStatement>\n")

    def compile_return(self) -> None:
        """Compiles a return statement."""
        # Your code goes here!
        self.out.write(f"<returnStatement>\n")
        self.write_next_keyword(['return'])
        if self.check_term():
            self.out.write(f"<expression>\n")
            self.compile_expression()
            self.out.write(f"</expression>\n")
        self.write_next_symbol(';')
        self.out.write(f"</returnStatement>\n")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # Your code goes here!
        self.out.write(f"<ifStatement>\n")
        self.write_next_keyword(['if'])
        self.write_next_symbol('(')
        self.out.write(f"<expression>\n")
        self.compile_expression()
        self.out.write(f"</expression>\n")
        self.write_next_symbol(')')
        self.write_next_symbol('{')
        self.out.write(f"<statements>\n")
        self.compile_statements()
        self.out.write(f"</statements>\n")
        self.write_next_symbol('}')
        if self.token[1] != 'else':
            self.out.write(f"</ifStatement>\n")
        else:
            self.write_next_keyword(['else'])
            self.write_next_symbol('{')
            self.out.write(f"<statements>\n")
            self.compile_statements()
            self.out.write(f"</statements>\n")
            self.write_next_symbol('}')
            self.out.write(f"</ifStatement>\n")

    # def compile_expression(self) -> None:
    #     """Compiles an expression."""
    #     # Your code goes here!
    #     self.out.write(f"<term>\n")
    #     self.compile_term()
    #     self.out.write(f"</term>\n")
    #     if op.match(self.token[1]):
    #         self.write_next_symbol(self.token[1])
    #         self.compile_expression()
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
        # Your code goes here!
        # print(self.token)
        if keyword_constant.match(self.token[1]) or self.token[0][1:-1] in ['integerConstant', 'stringConstant']:
            # print(self.token)
            self.out.write(" ".join(self.token) + '\n')
            if self.index < len(self.token_file):
                self.token = self.token_file[self.index].split(' ')
                self.index += 1
        elif '(' in self.token[1]:
            # print("FOUND2")
            self.write_next_symbol('(')
            self.out.write(f"<expression>\n")
            self.compile_expression()
            self.out.write(f"</expression>\n")
            self.write_next_symbol(')')
        elif unary_op.match(self.token[1]):
            # print("FOUND3")
            self.write_next_symbol(self.token[1])
            self.out.write(f"<term>\n")
            self.compile_term()
            self.out.write(f"</term>\n")
        elif self.token[0][1:-1] == 'identifier':

            self.write_identifier()

    def check_term(self):
        return keyword_constant.match(self.token[1]) or self.token[0][1:-1] in ['integerConstant', 'stringConstant'] \
               or '(' in self.token[1] or unary_op.match(self.token[1]) or self.token[0][1:-1] == 'identifier'

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!
        if self.check_term():
            self.out.write(f"<expression>\n")
            self.compile_expression()
            self.out.write(f"</expression>\n")
            if ',' in self.token[1]:
                self.write_next_symbol(',')
                self.compile_expression_list()
