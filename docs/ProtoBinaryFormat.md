We use big-endian

| Offset | Size [bytes]      | Filed                                          |
|--------|-------------------|------------------------------------------------|
| 0      | 4                 | Magic Number "CPU1"                            |
| 4      | 1                 | Format Version                                 |
| 5      | 1                 | Size of the rest of the header in no. of bytes |
| 6      | 2                 | Memory destination address 0x0000 by default   |
| 8      | 2                 | Starting value of PC                           |
| 10     | 2                 | -- Reserved -- future flags etc                |
| 12     | 4                 | CRC-32                                         |
| derived from header size    | 2x(code + static)   | Code words then data up to EOF                 |
