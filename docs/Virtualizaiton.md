# CPU Simulator
- ### Python

# External comunication
Second thread that allows to put in and pull out data outside of the simulation connecting to the CPU via buffers in the memory address space. We first do the operation on data register, and then set/reset the flag to prevent race conditions
- `0xFFFF` - `IN_READY` - I/O sets to one to indicate new input, CPU clears it after read
- `0xFFFE` - `IN_DATA` - I/O writes the data to here
- `0xFFFD` - `OUT_READY` - CPU sets this to one to indicate new output, I/O clears after read
- `0xFFFC` - `OUT_DATA` - CPU write the data to here
