from execution.execute import Dispatcher
from execution.load_binary_into_memory import LoadedBinary

from cpu_architecture.alu import ALU
from cpu_architecture.memory import memory
from cpu_architecture.register import (
    cpu_register,
    flags_register,
    program_counter,
    stack_pointer,
)


class CPU:
    def __init__(self):
        self.regs = [cpu_register() for _ in range(8)]
        self.flags = flags_register()
        self.pc = program_counter()
        self.sp = stack_pointer()
        self.memory = memory()
        self.alu = ALU
        self.dispatcher = Dispatcher

    def start(
        self, program: list[int], program_entry: int = 0x0000, stack_start: int = 0xFFFB
    ):
        self.memory.load_program(program, program_entry)
        self.pc.set(program_entry)
        self.sp.set(stack_start)

    def step(self):
        instr_addr = self.pc.read()
        raw = self.memory.read(instr_addr)
        self.pc.step()
        self.dispatcher.execute_instruction(self, raw)

    def load_binary_data_to_memory(self, data: LoadedBinary):
        self.memory.load_program(data.data, data.memory_destination)
        self.pc.set(data.pc_starting_value)
