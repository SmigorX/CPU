# I/O — External communication

Two separate python threads let data flow in and out of the common memory to let simulated program and python program interchange data. Python threads write to the virtual memory, simulated program uses LOAD/STORE to interact with its special I/O memory region on top of the stack. Race condition shouldn't be a problem since both sides first write value and then when finished set flag in the next register, the other side is the one that clears the flag so values aren't lost. Also the python global interpreter lock.

## Address layout

| Address | Name | Set by | Cleared by | Purpose |
| --- | --- | --- | --- | --- |
| `0xFFFF` | `IN_DATA` | I/O thread | — | CPU's **reading space** — I/O thread writes incoming data here before raising `IN_READY` |
| `0xFFFE` | `IN_READY` | I/O thread | CPU | CPU's **reading ready bit** — set to 1 when new input is waiting in `IN_DATA` |
| `0xFFFD` | `OUT_DATA` | CPU | — | CPU's **writing space** — CPU writes outgoing data here before raising `OUT_READY` |
| `0xFFFC` | `OUT_READY` | CPU | I/O thread | CPU's **writing ready bit** — set to 1 when new output is waiting in `OUT_DATA` |

This sits directly above the stack's initial position (`SP` starts at `0xFFFB`), so ordinary stack growth never collides with these four cells as long as a program doesn't push further than the available space allows.
