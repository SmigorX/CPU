class cpu_register:
    def __init__(self):
        self.value = 0

    def write(self, new_value: int):
        self.value = new_value & 0xFFFF

    def read(self):
        return self.value


class flags_register:
    def __init__(self):
        self.z = False
        self.c = False
        self.n = False
        self.v = False

    def set(self, z: bool, c: bool, n: bool, v: bool):
        """
        If you want to pass a `tuple[bool, bool, bool, bool]` use the `set_list` wrapper.
        """
        self.z, self.c, self.n, self.v = z, c, n, v

    def set_list(self, flag_vecor: tuple[bool, bool, bool, bool]):
        self.set(flag_vecor[0], flag_vecor[1], flag_vecor[2], flag_vecor[3])

    def read_z(self) -> bool:
        return self.z

    def read_c(self) -> bool:
        return self.c

    def read_n(self) -> bool:
        return self.n

    def read_v(self) -> bool:
        return self.v

    def read_all(self) -> tuple[bool, bool, bool, bool]:
        """
        returns z, c, n, v
        """
        return (self.z, self.c, self.n, self.v)


class program_counter:
    def __init__(self, start: int = 0x0000):
        self.value = start

    def step(self):
        self.value = (self.value + 1) & 0xFFFF

    def step_by(self, value: int):
        self.value = (self.value + value) & 0xFFFF

    def set(self, new_value: int):
        self.value = new_value & 0xFFFF

    def read(self):
        return self.value & 0xFFFF

    def back(self):
        self.value = (self.value - 1) & 0xFFFF

    def back_by(self, value: int):
        self.value = (self.value - value) & 0xFFFF


class stack_pointer:
    def __init__(
        self, start: int = 0xFFFB
    ):  # Leaves space for IO at the top of the memory
        self.value = start

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
