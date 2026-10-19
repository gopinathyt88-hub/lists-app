import zlib, struct
COLORS = [(255,90,95),(255,159,28),(255,217,61),(46,196,182)]
def inside(x, y, x0, y0, x1, y1, r):
    if x < x0 or x > x1 or y < y0 or y > y1: return False
    cx = min(max(x, x0 + r), x1 - r)
    cy = min(max(y, y0 + r), y1 - r)
    return (x - cx) ** 2 + (y - cy) ** 2 <= r * r
def make(size, name):
    rows = []
    for py in range(size):
        row = bytearray([0])
        y = py / size
        for px in range(size):
            x = px / size
            c = (0, 0, 0)
            for i, col in enumerate(COLORS):
                top = 0.20 + i * 0.16
                if inside(x, y, 0.20, top, 0.80, top + 0.12, 0.06):
                    c = col
            row += bytes(c)
        rows.append(bytes(row))
    raw = b"".join(rows)
    def chunk(t, d):
        body = t + d
        return struct.pack(">I", len(d)) + body + struct.pack(">I", zlib.crc32(body) & 0xffffffff)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")
    open(name, "wb").write(png)
    print("made", name)
make(192, "icon-192.png")
make(512, "icon-512.png")
