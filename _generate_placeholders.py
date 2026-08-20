"""Stdlib-only: PNG icons, PNG gallery images, silent MP3 stubs."""
from __future__ import annotations

import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent

SILENT_MP3 = bytes.fromhex(
    "fff340c400000000000000000000000000000000000000000000000000000000"
    "0000000000000000000000000000000000000000000000000000000000000000"
)


def write_png(path: Path, width: int, height: int, rgb: tuple[int, int, int]) -> None:
    r, g, b = rgb
    raw = b"".join(b"\x00" + bytes([r, g, b]) * width for _ in range(height))

    def chunk(tag: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )


def main() -> None:
    write_png(ROOT / "icons" / "icon-192.png", 192, 192, (139, 69, 19))
    write_png(ROOT / "icons" / "icon-512.png", 512, 512, (139, 69, 19))

    palette = [
        (139, 69, 19),
        (160, 82, 45),
        (101, 67, 33),
        (205, 133, 63),
        (210, 180, 140),
        (128, 70, 40),
        (150, 100, 60),
        (90, 50, 30),
        (180, 120, 70),
        (120, 80, 50),
    ]

    for i in range(1, 11):
        folder = ROOT / "media" / f"item-{i:03d}"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "audio-mr.mp3").write_bytes(SILENT_MP3)
        (folder / "audio-en.mp3").write_bytes(SILENT_MP3)
        base = palette[i - 1]
        for n, delta in ((1, 0), (2, 25), (3, -20)):
            rgb = (
                max(0, min(255, base[0] + delta)),
                max(0, min(255, base[1] + delta)),
                max(0, min(255, base[2] + delta)),
            )
            # Placeholder images as PNG (replace later with real WebP photos)
            write_png(folder / f"{n:02d}.png", 640, 480, rgb)

    print("OK")


if __name__ == "__main__":
    main()
