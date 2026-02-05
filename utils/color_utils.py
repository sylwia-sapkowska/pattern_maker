from typing import TypeAlias, List
from utils.palette import Palette, Color
from scipy.optimize import linear_sum_assignment
import numpy as np

RGB: TypeAlias = tuple[int, int, int]

def convert_rgb_to_cielab(RGB: RGB) -> tuple[float, float, float]:
    """ 
    Converts RGB color to CIELAB color space for better color distance calculations.
    Implemented from scratch for fun.
    """
    rgb = np.array(RGB) / 255.0

    def to_linear(c):
        return np.where(c <= 0.04045,
                        c / 12.92,
                        ((c + 0.055) / 1.055) ** 2.4)

    rgb_lin = to_linear(rgb)

    M = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    X, Y, Z = M.dot(rgb_lin)

    Xn, Yn, Zn = 0.95047, 1.0, 1.08883

    def f(t):
        delta = 6/29
        return np.where(t > delta**3,
                        t ** (1/3),
                        (t / (3 * delta**2)) + 4/29)

    fx, fy, fz = f(X/Xn), f(Y/Yn), f(Z/Zn)

    L = 116 * fy - 16
    a = 500 * (fx - fy)
    b = 200 * (fy - fz)
    return L, a, b

def map_colors_to_palette(
    colors_list: List[RGB], palette: Palette, include_blends: bool
) -> List[Color]:
    """
    Maps a list of RGB colors to the closest colors in the given palette.
    Returns a list of Color objects from the palette corresponding to the input colors.
    Currently doesn't handle blends, but the include_blends flag can be used in the future to enable that functionality.
    """
    palette_rgb = palette.get_all_rgb()



