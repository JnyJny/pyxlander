'''
'''

from dataclasses import dataclass
from .bitmap import Bitmap

LanderHull = Bitmap(16, 0, 16, 16)
Exhaust_D = Bitmap(40, 0, 8, 16)
Exhaust_R = Bitmap(32, 0, 8, 8)
Exhaust_L = Bitmap(32, 0, -8, 8)
Twinkle0 = Bitmap(48, 0, 3, 3)
Twinkle1 = Bitmap(51, 0, 3, 3)

                        
