# -------------------------------
# Movements
# -------------------------------

from param_var import *
import math

def rapid_move(x=None, y=None, z=None, a=None, b=None):
    line = "G0"
    if x is not None:
        line += f" X{x:.3f}"
    if y is not None:
        line += f" Y{y:.3f}"
    if z is not None:
        line += f" Z{z:.3f}"
    if a is not None:
        line += f" A{a:.3f}"
    if b is not None:
        line += f" B{b:.3f}"
    line += f" F{feed_g0}"
    return line

def linear_move(x=None, y=None, z=None, a=None, b=None, feed=None):
    line = "G1"
    if x is not None:
        line += f" X{x:.3f}"
    if y is not None:
        line += f" Y{y:.3f}"
    if z is not None:
        line += f" Z{z:.3f}"
    if a is not None:
        line += f" A{a:.3f}"
    if b is not None:
        line += f" B{b:.3f}"
    if feed is not None:
        line += f" F{feed}"
    return line

def get_oblique_position(y_base, z_base, h_rot_i, theta_deg):
    """Compute the Y and Z correction for oblique spray."""
    theta_rad = math.radians(theta_deg)
    dy = h_rot_i * math.tan(theta_rad)
    dz = h_rot_i * (1 - math.cos(theta_rad))
    return y_base + dy, z_base - dz