from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cpu_architecture.cpu import CPU

from execution.builder import *
from execution.optcode import RTypeSuboperands, ITypeSuboperands, BTypeSuboperands, JTypeSuboperands
import os

class Dispatcher:
    @staticmethod
    def execute_instruction(cpu: CPU, bits: int):
        bits = bits & 0xFFFF

        instruction = build_instruction(bits)

        if isinstance(instruction, RTypeInstruction):
            match instruction.subop:
                case RTypeSuboperands.ADD:
                    RTypeExecutions.ADD(cpu, instruction)
                case RTypeSuboperands.SUB:
                    RTypeExecutions.SUB(cpu, instruction)
                case RTypeSuboperands.AND:
                    RTypeExecutions.AND(cpu, instruction)
                case RTypeSuboperands.OR:
                    RTypeExecutions.OR(cpu, instruction)
                case RTypeSuboperands.XOR:
                    RTypeExecutions.XOR(cpu, instruction)
                case RTypeSuboperands.NOT:
                    RTypeExecutions.NOT(cpu, instruction)
                case RTypeSuboperands.SHL:
                    RTypeExecutions.SHL(cpu, instruction)
                case RTypeSuboperands.SHR:
                    RTypeExecutions.SHR(cpu, instruction)
                case RTypeSuboperands.SHRU:
                    RTypeExecutions.SHRU(cpu, instruction)
                case RTypeSuboperands.MOV:
                    RTypeExecutions.MOV(cpu, instruction)
                case RTypeSuboperands.CMP:
                    RTypeExecutions.CMP(cpu, instruction)
                case RTypeSuboperands.MUL:
                    RTypeExecutions.MUL(cpu, instruction)
                case RTypeSuboperands.DIV:
                    RTypeExecutions.DIV(cpu, instruction)
                case RTypeSuboperands.DIVU:
                    RTypeExecutions.DIVU(cpu, instruction)
                case RTypeSuboperands.PUSH:
                    RTypeExecutions.PUSH(cpu, instruction)
                case RTypeSuboperands.POP:
                    RTypeExecutions.POP(cpu, instruction)
                case RTypeSuboperands.RDSP:
                    RTypeExecutions.RDSP(cpu, instruction)
                case RTypeSuboperands.WRSP:
                    RTypeExecutions.WRSP(cpu, instruction)
                case RTypeSuboperands.REM:
                    RTypeExecutions.REM(cpu, instruction)
                case RTypeSuboperands.REMU:
                    RTypeExecutions.REMU(cpu, instruction)
                case RTypeSuboperands.RDPC:
                    RTypeExecutions.RDPC(cpu, instruction)
                case _:
                    raise Exception(f"Unimplemented R-type subop: {instruction.subop}")

        elif isinstance(instruction, ITypeInstruction):
            match instruction.subop:
                case ITypeSuboperands.ADDI:
                    ITypeExecutions.ADDI(cpu, instruction)
                case ITypeSuboperands.ANDI:
                    ITypeExecutions.ANDI(cpu, instruction)
                case ITypeSuboperands.ORI:
                    ITypeExecutions.ORI(cpu, instruction)
                case ITypeSuboperands.XORI:
                    ITypeExecutions.XORI(cpu, instruction)
                case ITypeSuboperands.SHLI:
                    ITypeExecutions.SHLI(cpu, instruction)
                case ITypeSuboperands.SHRI:
                    ITypeExecutions.SHRI(cpu, instruction)
                case ITypeSuboperands.SHRIU:
                    ITypeExecutions.SHRIU(cpu, instruction)
                case ITypeSuboperands.LOAD:
                    ITypeExecutions.LOAD(cpu, instruction)
                case ITypeSuboperands.STORE:
                    ITypeExecutions.STORE(cpu, instruction)
                case ITypeSuboperands.CMPI:
                    ITypeExecutions.CMPI(cpu, instruction)
                case _:
                    raise Exception(f"Unimplemented I-type subop: {instruction.subop}")

        elif isinstance(instruction, BTypeInstruction):
            match instruction.subop:
                case BTypeSuboperands.BEQ:
                    BTypeExecutions.BEQ(cpu, instruction)
                case BTypeSuboperands.BNE:
                    BTypeExecutions.BNE(cpu, instruction)
                case BTypeSuboperands.BLT:
                    BTypeExecutions.BLT(cpu, instruction)
                case BTypeSuboperands.BGE:
                    BTypeExecutions.BGE(cpu, instruction)
                case BTypeSuboperands.BLTU:
                    BTypeExecutions.BLTU(cpu, instruction)
                case BTypeSuboperands.BGEU:
                    BTypeExecutions.BGEU(cpu, instruction)
                case _:
                    raise Exception(f"Unimplemented B-type subop: {instruction.subop}")

        elif isinstance(instruction, JTypeInstruction):
            match instruction.subop:
                case JTypeSuboperands.JMP:
                    JTypeExecutions.JMP(cpu, instruction)
                case JTypeSuboperands.JMPA:
                    JTypeExecutions.JMPA(cpu, instruction)
                case JTypeSuboperands.CALL:
                    JTypeExecutions.CALL(cpu, instruction)
                case JTypeSuboperands.CALLA:
                    JTypeExecutions.CALLA(cpu, instruction)
                case JTypeSuboperands.RET:
                    JTypeExecutions.RET(cpu, instruction)
                case JTypeSuboperands.HALT:
                    JTypeExecutions.HALT(cpu, instruction)
                case JTypeSuboperands.NOP:
                    JTypeExecutions.NOP(cpu, instruction)
                case _:
                    raise Exception(f"Unimplemented J-type subop: {instruction.subop}")

        else:
            raise Exception("Can't execute nonexistent instruction")

class RTypeExecutions:
    @staticmethod
    def ADD(cpu: CPU, instructions: RTypeInstruction):
        output_register_address = instructions.rd
        first_input_register_address = instructions.rs1
        second_input_register_address = instructions.rs2

        first_register_value = cpu.regs[first_input_register_address].read()
        second_register_value = cpu.regs[second_input_register_address].read()

        result = cpu.alu.add(first_register_value, second_register_value)
        cpu.regs[output_register_address].write(result)

    @staticmethod
    def SUB(cpu: CPU, instructions: RTypeInstruction):
        first_register_value = cpu.regs[instructions.rs1].read()
        second_register_value = cpu.regs[instructions.rs2].read()

        result = cpu.alu.sub(first_register_value, second_register_value)
        cpu.regs[instructions.rd].write(result)

    @staticmethod
    def AND(cpu: CPU, instructions: RTypeInstruction):
        first_register_value = cpu.regs[instructions.rs1].read()
        second_register_value = cpu.regs[instructions.rs2].read()

        result = cpu.alu.and_(first_register_value, second_register_value)
        cpu.regs[instructions.rd].write(result)

    @staticmethod
    def OR(cpu: CPU, instructions: RTypeInstruction):
        first_register_value = cpu.regs[instructions.rs1].read()
        second_register_value = cpu.regs[instructions.rs2].read()

        result = cpu.alu.or_(first_register_value, second_register_value)
        cpu.regs[instructions.rd].write(result)
 
    @staticmethod
    def XOR(cpu: CPU, instructions: RTypeInstruction):
        first_register_value = cpu.regs[instructions.rs1].read()
        second_register_value = cpu.regs[instructions.rs2].read()

        result = cpu.alu.xor_(first_register_value, second_register_value)
        cpu.regs[instructions.rd].write(result)

    @staticmethod
    def NOT(cpu: CPU, instructions: RTypeInstruction):
        first_register_value = cpu.regs[instructions.rs1].read()

        result = cpu.alu.not_(first_register_value)
        cpu.regs[instructions.rd].write(result)

    @staticmethod
    def SHL(cpu: CPU, instructions: RTypeInstruction):
        first_register_value = cpu.regs[instructions.rs1].read()
        second_register_value = cpu.regs[instructions.rs2].read()

        result = cpu.alu.shl(first_register_value, second_register_value)
        cpu.regs[instructions.rd].write(result)

    @staticmethod
    def SHR(cpu: CPU, instructions: RTypeInstruction):
        first_register_value = cpu.regs[instructions.rs1].read()
        second_register_value = cpu.regs[instructions.rs2].read()

        result = cpu.alu.shr(first_register_value, second_register_value)
        cpu.regs[instructions.rd].write(result)

    @staticmethod
    def SHRU(cpu: CPU, instructions: RTypeInstruction):
        first_register_value = cpu.regs[instructions.rs1].read()
        second_register_value = cpu.regs[instructions.rs2].read()

        result = cpu.alu.shru(first_register_value, second_register_value)
        cpu.regs[instructions.rd].write(result)

    @staticmethod
    def MOV(cpu: CPU, instructions: RTypeInstruction):
        cpu.regs[instructions.rd].write(cpu.regs[instructions.rs1].read())

    @staticmethod
    def CMP(cpu: CPU, instructions: RTypeInstruction):
        first_register_value = cpu.regs[instructions.rs1].read()
        second_register_value = cpu.regs[instructions.rs2].read()

        flags_list = cpu.alu.cmp_flags(first_register_value, second_register_value)
        cpu.flags.set_list(flags_list)

    @staticmethod
    def MUL(cpu: CPU, instructions: RTypeInstruction):
        first_register_value = cpu.regs[instructions.rs1].read()
        second_register_value = cpu.regs[instructions.rs2].read()

        result = cpu.alu.mul(first_register_value, second_register_value)
        cpu.regs[instructions.rd].write(result)

    @staticmethod
    def DIV(cpu: CPU, instructions: RTypeInstruction):
        first_register_value = cpu.regs[instructions.rs1].read()
        second_register_value = cpu.regs[instructions.rs2].read()

        result = cpu.alu.div(first_register_value, second_register_value)
        cpu.regs[instructions.rd].write(result)

    @staticmethod
    def DIVU(cpu: CPU, instructions: RTypeInstruction):
        first_register_value = cpu.regs[instructions.rs1].read()
        second_register_value = cpu.regs[instructions.rs2].read()

        result = cpu.alu.divu(first_register_value, second_register_value)
        cpu.regs[instructions.rd].write(result)

    @staticmethod
    def PUSH(cpu: CPU, instructions: RTypeInstruction):
        cpu.sp.step()

        cpu.memory.write(cpu.sp.read(), cpu.regs[instructions.rs1].read())

    @staticmethod
    def POP(cpu: CPU, instructions: RTypeInstruction):
        cpu.regs[instructions.rd].write(cpu.memory.read(cpu.sp.read()))

        cpu.sp.back()

    @staticmethod
    def RDSP(cpu: CPU, instructions: RTypeInstruction):
        cpu.regs[instructions.rd].write(cpu.sp.read())

    @staticmethod
    def WRSP(cpu: CPU, instructions: RTypeInstruction):
        cpu.sp.set(cpu.regs[instructions.rs1].read())

    @staticmethod
    def REM(cpu: CPU, instructions: RTypeInstruction):
        first_register_value = cpu.regs[instructions.rs1].read()
        second_register_value = cpu.regs[instructions.rs2].read()
        remainder = cpu.alu.rem(first_register_value, second_register_value)
        
        cpu.regs[instructions.rd].write(remainder)

    @staticmethod
    def REMU(cpu: CPU, instructions: RTypeInstruction):
        first_register_value = cpu.regs[instructions.rs1].read()
        second_register_value = cpu.regs[instructions.rs2].read()
        reminder = cpu.alu.remu(first_register_value, second_register_value)
        
        cpu.regs[instructions.rd].write(reminder)

    @staticmethod
    def RDPC(cpu: CPU, instructions: RTypeInstruction):
        cpu.regs[instructions.rd].write((cpu.pc.read() - 1) & 0xFFFF)

def _sign_extend(value: int, width: int) -> int:
    mask = 1 << (width - 1)
    return (value ^ mask) - mask

class ITypeExecutions:
    @staticmethod
    def ADDI(cpu: CPU, instructions: ITypeInstruction):
        value = cpu.regs[instructions.rs1].read()
        imm = _sign_extend(instructions.imm, 4)
        cpu.regs[instructions.rd].write(cpu.alu.add(value, imm))

    @staticmethod
    def ANDI(cpu: CPU, instructions: ITypeInstruction):
        value = cpu.regs[instructions.rs1].read()
        cpu.regs[instructions.rd].write(cpu.alu.and_(value, instructions.imm))  # zero-extended

    @staticmethod
    def ORI(cpu: CPU, instructions: ITypeInstruction):
        value = cpu.regs[instructions.rs1].read()
        cpu.regs[instructions.rd].write(cpu.alu.or_(value, instructions.imm))  # zero-extended

    @staticmethod
    def XORI(cpu: CPU, instructions: ITypeInstruction):
        value = cpu.regs[instructions.rs1].read()
        cpu.regs[instructions.rd].write(cpu.alu.xor_(value, instructions.imm))  # zero-extended

    @staticmethod
    def SHLI(cpu: CPU, instructions: ITypeInstruction):
        value = cpu.regs[instructions.rs1].read()
        cpu.regs[instructions.rd].write(cpu.alu.shl(value, instructions.imm))

    @staticmethod
    def SHRI(cpu: CPU, instructions: ITypeInstruction):
        value = cpu.regs[instructions.rs1].read()
        cpu.regs[instructions.rd].write(cpu.alu.shr(value, instructions.imm))

    @staticmethod
    def SHRIU(cpu: CPU, instructions: ITypeInstruction):
        value = cpu.regs[instructions.rs1].read()
        cpu.regs[instructions.rd].write(cpu.alu.shru(value, instructions.imm))

    @staticmethod
    def LOAD(cpu: CPU, instructions: ITypeInstruction):
        base_register = 7 if instructions.rs1 == 1 else 6
        base_value = cpu.regs[base_register].read()
        offset = _sign_extend(instructions.imm, 6)
        address = (base_value + offset) & 0xFFFF
        cpu.regs[instructions.rd].write(cpu.memory.read(address))

    @staticmethod
    def STORE(cpu: CPU, instructions: ITypeInstruction):
        base_register = 7 if instructions.rs1 == 1 else 6
        base_value = cpu.regs[base_register].read()
        offset = _sign_extend(instructions.imm, 6)
        address = (base_value + offset) & 0xFFFF
        value_to_store = cpu.regs[instructions.rd].read()
        cpu.memory.write(address, value_to_store)

    @staticmethod
    def CMPI(cpu: CPU, instructions: ITypeInstruction):
        value = cpu.regs[instructions.rs1].read()
        imm = _sign_extend(instructions.imm, 4)
        flags_list = cpu.alu.cmp_flags(value, imm)
        cpu.flags.set_list(flags_list)

def _branch_if(cpu: CPU, instructions: BTypeInstruction, condition: bool):
    if condition:
        offset = _sign_extend(instructions.offset, 11)
        cpu.pc.set((cpu.pc.read() + offset) & 0xFFFF)

class BTypeExecutions:
    @staticmethod
    def BEQ(cpu: CPU, instructions: BTypeInstruction):
        _branch_if(cpu, instructions, cpu.flags.read_z())

    @staticmethod
    def BNE(cpu: CPU, instructions: BTypeInstruction):
        _branch_if(cpu, instructions, not cpu.flags.read_z())

    @staticmethod
    def BLT(cpu: CPU, instructions: BTypeInstruction):
        _branch_if(cpu, instructions, cpu.flags.read_n() != cpu.flags.read_v())

    @staticmethod
    def BGE(cpu: CPU, instructions: BTypeInstruction):
        _branch_if(cpu, instructions, cpu.flags.read_n() == cpu.flags.read_v())

    @staticmethod
    def BLTU(cpu: CPU, instructions: BTypeInstruction):
        _branch_if(cpu, instructions, not cpu.flags.read_c())

    @staticmethod
    def BGEU(cpu: CPU, instructions: BTypeInstruction):
        _branch_if(cpu, instructions, cpu.flags.read_c())

class JTypeExecutions:
    @staticmethod
    def JMP(cpu: CPU, instructions: JTypeInstruction):
        offset = _sign_extend(instructions.offset, 10)
        cpu.pc.step_by(offset)

    @staticmethod
    def JMPA(cpu: CPU, instructions: JTypeInstruction):
        register_index = instructions.offset & 0b111
        cpu.pc.set(cpu.regs[register_index].read())

    @staticmethod
    def CALL(cpu: CPU, instructions: JTypeInstruction):
        cpu.sp.step()  # SP -= 1
        cpu.memory.write(cpu.sp.read(), cpu.pc.read())  # push return address (already-incremented PC)
        offset = _sign_extend(instructions.offset, 10)
        cpu.pc.step_by(offset)

    @staticmethod
    def CALLA(cpu: CPU, instructions: JTypeInstruction):
        cpu.sp.step()
        cpu.memory.write(cpu.sp.read(), cpu.pc.read())
        register_index = instructions.offset & 0b111
        cpu.pc.set(cpu.regs[register_index].read())

    @staticmethod
    def RET(cpu: CPU, instructions: JTypeInstruction):
        cpu.pc.set(cpu.memory.read(cpu.sp.read()))
        cpu.sp.back()  # SP += 1 — this is stack_pointer.back(), correct; unrelated to program_counter's broken one above

    @staticmethod
    def HALT(cpu: CPU, instructions: JTypeInstruction):
        os._exit(0)

    @staticmethod
    def NOP(cpu: CPU, instructions: JTypeInstruction):
        pass
