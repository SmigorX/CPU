# =======================================================
# A second thread that interacts with simulation memory
# to give it I/O capabilities
# =======================================================
import time
from collections import deque
from threading import Event

from cpu_architecture.memory import memory


def io_function_write_prompt(buffer: deque[int], running: Event):
    while running.is_set():
        user_input = input("Send letter to CPU (a-Z): ")

        if len(user_input) == 1 and "A" <= user_input.upper() <= "Z":
            value = ord(user_input.upper()) - 65
        else:
            try:
                value = int(user_input) & 0xFFFF
            except ValueError:
                print("Not a number or a single letter A-Z, try again.")
                continue

        buffer.append(value)


def io_function_write_drain(memory: memory, buffer: deque[int], running: Event):
    while running.is_set():
        if buffer and not memory.read(0xFFFE):
            value_to_send = buffer.popleft()
            memory.write(0xFFFF, value_to_send)
            memory.write(0xFFFE, 1)
        time.sleep(0.001)


def io_function_read(memory: memory, running: Event):
    while running.is_set():
        if memory.read(0xFFFC):
            print(
                "\n Message from CPU: " + chr(memory.read(0xFFFD) + 65) + "\n",
                end="",
                flush=True,
            )
            memory.write(0xFFFC, 0)
        time.sleep(0.001)
