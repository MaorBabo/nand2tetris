"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import Constant
import shlex


class JackTokenizer:
    """Removes all comments from the input stream and breaks it
    into Jack language tokens, as specified by the Jack grammar.
    """

    def __init__(self, input_stream: typing.TextIO) -> None:
        """Opens the input stream and gets ready to tokenize it.

        Args:
            input_stream (typing.TextIO): input stream.
        """
        input_lines = input_stream.read().splitlines()
        JackTokenizer.clean_multiline_comment_and_doc(input_lines)
        JackTokenizer.clean_comment(input_lines)
        self.words = []
        self.tokens = []
        for line in input_lines:
            self.separate_word(line)
        for line in self.words:
            self.separate_token(line)
        self.current_token = ''
        self.tokens_counter = 0
        self.tokens_len = len(self.tokens)

    def get_token(self):
        return self.current_token

    def get_next_token(self):
        if self.tokens_len > self.tokens_counter +1:
            self.current_token = self.tokens[self.tokens_counter+1]
        else:
            return "No more tokens"

    def get_token_xml(self):
        if self.token_type() == Constant.TOKEN_SYMBOL:
            return self.symbol()
        if self.token_type() == Constant.TOKEN_KEYWORD:
            return self.keyword()
        if self.token_type() == Constant.TOKEN_IDENTIFIER:
            return self.identifier()
        if self.token_type() == Constant.TOKEN_INT_CONST:
            return self.int_val()
        if self.token_type() == Constant.TOKEN_STRING_CONST:
            return self.string_val()

    def has_more_tokens(self) -> bool:
        """Do we have more tokens in the input?

        Returns:
            bool: True if there are more tokens, False otherwise.
        """
        return self.tokens_len > self.tokens_counter

    def advance(self) -> None:
        """Gets the next token from the input and makes it the current token. 
        This method should be called if has_more_tokens() is true. 
        Initially there is no current token.
        """
        if self.has_more_tokens():
            self.current_token = self.tokens[self.tokens_counter]
            self.tokens_counter += 1
        else:
            raise ValueError(Constant.ERROR_NO_MORE_COMMAND)

    def token_type(self) -> str:
        """
        Returns:
            str: the type of the current token, can be
            "KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"
        """
        if self.current_token in Constant.TOKEN_TYPE_DICT:
            return Constant.TOKEN_TYPE_DICT[self.current_token]
        elif self.current_token.isdecimal():
            if Constant.INT_CONST_MAX_VAL >= int(self.current_token) >= Constant.INT_CONST_MIN_VAL:
                return Constant.TOKEN_INT_CONST
            else:
                raise ValueError(Constant.ERROR_UNKNOWN_TOKEN.format(self.current_token))
        elif self.current_token[0] == Constant.QUOTATION_MARK and self.current_token[-1] == Constant.QUOTATION_MARK:
            return Constant.TOKEN_STRING_CONST
        elif not self.current_token[0].isdigit() and self.current_token.replace(Constant.UNDERSCORE, "").isalnum():
            return Constant.TOKEN_IDENTIFIER
        else:
            raise ValueError(Constant.ERROR_UNKNOWN_TOKEN.format(self.current_token))

    def keyword(self) -> str:
        """
        Returns:
            str: the keyword which is the current token.
            Should be called only when token_type() is "KEYWORD".
            Can return "CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT", 
            "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET", "DO", 
            "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE", "NULL", "THIS"
        """
        if self.token_type() == Constant.TOKEN_KEYWORD:
            return "<keyword>" + " " + self.current_token + " " + "</keyword>"
        raise ValueError(Constant.WRONG_CALL.format("keyword", self.token_type()))

    def symbol(self) -> str:
        """
        Returns:
            str: the character which is the current token.
            Should be called only when token_type() is "SYMBOL".
        """
        if self.token_type() in Constant.TOKEN_SYMBOL:
            if self.current_token in Constant.PROBLEMATIC_SYMBOLS_EXCHANGE:
                self.current_token = Constant.PROBLEMATIC_SYMBOLS_EXCHANGE[self.current_token]
            return "<symbol>" + " " + self.current_token + " " + "</symbol>"
        raise ValueError(Constant.WRONG_CALL.format("symbol", self.token_type()))

    def identifier(self) -> str:
        """
        Returns:
            str: the identifier which is the current token.
            Should be called only when token_type() is "IDENTIFIER".
        """
        if self.token_type() == Constant.TOKEN_IDENTIFIER:
            return "<identifier>" + " " + self.current_token + " " + "</identifier>"
        raise ValueError(Constant.WRONG_CALL.format("identifier", self.token_type()))

    def int_val(self) -> str:
        """
        Returns:
            str: the integer value of the current token.
            Should be called only when token_type() is "INT_CONST".
        """
        if self.token_type() == Constant.TOKEN_INT_CONST:
            return "<integerConstant>" + " " + self.current_token + " " + "</integerConstant>"
        raise ValueError(Constant.WRONG_CALL.format("int_val", self.token_type()))

    def string_val(self) -> str:
        """
        Returns:
            str: the string value of the current token, without the double 
            quotes. Should be called only when token_type() is "STRING_CONST".
        """
        if self.token_type() == Constant.TOKEN_STRING_CONST:
            return "<stringConstant>" + " " + self.current_token[1:-1] + " " + "</stringConstant>"  # removing the " "
        raise ValueError(Constant.WRONG_CALL.format("string_val", self.token_type()))

    def separate_word(self, line: str) -> None:
        if Constant.QUOTATION_MARK not in line:
            self.words += line.split()
            return
        substring_start = line.find(Constant.QUOTATION_MARK)
        substring_end = line.find(Constant.QUOTATION_MARK, substring_start+1)
        self.words += line[:substring_start].split() + [line[substring_start:substring_end+1]]
        self.separate_word(line[substring_end+1:])

    def separate_token(self, line: str) -> None:
        # if the line is Const string, than add it without separate
        if line[0] == Constant.QUOTATION_MARK or len(line) == 1:
            self.tokens += [line]
            return
        token_start = 0
        for i in range(len(line)):
            if line[i] in Constant.SYMBOLS_AND_SPACE:
                if [line[token_start:i]] != [Constant.SPACE] and [line[token_start:i]] != ['']:
                    self.tokens += [line[token_start:i]]
                if line[i] != [Constant.SPACE]:
                    self.tokens += [line[i]]
                token_start = i+1

        if line[token_start:] != '':
            self.tokens += [line[token_start:]]

    @staticmethod
    def check_in_substring(line: str, string: str, counter: int) -> typing.Tuple[bool, int]:
        """
        Check if the all the appearances of string are inside " " or  not.
        if it does return true, else return false
        """
        if line == '':
            return False, counter
        if Constant.QUOTATION_MARK not in line:
            return False, counter
        substring_start = line.find(Constant.QUOTATION_MARK)
        substring_end = line.find(Constant.QUOTATION_MARK, substring_start+1)
        string_start = line.find(string)
        if string_start < substring_start:
            return False, counter
        elif substring_start < string_start < substring_end:
            if string in line[substring_end+1:]:
                counter += JackTokenizer.count_occurrence(line[substring_start:substring_end], string)
                return JackTokenizer.check_in_substring(line[substring_end+1:], string, counter)
            return True, counter
        else:
            return JackTokenizer.check_in_substring(line[substring_end+1:], string, counter)

    @staticmethod
    def count_occurrence(line, string):
        start = line.find(string)
        counter = 0
        while start >= 0:
            start = line.find(string, start + len(string))
            counter += 1
        return counter

    @staticmethod
    def find_nth(line, string, n):
        start = line.find(string)
        while start >= 0 and n >= 1:
            start = line.find(string, start + len(string))
            n -= 1
        return start

    @staticmethod
    def clean_multiline_comment_and_doc(input_lines: typing.List[str]):
        """
        Clean multiline comment and doc from the program only if its not inside Const String
        """
        for i in range(len(input_lines)):
            if Constant.MULTILINE_COMMENT_START in input_lines[i]:
                in_substring, counter = JackTokenizer.check_in_substring(input_lines[i],
                                                                         Constant.MULTILINE_COMMENT_START, 0)
                while Constant.MULTILINE_COMMENT_START in input_lines[i] and not in_substring:
                        JackTokenizer.remove_multiline_comment(input_lines, i, counter)

            if Constant.DOCUMENTATION_START in input_lines[i]:
                in_substring, counter = JackTokenizer.check_in_substring(input_lines[i], Constant.DOCUMENTATION_START, 0)
                while Constant.DOCUMENTATION_START in input_lines[i] and not in_substring:
                    JackTokenizer.remove_doc(input_lines, i, counter)

    @staticmethod
    def remove_multiline_comment(input_lines: typing.List[str], i: int, occurrence: int) -> None:
        comment_index_start = JackTokenizer.find_nth(input_lines[i], Constant.MULTILINE_COMMENT_START, occurrence)
        if Constant.MULTILINE_COMMENT_OR_DOC_END in input_lines[i]:
            comment_index_end = input_lines[i].find(Constant.MULTILINE_COMMENT_OR_DOC_END)
            input_lines[i] = input_lines[i][0: comment_index_start] + input_lines[i][comment_index_end+2:]
            return
        input_lines[i] = input_lines[i][0: comment_index_start]
        for j in range(i+1, len(input_lines)):
            if Constant.MULTILINE_COMMENT_OR_DOC_END in input_lines[j]:
                comment_index_end = input_lines[j].find(Constant.MULTILINE_COMMENT_OR_DOC_END)
                input_lines[j] = input_lines[j][comment_index_end + 2:]
                return
            input_lines[j] = ''

    @staticmethod
    def remove_doc(input_lines: typing.List[str], i: int, occurrence: int) -> None:
        doc_index_start = JackTokenizer.find_nth(input_lines[i], Constant.DOCUMENTATION_START, occurrence)
        if Constant.MULTILINE_COMMENT_OR_DOC_END in input_lines[i]:
            doc_index_end = input_lines[i].find(Constant.MULTILINE_COMMENT_OR_DOC_END)
            input_lines[i] = input_lines[i][0: doc_index_start] + input_lines[i][doc_index_end+2:]
            return
        input_lines[i] = input_lines[i][0: doc_index_start]
        for j in range(i+1, len(input_lines)):
            if Constant.MULTILINE_COMMENT_OR_DOC_END in input_lines[j]:
                doc_index_end = input_lines[j].find(Constant.MULTILINE_COMMENT_OR_DOC_END)
                input_lines[j] = input_lines[j][doc_index_end + 2:]
                return
            input_lines[i] = ''

    @staticmethod
    def clean_comment(input_lines: typing.List[str]):
        """
        Clean comment from line only if it does not in const string
        """
        for i in range(len(input_lines)):
            if Constant.COMMENT in input_lines[i]:
                in_substring, counter = JackTokenizer.check_in_substring(input_lines[i], Constant.COMMENT, 0)
                if not in_substring:
                    comment_index = JackTokenizer.find_nth(input_lines[i], Constant.COMMENT, counter)
                    input_lines[i] = input_lines[i][0: comment_index]