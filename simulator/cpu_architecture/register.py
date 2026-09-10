class cpu_register():
    def __init__(self):
        self.value = 0

    def write(self, new_value: int):
        self.value = new_value & 0xFFFF

    def read(self):
        return self.value

class flags_register():
    def __init__(self):
        self.z = False
        self.c = False
        self.n = False
        self.v = False

    def set(self, z: bool, c: bool, n: bool, v: bool):
        self.z, self.c, self.n, self.v = z, c, n, v

class program_counter():
    def __init__(self):
        self.value = 0x0000

    def step(self):
        self.value = (self.value + 1) & 0xFFFF

    def set(self, new_value: int):
        self.value = new_value & 0xFFFF

    def read(self):
        return self.value & 0xFFFF

class stack_pointer():
    def __init__(self):
        self.value = 0xFFFB # Leaves space for IO at the top of the memory

    def step(self):
        self.value = (self.value - 1) & 0xFFFF

    def back(self):
        self.value = (self.value + 1) & 0xFFFF

    def step_by(self, value: int):
        self.value = (self.value - value) & 0xFFFF

    def back_by(self, value: int):
        self.value = (self.value + value) & 0xFFFF

    def set(self, value: int):
        self.value = value & 0xFFFF

    def read(self):
        return self.value & 0xFFFF
