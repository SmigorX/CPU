import time
from collections import deque
from threading import Event, Thread

from cpu_architecture.cpu import CPU
from execution.load_binary_into_memory import LoadedBinary, load_binary_file, parse_program_binary_data
from io_devices.std import *

io_buffer: deque[int] = deque()
running = Event()
running.set()

cpu = CPU()

Thread(target=io_function_write_prompt, args=(io_buffer, running), daemon=True).start()
Thread(
    target=io_function_write_drain, args=(cpu.memory, io_buffer, running), daemon=True
).start()
Thread(target=io_function_read, args=(cpu.memory, running), daemon=True).start()

# program = [
#     0x431C,  # ADDI R6, R1, -4      -> R6 = 0xFFFC (I/O base address; R1 stays 0 all program)
#     0x5C02,  # LOAD R0, R6, 2       -> R0 = IN_READY                    [loop start, address 1]
#     0x6400,  # CMPI R0, 0           -> flags = R0 - 0
#     0x87FD,  # BEQ -3               -> if IN_READY == 0: loop back to address 1
#     0x5D03,  # LOAD R2, R6, 3       -> R2 = IN_DATA
#     0x6101,  # STORE R2, R6, 1      -> OUT_DATA = R2
#     0x4321,  # ADDI R3, R1, 1       -> R3 = 1
#     0x6180,  # STORE R3, R6, 0      -> OUT_READY = 1
#     0x6082,  # STORE R1, R6, 2      -> IN_READY = 0 (consumer clears it)
#     0xC3F7,  # JMP -9               -> back to address 1
# ]

# cpu.start(program)
binary_data = load_binary_file()
parsed_binary = parse_program_binary_data(binary_data)
cpu.load_binary_data_to_memory(parsed_binary)

while True:
    cpu.step()
    time.sleep(0.01)
