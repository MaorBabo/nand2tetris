// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
M=M
// pop local 0
@LCL
D=M
@0
D=D+A
@R15
M=M-1
M=M+1
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
// label command:
(BasicLoop&LOOP_START)
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
// push local 0
@LCL
M=M-1
M=M+1
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M-1
M=M+1
M=M+1
M=M
// add
@SP
AM=M-1
D=M
A=A-1
M=M+D
M=M
// pop local 0
@LCL
D=M
@0
D=D+A
@R15
M=M-1
M=M+1
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
@BasicLoop&LOOP_START
D;JNE
M=M
// push local 0
@LCL
M=M-1
M=M+1
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M-1
M=M+1
M=M+1
M=M