"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import re


class Parser:
    """Encapsulates access to the input code. Reads an assembly program
    by reading each command line-by-line, parses the current command,
    and provides convenient access to the commands components (fields
    and symbols). In addition, removes all white space and comments.
    """

    # represent an empty line:
    EMPTY_LINE = ''
    COMMENT = '/'
    A_COMMAND_PREFIX = "@"
    L_COMMAND_PREFIX = "("

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:

        # read all lines in input_file:
        self.input_lines = input_file.read().splitlines()
        self.input_lines = self.remove_comments_and_empty_lines(self.input_lines)

        # this is an index that represent the index of the current command:
        self.current_command_index = 0

        # represent the current command needed to be converted:
        self.current_command = self.input_lines[0]

        # a flag that tells if jump needed or not:
        self.is_jump = False
        self.is_dest = False


    def remove_comments_and_empty_lines(self, lines):
        lines_without_comments_and_empty = []

        for line in lines:
            # Remove the comment part of the line
            if '//' in line:
                line = line[:line.index('//')]

            # Remove leading and trailing whitespaces
            line = line.strip()

            # Only add non-empty lines to the result
            if line:
                lines_without_comments_and_empty.append(line)

        return lines_without_comments_and_empty

    def remove_spaces_and_comments(self, line):
        # Remove spaces
        line_without_spaces = line.replace(" ", "")

        # Remove comments (everything after '//')
        line_without_comments = re.sub(r'//.*', '', line_without_spaces)

        return line_without_comments

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """

        return self.current_command_index < len(self.input_lines)

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        self.current_command_index += 1
        if self.has_more_commands():

            self.current_command = self.input_lines[self.current_command_index]


        return

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        self.current_command = self.remove_spaces_and_comments(self.current_command)
        if self.current_command == self.EMPTY_LINE:
            return "Comment"

        elif self.current_command[0] == self.A_COMMAND_PREFIX:
            return "A_COMMAND"

        elif self.current_command[0] == self.L_COMMAND_PREFIX:
            return "L_COMMAND"

        elif self.current_command[0] == "/":
            return "Comment"

        else:
            return "C_COMMAND"

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """
        if self.command_type() == "A_COMMAND":
            return self.current_command[1:]
        elif self.command_type() == "L_COMMAND":
            return self.current_command[1: -1]

    def split_c_command(self) -> typing.List[str]:
        """
        This method is a helper method that splits the C_COMMAND
        into dest, comp, jump.
        """
        if "=" in self.current_command:
            parsed_commend = self.current_command.split("=")
            self.is_jump = False
            self.is_dest = True


        elif ";" in self.current_command:
            parsed_commend = self.current_command.split(";")
            self.is_jump = True
            self.is_dest = False
        return parsed_commend

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """

        self.current_command = self.remove_spaces_and_comments(self.current_command)
        command_part_list = self.split_c_command()
        if self.command_type() == "C_COMMAND" and self.is_dest:
            return command_part_list[0]

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        self.current_command = self.remove_spaces_and_comments(self.current_command)
        command_part_list = self.split_c_command()
        if self.command_type() == "C_COMMAND" and not self.is_jump:
            return command_part_list[1]
        elif not self.is_dest and self.is_jump:
            return command_part_list[0]

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        self.current_command = self.remove_spaces_and_comments(self.current_command)
        command_part_list = self.split_c_command()
        if self.command_type() == "C_COMMAND" and self.is_jump:
            return command_part_list[1]
