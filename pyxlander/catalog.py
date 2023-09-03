"""
"""


from .bitmap import Bitmap

LanderHull: Bitmap = Bitmap(0, 32, 12, 13)
Exhaust_D: Bitmap = Bitmap(0, 16, 4, 12)
Exhaust_L: Bitmap = Bitmap(8, 16, 8, 3)
Exhaust_R: Bitmap = Bitmap(8, 16, -8, 3)

Catalog: dict[str, tuple[int, int, int, int]] = {
    "LanderHull": (0, 32, 12, 13),
    "CrashedHull": (0, 48, 14, 10),
    "Exhaust_D": (0, 16, 4, 12),
    "Exhaust_L": (8, 16, 8, 3),
    "Exhaust_R": (8, 16, -8, 3),
    "Dust": (8, 24, 8, 8),
}

Twinkle0: Bitmap = Bitmap(48, 0, 3, 3)
Twinkle1: Bitmap = Bitmap(51, 0, 3, 3)
