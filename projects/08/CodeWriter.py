"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        # pass
        self._output_file = output_stream
        self._file_name = None
        self.jump = 10
        self.return_address_count = 0

    def bootstrap(self):
        stack_address = 256
        self._output_file.write("// bootstrap code\n")
        self._output_file.write(f"@{stack_address}\n")
        self._output_file.write("D=A\n")
        self._output_file.write("M=M+1\n")
        self._output_file.write("M=M-1\n")
        self._output_file.write("@SP\n")
        self._output_file.write("M=D\n")
        self._output_file.write("M=M\n")
        self.write_call("Sys.init", 0)

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        # This function is useful when translating code that handles the
        # static segment. For example, in order to prevent collisions between two
        # .vm files which push/pop to the static segment, one can use the current
        # file's name in the assembly variable's name and thus differentiate between
        # static variables belonging to different files.
        # To avoid problems with Linux/Windows/MacOS differences with regards
        # to filenames and paths, you are advised to parse the filename in
        # the function "translate_file" in Main.py using python's os library,
        # For example, using code similar to:
        # input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
        self._file_name = filename

    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """
        self.jump += 1
        arithmetic1 = {"add": "+", "sub": "-", "or": "|", "and": "&", "not": "!"}
        arithmetic2 = {"neg": "-"}
        arithmetic3 = {"eq": "==", "lt": "<", "gt": ">"}

        if command in arithmetic1:
            if command in ["and", "or"]:
                self._output_file.write(f"// {command}\n")
                self._output_file.write("@SP\n")
                self._output_file.write("M=M-1\n")
                self._output_file.write("A=M\n")
                self._output_file.write("D=M\n")
                self._output_file.write("@SP\n")
                self._output_file.write("M=M-1\n")
                self._output_file.write("A=M\n")
                self._output_file.write(f"M=D{arithmetic1[command]}M\n")
                self._output_file.write("@SP\n")
                self._output_file.write("M=M+1\n")

            elif command == "not":
                self._output_file.write(f"// {command}\n")
                self._output_file.write("@SP\n")
                self._output_file.write("AM=M-1\n")
                self._output_file.write(f"M={arithmetic1[command]}M\n")
                self._output_file.write("@SP\n")
                self._output_file.write("M=M+1\n")

            else:
                self._output_file.write(f"// {command}\n")
                self._output_file.write("@SP\n")
                self._output_file.write("AM=M-1\n")
                self._output_file.write("D=M\n")
                self._output_file.write("A=A-1\n")
                self._output_file.write(f"M=M{arithmetic1[command]}D\n")

        elif command in arithmetic2:
            self._output_file.write(f"// {command}\n")
            self._output_file.write("@SP\n")
            self._output_file.write("AM=M-1\n")
            self._output_file.write("M=-M\n")
            self._output_file.write("@SP\n")
            self._output_file.write("M=M+1\n")

        elif command in arithmetic3:
            self._output_file.write(f"// {command}\n")
            self._output_file.write("@SP\n")
            self._output_file.write("M=M-1\n")
            self._output_file.write("A=M\n")
            self._output_file.write("D=M\n")
            self._output_file.write("@SP\n")
            self._output_file.write("M=M-1\n")
            self._output_file.write("A=M\n")
            self._output_file.write("D=D-M\n")
            if command == "eq":
                self._output_file.write(f"@EQUAL{self.jump}\n"
                                        f"D;JEQ\n"
                                        f"@FALSE{self.jump}\n"
                                        f"0;JMP\n"
                                        f"(EQUAL{self.jump})\n"
                                        f"@SP\n"
                                        f"A=M\n"
                                        f"M=-1\n")
                self._output_file.write(f"@END{self.jump}\n"
                                        f"0;JMP\n")
                self._output_file.write(f"(FALSE{self.jump})\n"
                                        f"@SP\n"
                                        f"A=M\n"
                                        f"M=0\n")
                self._output_file.write(f"(END{self.jump})\n")
            if command == "lt":
                self._output_file.write(f"@IS_LESS{self.jump}\n"
                                        f"D;JGT\n"
                                        f"@FALSE{self.jump}\n"
                                        f"0;JMP\n"
                                        f"(IS_LESS{self.jump})\n"
                                        f"@SP\n"
                                        f"A=M\n"
                                        f"M=-1\n")
                self._output_file.write(f"@END{self.jump}\n"
                                        f"0;JMP\n")
                self._output_file.write(f"(FALSE{self.jump})\n"
                                        f"@SP\n"
                                        f"A=M\n"
                                        f"M=0\n")
                self._output_file.write(f"(END{self.jump})\n")

            if command == "gt":
                self._output_file.write(f"@IS_GREATER{self.jump}\n"
                                        f"D;JLT\n"
                                        f"@FALSE{self.jump}\n"
                                        f"0;JMP\n"
                                        f"(IS_GREATER{self.jump})\n"
                                        f"@SP\n"
                                        f"A=M\n"
                                        f"M=-1\n")
                self._output_file.write(f"@END{self.jump}\n"
                                        f"0;JMP\n")
                self._output_file.write(f"(FALSE{self.jump})\n"
                                        f"@SP\n"
                                        f"A=M\n"
                                        f"M=0\n")
                self._output_file.write(f"(END{self.jump})\n")
            self._output_file.write("@SP\n"
                                    "M=M+1\n")

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.

        if segment == "local":
            segment = "LCL"

            if command == "C_PUSH":
                self._output_file.write(f"// push local {index}\n")
                self._output_file.write("@LCL\n")
                self._output_file.write("M=M-1\n")
                self._output_file.write("M=M+1\n")
                self._output_file.write("D=M\n")
                self._output_file.write(f"@{index}\n")
                self._output_file.write("A=D+A\n")
                self._output_file.write("D=M\n")
                self._output_file.write("@SP\n")
                self._output_file.write("A=M\n")
                self._output_file.write("M=D\n")
                self._output_file.write("@SP\n")
                self._output_file.write("M=M-1\n")
                self._output_file.write("M=M+1\n")
                self._output_file.write("M=M+1\n")
            elif command == "C_POP":
                self._output_file.write(f"// pop local {index}\n")
                self._output_file.write(f"@{segment}\n")
                self._output_file.write("D=M\n")
                self._output_file.write(f"@{index}\n")
                self._output_file.write("D=D+A\n")
                self._output_file.write("@R15\n")
                self._output_file.write("M=M-1\n")
                self._output_file.write("M=M+1\n")
                self._output_file.write("M=D\n")
                self._output_file.write("@SP\n")
                self._output_file.write("AM=M-1\n")
                self._output_file.write("D=M\n")
                self._output_file.write("@R15\n")
                self._output_file.write("M=M-1\n")
                self._output_file.write("M=M+1\n")
                self._output_file.write("A=M\n")
                self._output_file.write("M=D\n")
        if segment == "argument":
            segment = "ARG"
            if command == "C_PUSH":
                self._output_file.write(f"// push argument {index}\n")
                self._output_file.write(f"@{segment}\n")
                self._output_file.write("D=M\n")
                self._output_file.write(f"@{index}\n")
                self._output_file.write("A=D+A\n")
                self._output_file.write("D=M\n")
                self._output_file.write("@SP\n")
                self._output_file.write("A=M\n")
                self._output_file.write("M=D\n")
                self._output_file.write("@SP\n")
                self._output_file.write("M=M+1\n")
            if command == "C_POP":
                self._output_file.write(f"// pop argument {index}\n")
                self._output_file.write(f"@{segment}\n")
                self._output_file.write("D=M\n")
                self._output_file.write(f"@{index}\n")
                self._output_file.write("D=D+A\n")
                self._output_file.write("@R15\n")
                self._output_file.write("M=D\n")
                self._output_file.write("@SP\n")
                self._output_file.write("AM=M-1\n")
                self._output_file.write("D=M\n")
                self._output_file.write("@R15\n")
                self._output_file.write("A=M\n")
                self._output_file.write("M=D\n")
        if segment == "constant":
            if command == "C_PUSH":
                self._output_file.write(f"// push constant {index}\n")
                self._output_file.write(f"@{index}\n")
                self._output_file.write("D=A\n")
                self._output_file.write("@SP\n")
                self._output_file.write("A=M\n")
                self._output_file.write("M=D\n")
                self._output_file.write("@SP\n")
                self._output_file.write("M=M+1\n")

        if segment == "static":
            static_address = self._file_name + "&" + str(index)

            if command == "C_PUSH":
                self._output_file.write(f"// push static {static_address}\n")
                self._output_file.write(f"@{static_address}\n")
                self._output_file.write("D=M\n")
                self._output_file.write("@SP\n")
                self._output_file.write("A=M\n")
                self._output_file.write("M=D\n")
                self._output_file.write("@SP\n")
                self._output_file.write("M=M+1\n")

            if command == "C_POP":
                self._output_file.write(f"// pop static {static_address}\n")
                self._output_file.write("@SP\n")
                self._output_file.write("M=M-1\n")
                self._output_file.write("A=M\n")
                self._output_file.write("D=M\n")
                self._output_file.write(f"@{static_address}\n")
                self._output_file.write("M=D\n")

        if segment == "this":
            segment = "THIS"
            if command == "C_PUSH":
                self._output_file.write(f"// push this {index}\n")
                self._output_file.write(f"@{segment}\n")
                self._output_file.write("D=M\n")
                self._output_file.write(f"@{index}\n")
                self._output_file.write("M=M-1\n")
                self._output_file.write("M=M+1\n")
                self._output_file.write("D=D+A\n")
                self._output_file.write("A=D\n")
                self._output_file.write("D=M\n")
                self._output_file.write("@SP\n")
                self._output_file.write("A=M\n")
                self._output_file.write("M=D\n")
                self._output_file.write("@SP\n")
                self._output_file.write("M=M+1\n")

            if command == "C_POP":
                self._output_file.write(f"// pop this {index}\n")
                self._output_file.write(f"@{segment}\n")
                self._output_file.write("D=M\n")
                self._output_file.write(f"@{index}\n")
                self._output_file.write("D=D+A\n")
                self._output_file.write("@R15\n")
                self._output_file.write("M=M-1\n")
                self._output_file.write("M=M+1\n")
                self._output_file.write("M=D\n")
                self._output_file.write("@SP\n")
                self._output_file.write("AM=M-1\n")
                self._output_file.write("D=M\n")
                self._output_file.write("@R15\n")
                self._output_file.write("A=M\n")
                self._output_file.write("M=D\n")

        if segment == "that":
            segment = "THAT"
            if command == "C_PUSH":
                self._output_file.write(f"// push that {index}\n")
                self._output_file.write(f"@{segment}\n")
                self._output_file.write("D=M\n")
                self._output_file.write(f"@{index}\n")
                self._output_file.write("D=D+A\n")
                self._output_file.write("A=D\n")
                self._output_file.write("D=M\n")
                self._output_file.write("@SP\n")
                self._output_file.write("A=M\n")
                self._output_file.write("M=D\n")
                self._output_file.write("@SP\n")
                self._output_file.write("M=M+1\n")
            if command == "C_POP":
                self._output_file.write(f"// pop that {index}\n")
                self._output_file.write(f"@{segment}\n")
                self._output_file.write("D=M\n")
                self._output_file.write(f"@{index}\n")
                self._output_file.write("D=D+A\n")
                self._output_file.write("@R15\n")
                self._output_file.write("M=D\n")
                self._output_file.write("@SP\n")
                self._output_file.write("AM=M-1\n")
                self._output_file.write("D=M\n")
                self._output_file.write("@R15\n")
                self._output_file.write("M=M-1\n")
                self._output_file.write("M=M+1\n")
                self._output_file.write("A=M\n")
                self._output_file.write("M=D\n")

        if segment == "pointer":
            if command == "C_PUSH":
                self._output_file.write(f"// push pointer {index}\n")
                self._output_file.write(f"@{index}\n")
                self._output_file.write("D=A\n")
                self._output_file.write(f"@{3}\n")
                self._output_file.write("M=M-1\n")
                self._output_file.write("M=M+1\n")
                self._output_file.write("A=D+A\n")
                self._output_file.write("D=M\n")
                self._output_file.write("@SP\n")
                self._output_file.write("M=M-1\n")
                self._output_file.write("M=M+1\n")
                self._output_file.write("A=M\n")
                self._output_file.write("M=D\n")
                self._output_file.write("@SP\n")
                self._output_file.write("M=M-1\n")
                self._output_file.write("M=M+1\n")
                self._output_file.write("M=M+1\n")

            if command == "C_POP":
                self._output_file.write(f"// pop pointer {index}\n")
                self._output_file.write("@SP\n")
                self._output_file.write("M=M-1\n")
                self._output_file.write("M=M+1\n")
                self._output_file.write("M=M-1\n")
                self._output_file.write("A=M\n")
                self._output_file.write("D=M\n")
                self._output_file.write(f"@{index + 3}\n")
                self._output_file.write("M=D\n")
        if segment == "temp":
            if command == "C_PUSH":
                self._output_file.write(f"// push temp {index}\n")
                self._output_file.write(f"@{5}\n")
                self._output_file.write("M=M-1\n")
                self._output_file.write("M=M+1\n")
                self._output_file.write("D=A\n")
                self._output_file.write(f"@{index}\n")
                self._output_file.write("A=D+A\n")
                self._output_file.write("D=M\n")
                self._output_file.write("@SP\n")
                self._output_file.write("M=M-1\n")
                self._output_file.write("M=M+1\n")
                self._output_file.write("A=M\n")
                self._output_file.write("M=D\n")
                self._output_file.write("@SP\n")
                self._output_file.write("M=M-1\n")
                self._output_file.write("M=M+1\n")
                self._output_file.write("M=M+1\n")

            if command == "C_POP":
                self._output_file.write(f"// pop temp {index}\n")
                self._output_file.write(f"@{5}\n")
                self._output_file.write("D=A\n")
                self._output_file.write(f"@{index}\n")
                self._output_file.write("D=D+A\n")
                self._output_file.write("@R15\n")
                self._output_file.write("M=M-1\n")
                self._output_file.write("M=M+1\n")
                self._output_file.write("M=D\n")
                self._output_file.write("@SP\n")
                self._output_file.write("AM=M-1\n")
                self._output_file.write("D=M\n")
                self._output_file.write("@R15\n")
                self._output_file.write("M=M-1\n")
                self._output_file.write("M=M+1\n")
                self._output_file.write("A=M\n")
                self._output_file.write("M=D\n")

    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command.
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        self._output_file.write("// label command:\n")
        self._output_file.write(f"({self._file_name}&{label})\n") # make the label unique per file.

    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        self._output_file.write("// goto command:\n")
        self._output_file.write(f"@{self._file_name}&{label}\n")
        self._output_file.write("0;JMP\n")

    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        self._output_file.write("// if-goto command:\n")
        self._output_file.write("@SP\n")
        self._output_file.write("AM=M-1\n")
        self._output_file.write("D=M\n")
        self._output_file.write(f"@{self._file_name}&{label}\n")
        self._output_file.write("M=M+1\n")
        self._output_file.write("M=M-1\n")
        self._output_file.write("D;JNE\n")

    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command.
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "function function_name n_vars" is:
        # (function_name)       // injects a function entry label into the code
        # repeat n_vars times:  // n_vars = number of local variables
        #   push constant 0     // initializes the local variables to 0

        self._output_file.write("// function command:\n")
        self._output_file.write("(" + function_name + ")\n")
        for var in range(n_vars):
            self._output_file.write("@SP\n")
            self._output_file.write("A=M\n")
            self._output_file.write("M=0\n")
            self._output_file.write("@SP\n")
            self._output_file.write("M=M+1\n")

    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command.
        Let "Xxx.foo" be a function within the file Xxx.vm.
        The handling of each "call" command within Xxx.foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "Xxx.foo").
        This symbol is used to mark the return address within the caller's
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "call function_name n_args" is:
        # push return_address   // generates a label and pushes it to the stack
        # push LCL              // saves LCL of the caller
        # push ARG              // saves ARG of the caller
        # push THIS             // saves THIS of the caller
        # push THAT             // saves THAT of the caller
        # ARG = SP-5-n_args     // repositions ARG
        # LCL = SP              // repositions LCL
        # goto function_name    // transfers control to the callee
        # (return_address)      // injects the return address label into the code

        # generate special label with $ sign:
        return_label = f"{self._file_name}&{function_name}{self.return_address_count}"

        # push return_label to the global stack:
        self._output_file.write("// call command:\n")
        self._output_file.write(f"@{return_label}\n")
        self._output_file.write("D=A\n")
        self._output_file.write("@SP\n")
        self._output_file.write("A=M\n")
        self._output_file.write("M=D\n")
        self._output_file.write("@SP\n")
        self._output_file.write("M=M+1\n")

        # push LCL:
        self._output_file.write(f"@LCL\n")
        self._output_file.write("D=M\n")
        self._output_file.write("@SP\n")
        self._output_file.write("A=M\n")
        self._output_file.write("M=D\n")
        self._output_file.write("@SP\n")
        self._output_file.write("M=M+1\n")

        # push ARG:
        self._output_file.write(f"@ARG\n")
        self._output_file.write("D=M\n")
        self._output_file.write("@SP\n")
        self._output_file.write("A=M\n")
        self._output_file.write("M=D\n")
        self._output_file.write("@SP\n")
        self._output_file.write("M=M+1\n")

        # push THIS:
        self._output_file.write(f"@THIS\n")
        self._output_file.write("D=M\n")
        self._output_file.write("@SP\n")
        self._output_file.write("A=M\n")
        self._output_file.write("M=D\n")
        self._output_file.write("@SP\n")
        self._output_file.write("M=M+1\n")

        # push THAT:
        self._output_file.write("@THAT\n")
        self._output_file.write("D=M\n")
        self._output_file.write("@SP\n")
        self._output_file.write("A=M\n")
        self._output_file.write("M=D\n")
        self._output_file.write("@SP\n")
        self._output_file.write("M=M+1\n")

        # initialize the new val of ARG:
        self._output_file.write("@SP\n")
        self._output_file.write("D=M\n")
        self._output_file.write(f"@5\n")
        self._output_file.write("D=D-A\n")
        self._output_file.write(f"@{n_args}\n")
        self._output_file.write("D=D-A\n")
        self._output_file.write("@ARG\n")
        self._output_file.write("M=D\n")

        # LCL = SP:
        self._output_file.write("@SP\n")
        self._output_file.write("D=M\n")
        self._output_file.write("@LCL\n")
        self._output_file.write("M=D\n")

        # goto function:
        self._output_file.write(f"@{function_name}\n")
        self._output_file.write("0;JMP\n")

        # generate return_label:
        self.write_label(f"{function_name}{self.return_address_count}")
        self.return_address_count += 1

    def write_return(self) -> None:
        """Writes assembly code that affects the return command."""
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "return" is:
        # frame = LCL                   // frame is a temporary variable
        # return_address = *(frame-5)   // puts the return address in a temp var
        # *ARG = pop()                  // repositions the return value for the caller
        # SP = ARG + 1                  // repositions SP for the caller
        # THAT = *(frame-1)             // restores THAT for the caller
        # THIS = *(frame-2)             // restores THIS for the caller
        # ARG = *(frame-3)              // restores ARG for the caller
        # LCL = *(frame-4)              // restores LCL for the caller
        # goto return_address           // go to the return address

        # frame = LCL:
        self._output_file.write("// return command:\n")
        self._output_file.write("@LCL\n")
        self._output_file.write("D=M\n")
        self._output_file.write("@R13\n")
        self._output_file.write("M=D\n")

        # return_address = *(frame-5):
        self._output_file.write("@5\n")
        self._output_file.write("A=D-A\n")
        self._output_file.write("D=M\n")
        self._output_file.write("@R14\n")
        self._output_file.write("M=D\n")

        # *ARG = pop():
        self._output_file.write("@SP\n")
        self._output_file.write("AM=M-1\n")
        self._output_file.write("D=M\n")
        self._output_file.write("@ARG\n")
        self._output_file.write("A=M\n")
        self._output_file.write("M=D\n")

        # SP = ARG + 1:
        self._output_file.write("@ARG\n")
        self._output_file.write("D=M+1\n")
        self._output_file.write("@SP\n")
        self._output_file.write("M=D\n")

        # THAT = *(frame-1):
        self.initialize_segment("THAT", 1)

        # THIS = *(frame-2):
        self.initialize_segment("THIS", 2)

        # ARG = *(frame-3):
        self.initialize_segment("ARG", 3)

        # LCL = *(frame-4):
        self.initialize_segment("LCL", 4)

        # goto return_address:
        self._output_file.write("@R14\n")
        self._output_file.write("A=M\n")
        self._output_file.write("0;JMP\n")

    def initialize_segment(self, segment, number_to_subtract):
        self._output_file.write(f"@{number_to_subtract}\n")
        self._output_file.write(f"D=A\n")
        self._output_file.write("@R13\n")
        self._output_file.write("D=M-D\n")
        self._output_file.write("A=D\n")
        self._output_file.write("D=M\n")
        self._output_file.write(f"@{segment}\n")
        self._output_file.write("M=D\n")
        self._output_file.write("M=M+1\n")
        self._output_file.write("M=M-1\n")
