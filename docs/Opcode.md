# Format

| Class bits | Format | Layout (MSB→LSB, 16 bits total) |
| --- | --- | --- |
| `00` | R-type | `class(2)` `subop(5)` `rd(3)` `rs1(3)` `rs2(3)` |
| `01` | I-type | `class(2)` `subop(4)` `rd(3)` `rs1(3)` `imm(4)` |
| `10` | B-type | `class(2)` `subop(3)` `offset(11)` |
| `11` | J-type | `class(2)` `subop(4)` `offset(10)` |

`LOAD`/`STORE` sub-format (overrides the standard I-type layout above): `class(2)` `subop(4)` `rd(3)` `rs1(1)` `imm(6)` — `rs1` narrowed to 1 bit (`R6` or `R7` only, the two conventional address registers), freeing 2 bits to widen `imm` to 6 bits (−32..31 instead of −8..7). **Bit mapping: `0 = R6`, `1 = R7`.**

`JMPA`/`CALLA` sub-format (overrides the standard J-type layout above): the 10-bit `offset` field is reinterpreted as a register operand — `rs1` occupies the low 3 bits (bits 2-0), the upper 7 bits are unused.

# Draft

### R-type (`class = 00`) Register instructions

Only `CMP` writes to `FLAGS` in this table — no other instruction does, despite computing a result.

| subop | Mnemonic | Operands | Semantics |
| --- | --- | --- | --- |
| 00000 | `ADD` | rd, rs1, rs2 | rd = rs1 + rs2 |
| 00001 | `SUB` | rd, rs1, rs2 | rd = rs1 − rs2 |
| 00010 | `AND` | rd, rs1, rs2 | rd = rs1 & rs2 |
| 00011 | `OR` | rd, rs1, rs2 | rd = rs1 \| rs2 |
| 00100 | `XOR` | rd, rs1, rs2 | rd = rs1 ^ rs2 |
| 00101 | `NOT` | rd, rs1 | rd = ~rs1 (rs2 ignored) |
| 00110 | `SHL` | rd, rs1, rs2 | rd = rs1 << rs2 |
| 00111 | `SHR` | rd, rs1, rs2 | rd = rs1 >> rs2 (arithmetic — sign-extends, for signed values) |
| 01000 | `SHRU` | rd, rs1, rs2 | rd = rs1 >> rs2 (logical — zero-fills, for unsigned values) |
| 01001 | `MOV` | rd, rs1 | rd = rs1 (rs2 ignored) |
| 01010 | `CMP` | rs1, rs2 | flags = rs1 − rs2, result discarded |
| 01011 | `MUL` | rd, rs1, rs2 | rd = low 16 bits of rs1 × rs2 (no signed/unsigned variant needed — identical bits either way, same as `ADD`/`SUB`) |
| 01100 | `DIV` | rd, rs1, rs2 | rd = rs1 / rs2, signed, truncates toward zero |
| 01101 | `DIVU` | rd, rs1, rs2 | rd = rs1 / rs2, unsigned |
| 01110 | `PUSH` | rs1 | SP -= 1; mem[SP] = rs1 |
| 01111 | `POP` | rd | rd = mem[SP]; SP += 1 |
| 10000 | `RDSP` | rd | rd = SP |
| 10001 | `WRSP` | rs1 | SP = rs1 |
| 10010 | `REM` | rd, rs1, rs2 | rd = rs1 % rs2, signed |
| 10011 | `REMU` | rd, rs1, rs2 | rd = rs1 % rs2, unsigned |
| 10100 | `RDPC` | rd | rd = PC (address of this `RDPC` instruction itself) |
| others | — | | reserved |

### I-type (`class = 01`) Immedate instructions

Only `CMPI` writes to `FLAGS` in this table — `ADDI`/`ANDI`/`ORI`/`XORI`/`SHLI`/`SHRI`/`SHRIU`/`LOAD`/`STORE` do not.

**`imm` is interpreted as signed or unsigned depending on the instruction** — it's only 4 (or 6) bits and has to be widened to 16 before use. Arithmetic values (`ADDI`/`CMPI`/`LOAD`/`STORE`) treat `imm` as **signed**. Raw bit patterns (`ANDI`/`ORI`/`XORI`) and shift counts (`SHLI`/`SHRI`/`SHRIU`) treat it as **unsigned**. This is separate from the shift *result's* fill behavior (arithmetic vs. logical).

| subop | Mnemonic | Operands | Semantics |
| --- | --- | --- | --- |
| 0000 | `ADDI` | rd, rs1, imm | rd = rs1 + imm (`imm` signed) |
| 0001 | `ANDI` | rd, rs1, imm | rd = rs1 & imm (`imm` unsigned — a raw bit pattern) |
| 0010 | `ORI` | rd, rs1, imm | rd = rs1 \| imm (`imm` unsigned) |
| 0011 | `XORI` | rd, rs1, imm | rd = rs1 ^ imm (`imm` unsigned) |
| 0100 | `SHLI` | rd, rs1, imm | rd = rs1 << imm (`imm` unsigned — a raw 0–15 shift count) |
| 0101 | `SHRI` | rd, rs1, imm | rd = rs1 >> imm, **arithmetic** result (sign-extends, per `rs1`'s sign bit). `imm` itself is unsigned — a raw 0–15 shift count. |
| 0110 | `SHRIU` | rd, rs1, imm | rd = rs1 >> imm, **logical** result (zero-fills). `imm` itself is unsigned — a raw 0–15 shift count. |
| 0111 | `LOAD` | rd, rs1, imm | rd = mem[rs1 + imm] (`imm` signed). rs1 ∈ {R6, R7} only (1 bit), imm is 6 bits. |
| 1000 | `STORE` | rd, rs1, imm | mem[rs1 + imm] = rd (rd field reused as source reg here) (`imm` signed). rs1 ∈ {R6, R7} only (1 bit), imm is 6 bits. |
| 1001 | `CMPI` | rs1, imm | flags = rs1 − imm (`imm` signed) |
| others | — | | reserved |

### B-type (`class = 10`) — conditional branch, `PC += offset` if condition true

- Z - result is 0
- N - result is <0
- C - carry bit
- V - overflow into sign bit for signed values

| subop | Mnemonic | Operands | Condition | Relation (rs1 vs rs2, from the preceding `CMP`/`CMPI`) | Semantics |
| --- | --- | --- | --- | --- | --- |
| 000 | `BEQ` | offset | Z == 1 | rs1 == rs2 | if Z == 1: PC += offset |
| 001 | `BNE` | offset | Z == 0 | rs1 ≠ rs2 | if Z == 0: PC += offset |
| 010 | `BLT` | offset | N != V | rs1 < rs2 (signed) | if N != V: PC += offset |
| 011 | `BGE` | offset | N == V | rs1 ≥ rs2 (signed) | if N == V: PC += offset |
| 100 | `BLTU` | offset | C == 0 | rs1 < rs2 (unsigned) | if C == 0: PC += offset |
| 101 | `BGEU` | offset | C == 1 | rs1 ≥ rs2 (unsigned) | if C == 1: PC += offset |
| others | — | | | | reserved |

### J-type (`class = 11`) — unconditional, `offset` used as PC-relative target

`JMPA`/`CALLA` reinterpret the 10-bit `offset` field as a register operand instead: `rs1` occupies the low 3 bits (bits 2-0), the upper 7 bits are unused.

| subop | Mnemonic | Operands | Semantics |
| --- | --- | --- | --- |
| 0000 | `JMP` | offset | PC += offset |
| 0001 | `JMPA` | rs1 | PC = rs1 |
| 0010 | `CALL` | offset | SP -= 1; mem[SP] = PC; PC += offset |
| 0011 | `CALLA` | rs1 | SP -= 1; mem[SP] = PC; PC = rs1 |
| 0100 | `RET` | — | PC = mem[SP]; SP += 1 |
| 1111 | `HALT` | — | Stop execution |
| 1110 | `NOP` | — | No-op |
| others | — | | reserved |
