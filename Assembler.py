"""
This is a 2-pass Assembler the capacity to handle OpCodes mentioned below and variables. Just like any standard 2-pass Assembler, it scans through the
code twice, 1st time to find out how long the machine code will be and storing the OpCodes in the Intermediate Table and hence the address of labels 
and storing them in the Symbol Tabel. Then the actual Machine Code is genertaed using the Intermidiate Table and Symbol Table.

The assembler handles the following Assembly OpCodes:
CLA : Clears the accumulator
LAC <Memory Address> : Load into accumulator from address
SAC <Memory Address> : Store accumulator contents into address
ADD <Memory Address> : Add address contents to accumulator contents
SUB <Memory Address> : Subtract address contents from accumulator contents
BRZ <Memory Address> : Branch to address if accumulator contains zero
BRN <Memory Address> : Branch to address if accumulator contains negative value
BRP <Memory Address> : Branch to address if accumulator contains positive value
INP <Memory Address> : Read from terminal and put in address
DSP <Memory Address> : Display value in address on terminal
MUL <Memory Address> : Multiply accumulator and address contents
DIV <Memory Address> : Divide accumulator contents by address content. Quotient in register R1 corresponding to address 00000000 
                      and remainder in register R2 corresponding to address 00000001.
STP : Stop execution

Syntax for the above mentioned OpCodes:

1)  Start your code with “START <Address(optional)>”.
2)  A line should have only 1 OpCode.
3)  OpCodes “CLA” and “STP” shouldn’t have any address provided to them as operand while all the other operands must have a valid address.
4)  To define a label follow this syntax  <LabelName> : <OpCode> <Address(if required)>.
5)  To add a comment type ";". Everything ahead of it is treated as a comment.
6)  Add “END” to end the code.


The output provides us with the corresponding machine code like so:

In the 1st pass we make the Intermediate Table and Symbol Table by checking the following:
1)  If the inputted OpCode is valid. Any invalid instruction return "Invalid Opcode!".
2)  If the instruction requires address, and hence the length of the instruction. If the instruction is too long, it returns "Too long instructions".
3)  If the instruction contains Label. We hence add the Label to the Symbol Table with the current location counter value. We also add the label with
the OpCode and the operand(if required) to Intermediate Table.
4)  We ignore the comments which are identified using ";".

In the 2nd pass we traverse the Intermediate Table and construct the corresponding Machine Code.


Errors handeled: 

1)  Use of Invalid OpCodes.
2)  Checks missing "END".
3)  Missing Operand for OpCodes that require one.
4)  Extra Operand provided for OpCodes that don't require it.
5)  Use of undefined labels.
6)  Defining a label more than once.
7)  Invalid syntax for label definition.
8)  START must be present.
9)  START can’t have more than 1 operand. 
10) START must have a valid address/ operand.
11) Handles empty/blank lines.
"""

import sys
import math
assemblyCode = []
symbolTable = {}
intermediateTable = []
machineCode = []
memory = []
locationCounter = 2
opcodeTable = {"CLA":0,"LAC":1,"SAC":2,"ADD":3,"SUB":4,"BRZ":5,"BRN":6,"BRP":7,"INP":8,"DSP":9,"MUL":10,"DIV":11,"STP":12}
register = {"R1":"00000000","R2":"00000001"}
stpExist = True
endExist = False


# def decToBin(num,size):
#     return format(num,'b').zfill(size)

def decToBin(num,size):
    if (num >= 2**size):
        print("Address Out of Bounds! Select a valid Address")
        return ("none")
    else:
        return format(num,'b').zfill(size)

# since 12 bit accumulator, and 4 bits reserved for opcode, address is of 8 bits
# 2^8 = 256. thus, memory address size = 256
for i in range(256):
    binaryNo = decToBin(i,8)
    memory.append(binaryNo)

# print (memory)  

#check is a string is without a space
def single(text):
    if (len(text.split()) == 1):
        return True
    else:
        return False

# remove \n from the list contents
def removeN(someList):
    for i in range(len(someList)-1):
        l = len(someList[i])
        someList[i] = someList[i][:l-1]
    return someList
    
#initializing the tables
def initalizeTables():
    global symbolTable
    global intermediateTable
    symbolTable = {}
    iteralTable = []
    intermediateTable = []

def lengthOfInstruction(assemblyInstruction):
    if (":" in assemblyInstruction):
        assemblyInstruction = assemblyInstruction[assemblyInstruction.find(":")+1:] #removes labels
    elements = assemblyInstruction.split()
    length = 0

    for i in elements:
        if (i in opcodeTable):
            length += 4 #opcode
        else:
            length += 8 #address

    return math.ceil(length/8) #return number of bytes in the instruction
    

def passOne():

    global symbolTable
    global intermediateTable
    global assemblyCode
    global locationCounter
    global opcodeTable
    global stpExist
    global endExist

    initalizeTables()

    #remove the /n from each instruction
    assemblyCode = removeN(assemblyCode)
    start = assemblyCode[0].split()

    if (start[0].upper() != 'START'):
        print ("START not present")
        sys.exit(0)

    elif (len(start) == 2):
        if (start[1].isdigit() and int(start[1]) >= 2):
            locationCounter = int(start[1])
        elif (start[1].isdigit() == False):
            print ("Operand of START should be number only")
            sys.exit(0)
        else:
            print("Location Counter starting form 2")

    elif (len(start) > 2):
        print ("START cannot have more than 1 operand")

    

    for assemblyInstruction in assemblyCode[1:]:
        # print(assemblyInstruction)

        length = lengthOfInstruction(assemblyInstruction)

        if (";" in assemblyInstruction):
            assemblyInstruction = assemblyInstruction[:assemblyInstruction.find(";")]

        if (single(assemblyInstruction) == True):

            if (assemblyInstruction != "END" and opcodeTable.get(assemblyInstruction) == None):
                print("Invalid Opcode! Opcode doesn't exist in Opcode Table!")
                continue
                
            if (assemblyInstruction == "STP"):
                stpExist = True

            if (assemblyInstruction == "END"):
                endExist = True

            if (assemblyInstruction == "CLA"):
                # print(opcodeTable.get(assemblyInstruction))
                # intermediateTable.append([opcodeTable.get(assemblyInstruction)])
                intermediateTable.append("(OP,"+str(opcodeTable.get(assemblyInstruction))+")")
                # intermediateTable.append("OP "+str(decToBin(opcodeTable.get(assemblyInstruction),4)))

            else:
                if (assemblyInstruction != "END"):
                    print ("Invalid Instruction!")
                    continue

            # if (opcodeTable.get(assemblyInstruction) in range(1, 12)):
            #     print ("Address not provided!")


        elif (single(assemblyInstruction) == False): # not CLA

            if (assemblyInstruction.find(":") == -1): # doesn't have a label
                
                assemblyInstructionList = assemblyInstruction.split()

                if (len(assemblyInstructionList) != 2):
                    print ("Too long instructions! Extra data added (including new empty line)! Reduce data.")
                    continue

                assemblyOpCode = assemblyInstructionList[0]
                address = assemblyInstructionList[1]

                if (assemblyOpCode=="CLA" or assemblyOpCode=="STP"):
                    print("Too Many Operands provided!")

                if (opcodeTable.get(assemblyOpCode) == None):
                    print("Invalid Opcode! Opcode doesn't exist in Opcode Table!")
                    continue

                if address.isdigit(): # not a label, just a normal instruction
                    intermediateTable.append("(OP,"+str(opcodeTable.get(assemblyOpCode))+") " + str(decToBin(int(address),8)))
                    # intermediateTable.append("OP "+str(decToBin(opcodeTable.get(assemblyOpCode),4))+" " + str(decToBin(int(address),8)))

                else:

                    if (address not in symbolTable):
                        if ( assemblyOpCode not in ["BRZ","BRN","BRP"]):
                            symbolTable[address] = ["VARIABLE","None"] #VAIRABLE, adds variable in sybmol table 

                    intermediateTable.append("(OP,"+str(opcodeTable.get(assemblyOpCode))+") " + address)


            elif (assemblyInstruction.find(":") != 1): # has a label or variable
                assemblyInstructionList = assemblyInstruction.split()

                if (assemblyInstructionList[0].find(":") == len(assemblyInstructionList[0])-1):
                    currentSymbol = assemblyInstructionList[0][:-1]
                    
                    # if (currentSymbol in symbolTable):
                    #     print("Symbol defined more than once")
                    #     continue
                    # else:

                    #     if ( assemblyOpCode in ["BRZ","BRN","BRP"]):
                    #         symbolTable[currentSymbol] = ["LABEL",locationCounter] #LABEL, adds label in sybmol table
                    #     else:
                    #         symbolTable[currentSymbol] = ["VARIABLE",locationCounter] #VAIRABLE, adds variable in sybmol table   
                    
                    if (currentSymbol in symbolTable):
                        print("Symbol defined more than once")
                        continue
                    else:
                        symbolTable[currentSymbol] = ["LABEL",locationCounter] #LABEL, adds label in sybmol table
                        

                    if (len(assemblyInstructionList) == 2):
                        label = assemblyInstructionList[0][:-1]
                        assemblyOpCode = assemblyInstructionList[1]

                        if (assemblyOpCode == "STP"):
                            stpExist = True
                        
                        if (opcodeTable.get(assemblyOpCode) == None):
                            print("Invalid Opcode! Opcode doesn't exist in Opcode Table!")
                            continue

                        intermediateTable.append("(ST,"+label+") " + "(OP,"+str(opcodeTable.get(assemblyOpCode))+")")
                    
                    elif (len(assemblyInstructionList) == 3):
                        label = assemblyInstructionList[0][:-1]
                        assemblyOpCode = assemblyInstructionList[1]
                        address = assemblyInstructionList[2]

                        if (assemblyOpCode=="CLA" or assemblyOpCode=="STP"):
                            print("Too Many Operands provided!")

                        if (assemblyOpCode == "STP"):     
                            stpExist = True

                        if (opcodeTable.get(assemblyOpCode) == None):
                            print("Invalid Opcode! Opcode doesn't exist in Opcode Table!")
                            continue

                        if (address.isdigit() == False):
                            if (assemblyOpCode != "BRZ" and assemblyCode != "BRN" and assemblyOpCode != "BRP"):
                                symbolTable[address] = ["VARIABLE","None"] #VAIRABLE, adds variable in sybmol table 
                                intermediateTable.append("(ST,"+label+") " + "(OP,"+str(opcodeTable.get(assemblyOpCode))+") " + address)
                        try:
                            intermediateTable.append("(ST,"+label+") " + "(OP,"+str(opcodeTable.get(assemblyOpCode))+") " + str(decToBin(int(address),8)))
                        except:
                            pass

                    else:
                        print ("Invalid Opcode!")
                        continue

                else:
                    print ("Invalid Opcode!")
                    continue

        else:
            print ("Invalid Opcode!")
            continue

        # print("locationCounter "+str(locationCounter))
        locationCounter += length


    for i in symbolTable:
        if (symbolTable[i][0] == "VARIABLE" and symbolTable[i][1] == "None"):
            symbolTable[i][1] = locationCounter
            locationCounter += 1

    print ()
    print ("Symbol Table")
    print ()
    for i in symbolTable:
        try:
            print (str(i) + " " + str(decToBin(symbolTable[i][1],8)))    
        except:
            print (str(i) + " " + symbolTable[i][1])

    print ()
    print ("-------------------------------")
    print ()

    print ("Intermediate Table")
    print ()
    for i in intermediateTable:
        print (i)

    if (endExist == True):
        print ("END doesn't exist!")
        print ("Warning: END should be the only syntax of the instruction")

def passTwo():
    

    for instruction in intermediateTable:
        output=""
        
        if (single(instruction) == True):
            instructionList = instruction.split(",")
            if (instructionList[1] == "0)"):
                machineCode.append('0000')
                continue
            elif (instructionList[1] == "12)"):
                machineCode.append('1100')
                continue
                
        
        elif len(instruction.split()) == 2:
            instructionList = instruction.split()

            opcode = instructionList[0]
            address = instructionList[1]

            opcodeList = opcode.split(",")

            if (opcodeList[0] == "(OP"):
                output = str(decToBin(int(opcodeList[1][:-1]),4))

            if (opcodeList[0] == "(ST"):
                # REMOVE BELOW COMMENT IF LABEL DECLARATION REQUIRED IN MACHINE LANG OUTPUT
                # output = str(decToBin(int(symbolTable[opcodeList[1][:-1]]),8)) + " "
                output = ""

            if (address.isdigit()):
                output = output + " " + str(address)
                # machineCode.append(output)

            else: #if label in address place, address is variable which stores label
                if address in symbolTable: # if symbol exists in symbol table, i.e. if label is declared
                    if (symbolTable[address][0] == "LABEL"): #label
                        output = output + " " + str( decToBin(int(symbolTable[address][1]),8))
                    else: # variable
                        output = output + " " + str(decToBin(symbolTable[address][1],8))

                elif (address.split(",")[0] == "(OP"): # cases like these (ST,L2) (OP,12) address variable stores (OP,12)
                    addressList = address.split(",")
                    output = output + "" + decToBin(int(addressList[1][:-1]),4)
                    
                else:
                    print (instruction)
                    print ("Label not defined!")
                    continue

        elif len(instruction.split()) == 3:
            
            instructionList = instruction.split()

            label = instructionList[0]
            opcode = instructionList[1]
            address = instructionList[2]

            labelList = label.split(",")
            # REMOVE BELOW COMMENT IF LABEL DECLARATION REQUIRED IN MACHINE LANG OUTPUT
            # output = decToBin(int(symbolTable[labelList[1][:-1]]),8) + " "
            output = ""

            opcodeList = opcode.split(",")
            
            output = output + decToBin(int(opcodeList[1][:-1]),4)

            if (address.isdigit()):
                output = output + " " + str(address)
            
            else:
                if address in symbolTable: # if symbol exists in symbol table, or i.e. if variable is declared
                    if (symbolTable[address][0] == "LABEL"): #label
                        output = output + " " + str( decToBin(int(symbolTable[address][1]),8))
                    else: # variable
                        output = output + " " + str(decToBin(symbolTable[address][1],8))

        machineCode.append(output)


        
    print ()
    print ("-------------------------------")
    print ()

    print ("Machine Code")
    print ()
    for i in machineCode:
        print (i)


# print(opcodeTable)
# ip = open("input.txt","r")
ip = open("input2.txt","r")
    
assemblyCode = ip.readlines()
lengthAssemblyCode = len(assemblyCode) # length of assembly code
ip.close()
passOne()
passTwo()