from cpu_architecture.register import cpu_register, flags_register, program_counter, stack_pointer
from cpu_architecture.memory import memory

class CPU():
    def __init__(self):
        self.regs = [cpu_register() for _ in range(8)]
        self.flags = flags_register()
        self.pc = program_counter()
        self.sp = stack_pointer()
        self.memory = memory()

    def start(self, program: list[int], entry: int = 0x0000):
        self.memory.load_program(program, entry)
        self.pc.set(entry)



