from enum import IntEnum


class InstructionClass(IntEnum):
    R = 0b00
    I = 0b01
    B = 0b10
    J = 0b11


class Suboperand(IntEnum):
    pass


class RTypeSuboperands(Suboperand):
    ADD = 0b00000
    SUB = 0b00001
    AND = 0b00010
    OR = 0b00011
    XOR = 0b00100
    NOT = 0b00101
    SHL = 0b00110
    SHR = 0b00111
    SHRU = 0b01000
    MOV = 0b01001
    CMP = 0b01010
    MUL = 0b01011
    DIV = 0b01100
    DIVU = 0b01101
    PUSH = 0b01110
    POP = 0b01111
    RDSP = 0b10000
    WRSP = 0b10001
    REM = 0b10010
    REMU = 0b10011
    RDPC = 0b10100


class ITypeSuboperands(Suboperand):
    ADDI = 0b0000
    ANDI = 0b0001
    ORI = 0b0010
    XORI = 0b0011
    SHLI = 0b0100
    SHRI = 0b0101
    SHRIU = 0b0110
    LOAD = 0b0111
    STORE = 0b1000
    CMPI = 0b1001


class BTypeSuboperands(Suboperand):
    BEQ = 0b000
    BNE = 0b001
    BLT = 0b010
    BGE = 0b011
    BLTU = 0b100
    BGEU = 0b101


class JTypeSuboperands(Suboperand):
    JMP = 0b0000
    JMPA = 0b0001
    CALL = 0b0010
    CALLA = 0b0011
    RET = 0b0100
    HALT = 0b1111
    NOP = 0b1110


def decode_instruction(bits: int) -> tuple[Suboperand, int]:
    instruction = bits & 0xFFFF

    instruction_class = _decode_class(instruction)

    match instruction_class:
        case InstructionClass.R:
            instruction_subop, instruction_data = _decode_r_type_subop(instruction)
        case InstructionClass.I:
            instruction_subop, instruction_data = _decode_i_type_subop(instruction)
        case InstructionClass.B:
            instruction_subop, instruction_data = _decode_b_type_subop(instruction)
        case InstructionClass.J:
            instruction_subop, instruction_data = _decode_j_type_subop(instruction)
        case _:
            raise Exception("Unknown optcode")

    return instruction_subop, instruction_data


def _decode_class(instruction: int) -> InstructionClass:
    class_bits = (instruction >> (16 - 2)) & 0b11

    instr_class = InstructionClass(class_bits)

    return instr_class


def _decode_r_type_subop(instruction: int) -> tuple[RTypeSuboperands, int]:
    subop_bits = (instruction >> (16 - 2 - 5)) & 0b11111

    subop_class = RTypeSuboperands(subop_bits)

    instruction_data = instruction & 0b111111111

    return (subop_class, instruction_data)


def _decode_i_type_subop(instruction: int) -> tuple[ITypeSuboperands, int]:
    subop_bits = (instruction >> (16 - 2 - 4)) & 0b1111

    subop_class = ITypeSuboperands(subop_bits)

    instruction_data = instruction & 0b1111111111

    return (subop_class, instruction_data)


def _decode_b_type_subop(instruction: int) -> tuple[BTypeSuboperands, int]:
    subop_bits = (instruction >> (16 - 2 - 3)) & 0b111

    subop_class = BTypeSuboperands(subop_bits)

    instruction_data = instruction & 0b11111111111

    return (subop_class, instruction_data)


def _decode_j_type_subop(instruction: int) -> tuple[JTypeSuboperands, int]:
    subop_bits = (instruction >> (16 - 2 - 4)) & 0b1111

    subop_class = JTypeSuboperands(subop_bits)

    instruction_data = instruction & 0b1111111111

    return (subop_class, instruction_data)
