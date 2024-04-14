// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// The program should swap between the max. and min. elements of an array.
// Assumptions:
// - The array's start address is stored in R14, and R15 contains its length
// - Each array value x is between -16384 < x < 16384
// - The address in R14 is at least >= 2048
// - R14 + R15 <= 16383
//
// Requirements:
// - Changing R14, R15 is not allowed.


// define two registers that will store the max and min address
@R0
M=0
@20000
D=A
@R1
M=D
@20000
M=A
@R2
M=0

// define the index i that will go over the array
@i 
M=0
@j
M=0

// find max/min value in array
(LOOP)

	@INRANGE
	0;JMP
	
	(INRANGES)
	@R14
	D=M
	@i
	A=D+M
	D=M
	@R0
	A=M
	D=D-M
	@UPDATEMAX
	D;JGT
	
	(UPDATEMAXS)
	@R14
	D=M
	@i
	A=D+M
	D=M
	@R1
	A=M
	D=D-M
	@UPDATEMIN
	D;JLT
	
	(UPDATEMINS)
	// update i
	@i
	M=M+1
	
	@LOOP
	0;JMP
	
	






// check boundries
(INRANGE)
	@i
	D=M
	@R15
	D=D-M
	@SWAP
	D;JEQ
	@INRANGES
	0;JMP
	

// update max value
(UPDATEMAX)
	@R14
	D=M
	@i
	A=D+M
	D=A
	@R0
	M=D
	@UPDATEMAXS
	0;JMP
	
// update min value
(UPDATEMIN)
	@R14
	D=M
	@i
	A=D+M
	D=A
	@R1
	M=D
	@UPDATEMINS
	0;JMP
	

	
(SWAP)
	@R0
	A=M
	D=M
	@R2
	M=D
	
	@R1
	A=M
	D=M
	
	@R0
	A=M
	M=D
	
	@R2
	D=M
	@R1
	A=M
	M=D
	
	@END
	0;JMP
	
	
	
	


(END)
@END
0;JMP
	
