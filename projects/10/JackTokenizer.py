"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import re


class JackTokenizer:
    """Removes all comments from the input stream and breaks it
    into Jack language tokens, as specified by the Jack grammar.

    # Jack Language Grammar

    A Jack file is a stream of characters. If the file represents a
    valid program, it can be tokenized into a stream of valid tokens. The
    tokens may be separated by an arbitrary number of whitespace characters,
    and comments, which are ignored. There are three possible comment formats:
    /* comment until closing */ , /** API comment until closing */ , and
    // comment until the line’s end.

    - ‘xxx’: quotes are used for tokens that appear verbatim (‘terminals’).
    - xxx: regular typeface is used for names of language constructs
           (‘non-terminals’).
    - (): parentheses are used for grouping of language constructs.
    - x | y: indicates that either x or y can appear.
    - x?: indicates that x appears 0 or 1 times.
    - x*: indicates that x appears 0 or more times.

    ## Lexical Elements

    The Jack language includes five types of terminal elements (tokens).

    - keyword: 'class' | 'constructor' | 'function' | 'method' | 'field' |
               'static' | 'var' | 'int' | 'char' | 'boolean' | 'void' | 'true' |
               'false' | 'null' | 'this' | 'let' | 'do' | 'if' | 'else' |
               'while' | 'return'
    - symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' |
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
    - integerConstant: A decimal number in the range 0-32767.
    - StringConstant: '"' A sequence of Unicode characters not including
                      double quote or newline '"'
    - identifier: A sequence of letters, digits, and underscore ('_') not
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.

    ## Program Structure

    A Jack program is a collection of classes, each appearing in a separate
    file. A compilation unit is a single class. A class is a sequence of tokens
    structured according to the following context free syntax:

    - class: 'class' className '{' classVarDec* subroutineDec* '}'
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

    ## Statements

    - statements: statement*
    - statement: letStatement | ifStatement | whileStatement | doStatement |
                 returnStatement
    - letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
    - ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{'
                   statements '}')?
    - whileStatement: 'while' '(' 'expression' ')' '{' statements '}'
    - doStatement: 'do' subroutineCall ';'
    - returnStatement: 'return' expression? ';'

    ## Expressions

    - expression: term (op term)*
    - term: integerConstant | stringConstant | keywordConstant | varName |
            varName '['expression']' | subroutineCall | '(' expression ')' |
            unaryOp term
    - subroutineCall: subroutineName '(' expressionList ')' | (className |
                      varName) '.' subroutineName '(' expressionList ')'
    - expressionList: (expression (',' expression)* )?
    - op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
    - unaryOp: '-' | '~' | '^' | '#'
    - keywordConstant: 'true' | 'false' | 'null' | 'this'

    Note that ^, # correspond to shiftleft and shiftright, respectively.
    """

    def __init__(self, input_stream: typing.TextIO) -> None:
        """Opens the input stream and gets ready to tokenize it.

        Args:
            input_stream (typing.TextIO): input stream.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        input_lines = input_stream.read().splitlines()

        # remove all kinds of comments:
        self.pure_input_lines = []
        for line in input_lines:
            line = self.remove_spaces_comments(line)
            line = line.replace("(", ' ( ')
            line = line.replace(")", ' ) ')
            line = line.replace("[", " [ ")
            line = line.replace("]", " ] ")
            line = line.replace("{", ' { ')
            line = line.replace("}", ' } ')
            line = line.replace(";", " ; ")
            line = line.replace(",", " , ")
            line = line.replace(".", " . ")
            line = line.replace("-", " - ")
            line = line.replace("~", " ~ ")
            if line != '':
                self.pure_input_lines.append(line)

        self.token_index = 0
        self.line_index = 0
        self.current_token = None
        self.current_line = self.pure_input_lines[self.line_index]
        while self.current_line == "":
            self.line_index += 1
            self.current_line = self.pure_input_lines[self.line_index]

        if self.current_line[0] != '"':
            self.tokens = self.current_line.split()
        else:
            self.tokens = [self.current_line]
        if self.tokens:
            self.current_token = self.tokens[self.token_index]


    def has_more_tokens(self) -> bool:
        """Do we have more tokens in the input?

        Returns:
            bool: True if there are more tokens, False otherwise.
        """
        return self.line_index < len(self.pure_input_lines)

    def advance(self) -> None:
        """Gets the next token from the input and makes it the current token.
        This method should be called if has_more_tokens() is true.
        Initially there is no current token.
        """
        if self.has_more_tokens():
            # If we have reached the end of the current line
            if self.token_index >= len(self.tokens) - 1:
                # Move to the next line if available
                if self.line_index < len(self.pure_input_lines) - 1:
                    self.line_index += 1
                    self.current_line = self.pure_input_lines[self.line_index]

                    self.tokens = self.custom_split(self.current_line)

                    self.token_index = 0  # Reset token index
                    self.current_token = self.tokens[self.token_index]
                else:
                    # No more lines, set current token to None
                    self.current_token = None
            else:
                # Move to the next token in the current line
                self.token_index += 1
                self.current_token = self.tokens[self.token_index]
        else:
            # No more tokens
            self.current_token = None

    def token_type(self) -> str:
        """
        Returns:
            str: the type of the current token, can be
            "KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"
        """
        keyword_set = {'class', 'constructor', 'function', 'method', 'field', 'static',
                       'var', 'int', 'char', 'boolean', 'void', 'true', 'false',
                       'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return'}
        symbol_set = {'{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/',
                      '&', '|', '<', '>', '=', '~', "&amp", "&lt", "&gt"}

        # handling keyword:
        if self.current_token in keyword_set:
            return "KEYWORD"
        # handling symbol:
        if self.current_token in symbol_set:
            return "SYMBOL"
        # handling int:
        if self.current_token.isdigit():
            if 0 <= int(self.current_token) <= 32767:
                return "INT_CONST"

        # handling string:
        if self.current_token[0] == '"':
            return "STRING_CONST"

        # handling identifier:
        if self.current_token.isidentifier():
            return "IDENTIFIER"

    def keyword(self) -> str:
        """
        Returns:
            str: the keyword which is the current token.
            Should be called only when token_type() is "KEYWORD".
            Can return "CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT",
            "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET", "DO",
            "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE", "NULL", "THIS"
        """
        # key_map = {"class": "CLASS", "method": "METHOD", "function": "FUNCTION",
        #            "constructor": "CONSTRUCTOR", "int": "INT", "boolean": "BOOLEAN",
        #            "char": "CHAR", "void": "VOID", "var": "VAR", "static": "STATIC",
        #            "field": "FIELD", "let": "LET", "do": "DO", "if": "IF", "else": "ELSE",
        #            "while": "WHILE", "return": "RETURN", "true": "TRUE", "false": "FALSE",
        #            "null": "NULL", "this": "THIS"}
        # if self.current_token in key_map:
        #     return key_map[self.current_token]
        return self.current_token

    def symbol(self) -> str:
        """
        Returns:
            str: the character which is the current token.
            Should be called only when token_type() is "SYMBOL".
            Recall that symbol was defined in the grammar like so:
            symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' |
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
        """
        return self.current_token

    def identifier(self) -> str:
        """
        Returns:
            str: the identifier which is the current token.
            Should be called only when token_type() is "IDENTIFIER".
            Recall that identifiers were defined in the grammar like so:
            identifier: A sequence of letters, digits, and underscore ('_') not
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.
        """
        return self.current_token

    def int_val(self) -> int:
        """
        Returns:
            str: the integer value of the current token.
            Should be called only when token_type() is "INT_CONST".

            Recall that integerConstant was defined in the grammar like so:
            integerConstant: A decimal number in the range 0-32767.
        """
        return int(self.current_token)

    def string_val(self) -> str:
        """
        Returns:
            str: the string value of the current token, without the double
            quotes. Should be called only when token_type() is "STRING_CONST".
            Recall that StringConstant was defined in the grammar like so:
            StringConstant: '"' A sequence of Unicode characters not including
                      double quote or newline '"'
        """
        return self.current_token

    def remove_spaces_comments(self, line):
        # Remove single-line comments (everything after '//')
        line_without_single_comments = re.sub(r'//.*', '', line)

        # Remove multiline comments with asterisks (/* ... */ or /** ... */)
        line_without_multiline_comments = re.sub(r'/\*\*?([^*]|(\*+([^*/])))*\*+/', '', line_without_single_comments)

        # Remove spaces only from the start of a line
        line_without_spaces = line_without_multiline_comments.lstrip()

        if len(line_without_spaces) > 0:
            if line_without_spaces[0] == "*" or line_without_spaces[0] == "/":
                return ""

        return line_without_spaces

    def custom_split(self, line):
        # Split by white space outside of double quotes
        parts = re.findall(r'[^"\s]+|"[^"]*"', line)
        # Remove double quotes from the parts
        # parts = [part.strip('"') for part in parts]
        return parts
