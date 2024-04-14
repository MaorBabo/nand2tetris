"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import re
import os
import sys
import typing
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code


def decimal_to_binary_16bit(decimal_number):
    # Convert decimal to binary and remove the '0b' prefix
    binary_representation = bin(decimal_number)[2:]

    # Pad with zeros to make it a 16-bit binary representation
    binary_representation = binary_representation.zfill(16)

    return binary_representation


def remove_spaces_and_comments(line):
    # Remove spaces
    line_without_spaces = line.replace(" ", "")

    # Remove comments (everything after '//')
    line_without_comments = re.sub(r'//.*', '', line_without_spaces)

    return line_without_comments


def assemble_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    # Your code goes here!
    # A good place to start is to initialize a new Parser object:
    # parser = Parser(input_file)
    # Note that you can write to output_file like so:
    # output_file.write("Hello world! \n")

    # create parser object:
    parser = Parser(input_file)
    code = Code()
    symbol_table = SymbolTable()

    # first pass:
    label_row_num = 0
    while parser.has_more_commands():
        if parser.command_type() == "L_COMMAND":
            # add the symbol to the table:
            symbol_table.table[parser.symbol()] = label_row_num
        elif parser.command_type() == "A_COMMAND" or parser.command_type() == "C_COMMAND":
            label_row_num += 1

        # go to next instruction:
        parser.advance()

    # second pass:
    # go to start of input file:
    parser.current_command_index = 0
    parser.current_command = parser.input_lines[0]
    binary_value = ""
    shift = False
    while parser.has_more_commands():

        if parser.command_type() == "Comment":
            parser.advance()
            continue
        # get next instruction and parse it
        if parser.command_type() == "A_COMMAND":
            # adds the symbol to the table if needed:

            if not symbol_table.contains(parser.symbol()) and not parser.symbol().isnumeric():
                symbol_table.table[parser.symbol()] = symbol_table.symbol_index
                symbol_table.symbol_index += 1

            # convert to binary:
            if parser.symbol().isnumeric():
                binary_value = decimal_to_binary_16bit(int(parser.symbol()))
            else:
                binary_value = decimal_to_binary_16bit(symbol_table.table[parser.symbol()])

        elif parser.command_type() == "C_COMMAND":
            # parse dest, comp and jump to its strings:
            dest = parser.dest()
            comp = parser.comp()
            jump = parser.jump()

            if comp in {"A<<", "D<<", "M<<", "A>>", "D>>", "M>>"}:
                shift = True
            # translate to binary value:

            dest = code.dest(dest)
            comp = code.comp(comp)
            jump = code.jump(jump)

            # combining to 16 bit binary string:

            if shift:
                shift = False
                binary_value = "101" + comp + dest + jump
            else:
                binary_value = "111" + comp + dest + jump


        else:
            parser.advance()
            continue

        # writing the binary command to output file:
        output_file.write(binary_value + "\n")
        parser.advance()


if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)
