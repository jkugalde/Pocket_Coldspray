import math
from param_var import *
from param_fix import * 
from movements import *

def linewall(gcode):

    gcode2=gcode

    # Compute base coordinates
    x_center = 0.0
    x_start = x_center - line_length / 2
    x_end = x_center + line_length / 2
    y_base = -y_negative_offset
    z_zero = -(z_offset_total + standoff_distance)

    for i in range(num_layers):
            z_layer = z_zero - i * layer_height
            h_rot_i = h_rot_0 - i * layer_height

            # Main normal pass (A = 90)
            gcode.append(rapid_move(a=90))
            gcode.append(rapid_move(x=x_start, y=y_base, z=z_layer))
            gcode.append(linear_move(x=x_end, y=y_base, z=z_layer, feed=feed_g1))

            # Oblique pass (A = 90 + θ)
            gcode.append(rapid_move(a=90 + theta_deg))
            y_corr, z_corr = get_oblique_position(y_base, z_layer, h_rot_i, theta_deg)
            gcode.append(rapid_move(x=x_end, y=y_corr, z=z_corr))
            gcode.append(linear_move(x=x_start, y=y_corr, z=z_corr, feed=feed_g1))

            # Oblique pass (A = 90 - θ)
            gcode.append(rapid_move(a=90 - theta_deg))
            y_corr, z_corr = get_oblique_position(y_base, z_layer, h_rot_i, -theta_deg)
            gcode.append(rapid_move(x=x_start, y=y_corr, z=z_corr))
            gcode.append(linear_move(x=x_end, y=y_corr, z=z_corr, feed=feed_g1))

    return gcode2