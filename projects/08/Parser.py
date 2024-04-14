"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import re
import io


class Parser:
    """
    # Parser

    Handles the parsing of a single .vm file, and encapsulates access to the
    input code. It reads VM commands, parses them, and provides convenient
    access to their components.
    In addition, it removes all white space and comments.

    ## VM Language Specification

    A .vm file is a stream of characters. If the file represents a
    valid program, it can be translated into a stream of valid assembly
    commands. VM commands may be separated by an arbitrary number of whitespace
    characters and comments, which are ignored. Comments begin with "//" and
    last until the lines end.
    The different parts of each VM command may also be separated by an arbitrary
    number of non-newline whitespace characters.

    - Arithmetic commands:
      - add, sub, and, or, eq, gt, lt
      - neg, not, shiftleft, shiftright
    - Memory segment manipulation:
      - push <segment> <number>
      - pop <segment that is not constant> <number>
      - <segment> can be any of: argument, local, static, constant, this, that,
                                 pointer, temp
    - Branching (only relevant for project 8):
      - label <label-name>
      - if-goto <label-name>
      - goto <label-name>
      - <label-name> can be any combination of non-whitespace characters.
    - Functions (only relevant for project 8):
      - call <function-name> <n-args>
      - function <function-name> <n-vars>
      - return
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Gets ready to parse the input file.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        self._input_lines = input_file.read().splitlines()
        modified_lines = []
        for line in self._input_lines:
            if self._input_lines is not None:
                line = self.remove_spaces_comments(line)
                if line != '':
                    modified_lines.append(line)
        self._current_index = 0
        self._current_command = modified_lines[0] if modified_lines else None
        self.lines = modified_lines
        self.splited_command = self._current_command.split()

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return self._current_index < len(self.lines)

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current
        command. Should be called only if has_more_commands() is true. Initially
        there is no current command.
        """
        self._current_index += 1
        if self.has_more_commands():
            self._current_command = self.lines[self._current_index]
            self.splited_command = self._current_command.split()

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current VM command.
            "C_ARITHMETIC" is returned for all arithmetic commands.
            For other commands, can return:
            "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
            "C_RETURN", "C_CALL".
        """
        art_set = {"add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"}
        self._current_command = self._current_command.strip()
        if self._current_command in art_set:
            return "C_ARITHMETIC"
        elif self._current_command[0:4] == "push":
            return "C_PUSH"
        elif self._current_command[0:3] == "pop":
            return "C_POP"
        elif self._current_command[0:5] == "label":
            return "C_LABEL"
        elif self._current_command[0:9] == "function ":
            return "C_FUNCTION"
        elif self._current_command[0:4] == "call":
            return "C_CALL"
        elif self._current_command[0:5] == "goto ":
            return "C_GOTO"
        elif self._current_command[0:2] == "if":
            return "C_IF"
        elif self._current_command == "return":
            return "C_RETURN"

    def arg1(self) -> str:
        """
        Returns:
            str: the first argument of the current command. In case of
            "C_ARITHMETIC", the command itself (add, sub, etc.) is returned.
            Should not be called if the current command is "C_RETURN".
        """
        if self.command_type() == "C_ARITHMETIC":
            return self._current_command
        elif self.command_type() == "C_PUSH":
            return self.splited_command[1]
        elif self.command_type() == "C_POP":
            return self.splited_command[1]
        elif self.command_type() == "C_LABEL":
            return self.splited_command[1]
        elif self.command_type() == "C_FUNCTION":
            return self.splited_command[1]
        elif self.command_type() == "C_CALL":
            return self.splited_command[1]
        elif self.command_type() == "C_GOTO":
            return self.splited_command[1]
        elif self.command_type() == "C_IF":
            return self.splited_command[1]
        elif self.command_type() == "C_RETURN":
            return self.splited_command[1]
    def arg2(self) -> int:
        """
        Returns:
            int: the second argument of the current command. Should be
            called only if the current command is "C_PUSH", "C_POP",
            "C_FUNCTION" or "C_CALL".
        """
        if self.command_type() == "C_PUSH" or self.command_type() == "C_POP" or self.command_type() == "C_FUNCTION" or self.command_type() == "C_CALL":
            return int(self.splited_command[2])


    def remove_spaces_comments(self, line):
        # Remove comments (everything after '//')
        line_without_comments = re.sub(r'//.*', '', line)

        # Remove spaces only from the start of a line
        line_without_spaces = line_without_comments.lstrip()

        return line_without_spaces