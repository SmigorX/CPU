class memory:
    SIZE = 0x10000  # 65,536 words

    def __init__(self):
        self.cells = [0] * self.SIZE

    def read(self, address: int) -> int:
        return self.cells[address & 0xFFFF]

    def write(self, address: int, value: int):
        self.cells[address & 0xFFFF] = value & 0xFFFF

    def load_program(self, words: list[int], start: int = 0):
        for offset, word in enumerate(words):
            self.write(start + offset, word)
