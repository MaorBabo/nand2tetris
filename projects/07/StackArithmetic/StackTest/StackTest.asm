// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D-M
@EQUAL11
D;JEQ
@FALSE11
0;JMP
(EQUAL11)
@SP
A=M
M=-1
@END11
0;JMP
(FALSE11)
@SP
A=M
M=0
(END11)
@SP
M=M+1
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D-M
@EQUAL12
D;JEQ
@FALSE12
0;JMP
(EQUAL12)
@SP
A=M
M=-1
@END12
0;JMP
(FALSE12)
@SP
A=M
M=0
(END12)
@SP
M=M+1
// push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D-M
@EQUAL13
D;JEQ
@FALSE13
0;JMP
(EQUAL13)
@SP
A=M
M=-1
@END13
0;JMP
(FALSE13)
@SP
A=M
M=0
(END13)
@SP
M=M+1
// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D-M
@IS_LESS14
D;JGT
@FALSE14
0;JMP
(IS_LESS14)
@SP
A=M
M=-1
@END14
0;JMP
(FALSE14)
@SP
A=M
M=0
(END14)
@SP
M=M+1
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D-M
@IS_LESS15
D;JGT
@FALSE15
0;JMP
(IS_LESS15)
@SP
A=M
M=-1
@END15
0;JMP
(FALSE15)
@SP
A=M
M=0
(END15)
@SP
M=M+1
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D-M
@IS_LESS16
D;JGT
@FALSE16
0;JMP
(IS_LESS16)
@SP
A=M
M=-1
@END16
0;JMP
(FALSE16)
@SP
A=M
M=0
(END16)
@SP
M=M+1
// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D-M
@IS_GREATER17
D;JLT
@FALSE17
0;JMP
(IS_GREATER17)
@SP
A=M
M=-1
@END17
0;JMP
(FALSE17)
@SP
A=M
M=0
(END17)
@SP
M=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D-M
@IS_GREATER18
D;JLT
@FALSE18
0;JMP
(IS_GREATER18)
@SP
A=M
M=-1
@END18
0;JMP
(FALSE18)
@SP
A=M
M=0
(END18)
@SP
M=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D-M
@IS_GREATER19
D;JLT
@FALSE19
0;JMP
(IS_GREATER19)
@SP
A=M
M=-1
@END19
0;JMP
(FALSE19)
@SP
A=M
M=0
(END19)
@SP
M=M+1
// push constant 57
@57
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 31
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 53
@53
D=A
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
AM=M-1
D=M
A=A-1
M=M+D
// push constant 112
@112
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
// neg
@SP
AM=M-1
M=-M
@SP
M=M+1
// and
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=D&M
@SP
M=M+1
// push constant 82
@82
D=A
@SP
A=M
M=D
@SP
M=M+1
// or
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=D|M
@SP
M=M+1
// not
@SP
AM=M-1
M=!M
@SP
M=M+1