from execution.optcode import *

class Instruction():
    pass

class RTypeInstruction(Instruction):
    def __init__(self, subop: RTypeSuboperands, rd: int, rs1: int, rs2: int):
        self.subop = subop
        self.rd = rd
        self.rs1 = rs1
        self.rs2 = rs2

class ITypeInstruction(Instruction):
    def __init__(self, subop: ITypeSuboperands, rd: int, rs1: int, imm: int):
        self.subop = subop
        self.rd = rd
        self.rs1 = rs1
        self.imm = imm

class BTypeInstruction(Instruction):
    def __init__(self, subop: BTypeSuboperands, offset: int):
        self.subop = subop
        self.offset = offset

class JTypeInstruction(Instruction):
    def __init__(self, subop: JTypeSuboperands, offset: int):
        self.subop = subop
        self.offset = offset

def build_instruction(bits: int) -> Instruction:
    bits = bits & 0xFFFF

    instruction_subop, instruction_data = decode_instruction(bits)
    if isinstance(instruction_subop, RTypeSuboperands):
        instruction = _r_type_instruction_split(instruction_subop, instruction_data)
    elif isinstance(instruction_subop, ITypeSuboperands):
        instruction = _i_type_instruction_split(instruction_subop, instruction_data)
    elif isinstance(instruction_subop, BTypeSuboperands):
        instruction = _b_type_instruction_split(instruction_subop, instruction_data)
    elif isinstance(instruction_subop, JTypeSuboperands):
        instruction = _j_type_instruction_split(instruction_subop, instruction_data)
    else:
        raise Exception("Non existent instruction class")

    return instruction


def _r_type_instruction_split(instruction_subop: RTypeSuboperands, instruction_data: int) -> RTypeInstruction:
    rd = (instruction_data >> 6) & 0b111
    rs1 = (instruction_data >> 3) & 0b111
    rs2 = instruction_data & 0b111

    return RTypeInstruction(instruction_subop, rd, rs1, rs2)

def _i_type_instruction_split(instruction_subop: ITypeSuboperands, instruction_data: int) -> ITypeInstruction:
    # See documentation, LOAD and STORE use non standard layout for their class.
    if instruction_subop == 0b0111 or instruction_subop == 0b1000:
        rd = (instruction_data >> 7) & 0b111
        rs1 = (instruction_data >> 6) & 0b1
        imm = instruction_data & 0b111111

        return ITypeInstruction(instruction_subop, rd, rs1, imm)

    else:
        rd = (instruction_data >> 7) & 0b111
        rs1 = (instruction_data >> 4) & 0b111
        imm = instruction_data & 0b1111

        return ITypeInstruction(instruction_subop, rd, rs1, imm)

def _b_type_instruction_split(instruction_subop: BTypeSuboperands, instruction_data: int) -> BTypeInstruction:
    return BTypeInstruction(instruction_subop, instruction_data)

def _j_type_instruction_split(instruction_subop: JTypeSuboperands, instruction_data: int) -> JTypeInstruction:
    return JTypeInstruction(instruction_subop, instruction_data)
