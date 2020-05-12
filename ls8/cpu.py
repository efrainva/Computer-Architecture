"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.pc = 0# the pointer
        self.ram = [0] * 256
        # register
        self.reg = [0] * 8
        self.reg[7] = 0xF4

        self.sp = 7

        self.opcodes = {
            0b00000001: "HLT",
            0b01000111: "PRN",
            0b10000010: "LDI",
            0b10100010: "MUL", 
            0b01000101: "PUSH",
            0b01000110: "POP", 
            0b10100000: "ADD",

        }   


    def ram_read(self, address):

        return self.ram[address]

    def ram_write(self, address, item):
        write = self.ram[address] = item
        return write

    def load(self, filename): 
        address = 0
        try:
            with open(filename) as file:
                for line in file:
                    fileSplit = line.split("#")
                    numberString = fileSplit[0].strip()

                    if numberString == "":
                        continue

                    num = int(numberString, 2)
                    self.ram[address] = num
                    address += 1

        except FileNotFoundError:
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            # self.pc += 3
        elif op == "MUL":
            self.reg[reg_a] += self.reg[reg_b]
            # self.pc += 3
        else:
            raise Exception("Unsupported ALU operation")



    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        print(self.pc)
        self.running = True 
        while self.running:
            IR = self.ram_read(self.pc)
            print(self.pc)
            #  print("This is what's not working", IR)
            operandA = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            opcode = self.opcodes[IR]
            if opcode == "HLT":
                self.running = False
            if opcode == "PRN":
                print(self.reg[operandA])
                self.pc += 2
            if opcode == "LDI":
                self.reg[operandA] = operand_b
                self.pc += 3



            if opcode == "ADD":
                self.reg[operandA] += self.reg[operand_b]
                self.pc += 3

            if opcode == "MUL":
                self.reg[operandA] * self.reg[operand_b]
                self.pc += 3


            if opcode == "PUSH":
                self.reg[self.sp] -= 1
                operandA = self.ram[self.pc + 1]
                item = self.reg[operandA]
                self.ram[self.reg[self.sp]] = item
                self.pc +=2

            if opcode == "POP":
                operandA = self.ram[self.pc + 1]
                item = self.ram[self.reg[self.sp]]
                self.reg[operandA] = item 
                self.reg[self.sp] += 1
                self.pc += 2
