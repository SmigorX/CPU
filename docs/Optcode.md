# Format
| Class bits | Format | Layout (MSB→LSB, 16 bits total) |
|---|---|---|
| `00` | R-type | `class(2)` `subop(5)` `rd(3)` `rs1(3)` `rs2(3)` |
| `01` | I-type | `class(2)` `subop(4)` `rd(3)` `rs1(3)` `imm(4)` |
| `10` | B-type | `class(2)` `subop(4)` `cc(3)` `offset(7)` |
| `11` | J-type | `class(2)` `subop(4)` `offset(10)` |

`LOAD`/`STORE` sub-format (overrides the standard I-type layout above): `class(2)` `subop(4)` `rd(3)` `rs1(1)` `imm(6)` — `rs1` narrowed to 1 bit (`R6` or `R7` only, the two conventional address registers), freeing 2 bits to widen `imm` to 6 bits (−32..31 instead of −8..7).

# Draft
### R-type (`class = 00`) Register instructions

Only `CMP` writes to `FLAGS` in this table — no other instruction does, despite computing a result.

| subop | Mnemonic | Operands | Semantics |
|---|---|---|---|
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

| subop | Mnemonic | Operands | Semantics |
|---|---|---|---|
| 0000 | `ADDI` | rd, rs1, imm | rd = rs1 + imm |
| 0001 | `ANDI` | rd, rs1, imm | rd = rs1 & imm |
| 0010 | `ORI` | rd, rs1, imm | rd = rs1 \| imm |
| 0011 | `XORI` | rd, rs1, imm | rd = rs1 ^ imm |
| 0100 | `SHLI` | rd, rs1, imm | rd = rs1 << imm |
| 0101 | `SHRI` | rd, rs1, imm | rd = rs1 >> imm (arithmetic — sign-extends, for signed values) |
| 0110 | `SHRIU` | rd, rs1, imm | rd = rs1 >> imm (logical — zero-fills, for unsigned values) |
| 0111 | `LOAD` | rd, rs1, imm | rd = mem[rs1 + imm]. rs1 ∈ {R6, R7} only (1 bit), imm is 6 bits. |
| 1000 | `STORE` | rd, rs1, imm | mem[rs1 + imm] = rd (rd field reused as source reg here). rs1 ∈ {R6, R7} only (1 bit), imm is 6 bits. |
| 1001 | `CMPI` | rs1, imm | flags = rs1 − imm |
| others | — | | reserved |

### B-type (`class = 10`) — conditional branch, `PC += offset` if condition true
 - Z - result is 0
 - N - result is <0
 - C - carry bit
 - V - overflow into sign bit for signed values

| subop (cc) | Mnemonic | Operands | Condition | Relation (rs1 vs rs2, from the preceding `CMP`/`CMPI`) | Semantics |
|---|---|---|---|---|---|
| 000 | `BEQ` | offset | Z == 1 | rs1 == rs2 | if Z == 1: PC += offset |
| 001 | `BNE` | offset | Z == 0 | rs1 ≠ rs2 | if Z == 0: PC += offset |
| 010 | `BLT` | offset | N != V | rs1 < rs2 (signed) | if N != V: PC += offset |
| 011 | `BGE` | offset | N == V | rs1 ≥ rs2 (signed) | if N == V: PC += offset |
| 100 | `BLTU` | offset | C == 0 | rs1 < rs2 (unsigned) | if C == 0: PC += offset |
| 101 | `BGEU` | offset | C == 1 | rs1 ≥ rs2 (unsigned) | if C == 1: PC += offset |
| others | — | | | | reserved |

### J-type (`class = 11`) — unconditional, `offset` used as PC-relative target
| subop | Mnemonic | Operands | Semantics |
|---|---|---|---|
| 0000 | `JMP` | offset | PC += offset |
| 0001 | `JMPA` | rs1 | PC = rs1 |
| 0010 | `CALL` | offset | SP -= 1; mem[SP] = PC+1; PC += offset |
| 0011 | `CALLA` | rs1 | SP -= 1; mem[SP] = PC+1; PC = rs1 |
| 0100 | `RET` | — | PC = mem[SP]; SP += 1 |
| 1111 | `HALT` | — | Stop execution |
| 1110 | `NOP` | — | No-op |
| others | — | | reserved |