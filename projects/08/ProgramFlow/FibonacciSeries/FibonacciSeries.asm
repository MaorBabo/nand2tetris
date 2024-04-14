// push argument 1
@ARG
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
M=M
// pop pointer 1
@SP
M=M-1
M=M+1
M=M-1
A=M
D=M
@4
M=D
M=M
// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
M=M
// pop that 0
@THAT
D=M
@0
D=D+A
@R15
M=D
@SP
AM=M-1
D=M
@R15
M=M-1
M=M+1
A=M
M=D
M=M
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
M=M
// pop that 1
@THAT
D=M
@1
D=D+A
@R15
M=D
@SP
AM=M-1
D=M
@R15
M=M-1
M=M+1
A=M
M=D
M=M
// push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
M=M
// push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
M=M
// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
M=M
// pop argument 0
@ARG
D=M
@0
D=D+A
@R15
M=D
@SP
AM=M-1
D=M
@R15
A=M
M=D
M=M
// label command:
(FibonacciSeries&MAIN_LOOP_START)
M=M
// push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
M=M
// if-goto command:
@SP
AM=M-1
D=M
@FibonacciSeries&COMPUTE_ELEMENT
D;JNE
M=M
// goto command:
@FibonacciSeries&END_PROGRAM
0;JMP
M=M
// label command:
(FibonacciSeries&COMPUTE_ELEMENT)
M=M
// push that 0
@THAT
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
M=M
// push that 1
@THAT
D=M
@1
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
M=M
// add
@SP
AM=M-1
D=M
A=A-1
M=M+D
M=M
// pop that 2
@THAT
D=M
@2
D=D+A
@R15
M=D
@SP
AM=M-1
D=M
@R15
M=M-1
M=M+1
A=M
M=D
M=M
// push pointer 1
@1
D=A
@3
M=M-1
M=M+1
A=D+A
D=M
@SP
M=M-1
M=M+1
A=M
M=D
@SP
M=M-1
M=M+1
M=M+1
M=M
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
M=M
// add
@SP
AM=M-1
D=M
A=A-1
M=M+D
M=M
// pop pointer 1
@SP
M=M-1
M=M+1
M=M-1
A=M
D=M
@4
M=D
M=M
// push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
M=M
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
M=M
// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
M=M
// pop argument 0
@ARG
D=M
@0
D=D+A
@R15
M=D
@SP
AM=M-1
D=M
@R15
A=M
M=D
M=M
// goto command:
@FibonacciSeries&MAIN_LOOP_START
0;JMP
M=M
// label command:
(FibonacciSeries&END_PROGRAM)
M=M
