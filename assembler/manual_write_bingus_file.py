import struct
import zlib

def build_bingus_file(
    instructions: list[int],
    load_address: int = 0x0000,
    pc_entry: int = 0x0000,
    version: int = 1
) -> bytes:
    # 1. Convert 16-bit instruction integers to Big-Endian payload bytes
    payload = b"".join(struct.pack(">H", word & 0xFFFF) for word in instructions)

    # 2. Pack initial header fields (0..11)
    # Format: Magic (4s), Version (B), RestHeaderLen (B), MemDest (H), PC (H), Reserved (H)
    header_part1 = struct.pack(
        ">4sBBHHH",
        b"CPU1",
        version,
        10,  # Rest of header length (bytes 6..15)
        load_address,
        pc_entry,
        0x0000
    )

    # 3. Compute CRC-32 across Header Part 1 + Payload
    crc = zlib.crc32(header_part1 + payload) & 0xFFFFFFFF

    # 4. Assemble complete binary
    full_binary = header_part1 + struct.pack(">I", crc) + payload
    return full_binary


program = [
    0x431C, 0x5C02, 0x6400, 0x87FD, 0x5D03,
    0x6101, 0x4191, 0x6180, 0x6082, 0xC3F7
]

binary_data = build_bingus_file(program)

# Save to file in hex format
with open("program.bingus", "w") as f:
    f.write(binary_data.hex())