# Registers

## R0–R7 (general-purpose)

| Register | GPR? | Additional / conventional role |
|---|---|---|
| `R0` | Yes | Conventionally holds function-call argument 1 (first of up to 3 register-passed args), and also the function's **return value** — reused once the argument is no longer needed by the time the function returns |
| `R1` | Yes | Conventionally holds function-call argument 2 |
| `R2` | Yes | Conventionally holds function-call argument 3 |
| `R3` | Yes | None |
| `R4` | Yes | None |
| `R5` | Yes | None |
| `R6` | Yes | Hardware-restricted: one of only two registers (`R6`/`R7`) selectable as the base address register for `LOAD`/`STORE` (their `rs1` field is only 1 bit for these two ops). Also conventionally the general scratch/temporary register (`tmp`). |
| `R7` | Yes | Same hardware restriction as `R6` (base-address pair for `LOAD`/`STORE`). Additionally serves as `FP` (frame pointer) by **software convention** — the compiler always treats it this way when addressing locals/params in a stack frame. The hardware itself has no idea `R7` is special; nothing enforces this except discipline. |

None of `R0`–`R7` are hardwired to a fixed value — no zero register, no built-in ±1 constants (decided early on: use `ADDI` against any register instead of dedicating registers to constants).

## PC, SP, FLAGS (not GPRs)

These are separate dedicated registers — none are addressable through the 3-bit register fields that select `R0`–`R7`.

| Register | Role |
|---|---|
| `PC` | Address of the next instruction. Only changed by branch/jump/call — never writable by ordinary ALU/`MOV` instructions. |
| `SP` | Top of the stack. Moves automatically via `PUSH`/`POP`/`CALL`/`RET`; bridged to the GPR file explicitly via `RDSP`/`WRSP` when a computed value (e.g. reserving space for locals in a prologue) needs to reach it. |
| `FLAGS` | `Z`/`C`/`N`/`V` — zero, carry, negative, overflow. **Only `CMP`/`CMPI` write to it** — no other instruction does, even ones that compute an ALU result. Read by conditional branches (`BEQ`/`BLT`/etc.). |

## Still open

Nothing outstanding at the moment.