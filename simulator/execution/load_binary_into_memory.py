from __future__ import annotations

import re
import struct
import zlib


class LoadedBinary:
    def __init__(
        self, memory_destination: int, pc_starting_value: int, data: list[int]
    ) -> None:
        self.memory_destination = memory_destination
        self.pc_starting_value = pc_starting_value
        self.data = data


def load_binary_file(path: str = "./program.bingus") -> bytes:
    """
    Reads a hex-encoded file, parses the CPU1 header, and verifies the CRC-32 checksum.
    Returns the verified raw binary data.
    """
    with open(path, "r") as file:
        content = file.read()

    # Clean out whitespace, newlines, or optional "0x" prefixes
    cleaned_content = re.sub(r"[\s,]|0x", "", content)
    binary_data = bytes.fromhex(cleaned_content)

    if len(binary_data) < 16:
        raise ValueError("File too short to contain a valid CPU1 header.")

    if binary_data[:4] != b"CPU1":
        raise ValueError("Invalid file format: Magic number mismatch.")

    # Extract Big-Endian CRC-32 stored in header at bytes 12..15
    expected_crc = struct.unpack(">I", binary_data[12:16])[0]

    # CRC itself is excluded from CRC calculations
    bytes_to_check = binary_data[:12] + binary_data[16:]
    actual_crc = zlib.crc32(bytes_to_check) & 0xFFFFFFFF

    # Validate Checksum
    if actual_crc != expected_crc:
        raise ValueError(
            f"CRC-32 Checksum Corrupted! File expected {hex(expected_crc)}, got {hex(actual_crc)}"
        )

    return binary_data


def parse_program_binary_data(binary_data: bytes) -> LoadedBinary:
    version = binary_data[4]
    if version != 1:
        raise ValueError(f"Version {version} not supported.")

    rest_of_header_size = binary_data[5]
    payload_start_offset = 6 + rest_of_header_size

    memory_destination = struct.unpack(">H", binary_data[6:8])[0]
    pc_starting_value = struct.unpack(">H", binary_data[8:10])[0]

    payload = binary_data[payload_start_offset:]

    # Convert 8-bit bytes into 16-bit Big-Endian CPU instructions
    code_words = [
        struct.unpack(">H", payload[i : i + 2])[0] for i in range(0, len(payload), 2)
    ]

    return LoadedBinary(
        memory_destination=memory_destination,
        pc_starting_value=pc_starting_value,
        data=code_words,
    )
