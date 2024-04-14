def split_c_command(command):
    """
    This method is a helper method that splits the C_COMMAND
    into dest, comp, jump.
    """
    parsed_commend = command.split("=")
    second_half_to_parse = parsed_commend.pop()
    second_half = second_half_to_parse.split(";")
    parsed_commend += second_half
    return parsed_commend


def comp(mnemonic: str) -> str:
    comp_dict = {"0": "0101010", "1": "0111111", "-1": "0111010",
                 "D": "0001100", "A": "0110000", "!D": "0001101",
                 "!A": "0110001", "-D": "0001111", "-A": "0110011",
                 "D+1": "0011111", "A+1": "0110010", "D+A": "0000010",
                 "D-A": "0010011", "A-D": "0000111", "D&A": "0000000",
                 "D|A": "0010101", "M": "1110000", "!M": "1110001",
                 "-M": "1110011", "M+1": "1110111", "M-1": "1110010",
                 "D+M": "1000010", "D-M": "1010011", "M-D": "1000111",
                 "D&M": "1000000", "D|M": "1010101"}

    return comp_dict[mnemonic]

def remove_comments_and_empty_lines(lines):
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

# Example usage
input_lines = [
    "// This file is part of www.nand2tetris.org",
    "// and the book \"The Elements of Computing Systems\"",
    "// by Nisan and Schocken, MIT Press.",
    "// File name: projects/06/max/Max.asm",
    "",
    "// Computes R2 = max(R0, R1)  (R0,R1,R2 refer to RAM[0],RAM[1],RAM[2])",
    "   @R0"
]

output_lines = remove_comments_and_empty_lines(input_lines)
print(output_lines)



