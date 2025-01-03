from bitstring import Bits

variables = {}
assembly_code = []
instruction_list = {}

MRI_table = {
    'AND': '0',
    'ADD': '1',
    'LDA': '2',
    'STA': '3',
    'BUN': '4',
    'BSA': '5',
    'ISZ': '6'
}

NON_MRI_table = {
    'CLA': '7800',
    'CLE': '7400',
    'CMA': '7200',
    'CME': '7100',
    'CIR': '7080',
    'CIL': '7040',
    'INC': '7020',
    'SPA': '7010',
    'SNA': '7008',
    'SZA': '7004',
    'SZE': '7002',
    'HLT': '7001',
    'INP': 'F800',
    'OUT': 'F400',
    'SKI': 'F200',
    'SKO': 'F100',
    'ION': 'F080',
    'IOF': 'F040'
}

# Read the assembly code from the file as a list of lines
with open('asm.txt', "r") as text_file:
    lines = text_file.readlines()

# Store the assembly code in a list of lists of tokens
for line in lines:
    line = line.split()
    assembly_code.append(line)



def make_dir(origin, line, instruction_list=instruction_list):
    """
    Adds a line to the instruction list with the given origin as the key.

    Args:
        origin (str): The key for the instruction list.
        line (str): The line to be added to the instruction list.
        instruction_list (dict): The dictionary to store the instructions.
    """
    instruction_list[origin] = line


def first_pass(assembly_code):
    """
    Performs the first pass of the assembler to create the address symbol table.

    Args:
        assembly_code (list): The list of assembly code lines.
    """
    origin = 0
    for line in assembly_code:
        if line[0] == 'ORG':
            origin = int(line[1], 16)
            continue
        elif line[0] == 'END':
            break
        elif line[0][-1] == ',':
            make_dir(origin, line)
            variables[line[0][:-1]] = origin
            origin += 1
        else:
            origin += 1
            make_dir(origin, line)


def second_pass(assembly_code):
    """
    Performs the second pass of the assembler to generate the machine code.

    Args:
        assembly_code (list): The list of assembly code lines.
    """
    counter = 0
    origin = 0

    for line in assembly_code:
        # saves the origin place of the program
        if line[0] == 'ORG':
            origin = int(line[1], 16)
            continue
        # Ends the program when END is reached
        elif line[0] == 'END':
            break
        # Checks for memory reference instructions in the memory reference instruction table
        elif line[0] in MRI_table:
            opcode = bin(int(MRI_table[line[0]], 16))[2:].zfill(4)
            if line[1] in variables:
                address = variables[line[1]]
                address = bin(address)[2:].zfill(12)
                print(f"{Bits(int=counter, length=16).bin}  {opcode}{address}")

        else:
            # converts the value of the variables intialised in the first pass into binary
            if line[0] not in NON_MRI_table and line[0][:-1] in variables:
                # Converts the value of the variable into binary from either hex or decimal based on the type referened in the assembly code
                if line[1] == ["HEX"]:
                    number = Bits(hex=int(line[2], 16), length=16).bin
                else:
                    number = Bits(int=int(line[2]), length=16).bin

                print(f"{Bits(int=counter, length=16).bin}  {number}")

            # Converts the non memory reference instructions into binary from their hexadecimal code
            else:
                opcode = NON_MRI_table[line[0]]
                code = ''
                for i in opcode:
                    code += bin(int(i, 16))[2:].zfill(4)
                print(f"{Bits(int=counter, length=16).bin}  {code}")
        # Increments the counter to keep track of the memory address
        counter += 1


# Execute passes
first_pass(assembly_code)
second_pass(assembly_code)