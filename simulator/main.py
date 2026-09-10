from cpu_architecture.cpu import CPU
from io_devices.std import *
from collections import deque
from threading import Event, Thread
import time

io_buffer: deque[int] = deque()
running = Event()
running.set()

cpu = CPU()

Thread(target=io_function_write_prompt, args=(io_buffer, running), daemon=True).start()
Thread(target=io_function_write_drain, args=(cpu.memory, io_buffer, running), daemon=True).start()
Thread(target=io_function_read, args=(cpu.memory, running), daemon=True).start()

program = [
    0x4013,  # ADDI R0, R1, 3    -> R0 = 3                      (the value to output)
    0x4111,  # ADDI R2, R1, 1    -> R2 = 1                      (the readiness flag value)
    0x439C,  # ADDI R7, R1, -4   -> R7 = 0xFFFC                 (base address, OUT_READY)
    0x6041,  # STORE R0, R7, 1   -> mem[0xFFFD] = 3             (OUT_DATA)
    0x6140,  # STORE R2, R7, 0   -> mem[0xFFFC] = 1             (OUT_READY)
    0xFC00,  # HALT
]

cpu.start(program)

while True:
    cpu.step() 
    time.sleep(0.5)