import math

# -------------------------------
# Fixed system offsets
# -------------------------------
z_tool_offset = 45.0          # Tool length offset [mm]
substrate_thickness = 5.0     # Substrate thickness [mm]
y_negative_offset = 10.0      # Y offset due to tool positioning [mm]
z_offset_total = z_tool_offset - substrate_thickness

# -------------------------------
# Parameters that vary per test
# -------------------------------
feed_g1 = 300.0               # Linear deposition feedrate [mm/min]
feed_g0 = 1500.0              # Rapid move feedrate [mm/min]
standoff_distance = 6.0       # Distance from nozzle to surface [mm]
layer_height = 0.2            # Deposition layer height [mm]
num_layers = 5                # Number of layers to deposit
line_length = 40.0            # Length of each line [mm]
theta_deg = 20.0              # Oblique angle for side passes [degrees]
h_rot_0 = 20.0                # Initial height from rotation axis to substrate [mm]
output_filename = "oblique_test.ngc"

# -------------------------------
# G-code utility functions
# -------------------------------
def gcode_start():
    return [
        "%",
        "G21",                      # Set units to millimeters
        "G90",                      # Set absolute positioning
        "G28",                      # Go to machine home
        "G53 G0 A90",               # Move A to 90 deg (tool normal to surface)
    ]

def gcode_end():
    return [
        "G53 G0 Z0",                # Move Z to absolute machine zero
        "G53 G0 X0 Y0 A0 B0",       # Present part
        "M30",                      # Program end
        "%"
    ]

def set_axis(axis, value):
    return f"G0 {axis}{value:.3f}"

def rapid_move(x=None, y=None, z=None):
    line = "G0"
    if x is not None:
        line += f" X{x:.3f}"
    if y is not None:
        line += f" Y{y:.3f}"
    if z is not None:
        line += f" Z{z:.3f}"
    line += f" F{feed_g0}"
    return line

def linear_move(x=None, y=None, z=None, feed=None):
    line = "G1"
    if x is not None:
        line += f" X{x:.3f}"
    if y is not None:
        line += f" Y{y:.3f}"
    if z is not None:
        line += f" Z{z:.3f}"
    if feed is not None:
        line += f" F{feed}"
    return line

def get_oblique_position(y_base, z_base, h_rot_i, theta_deg):
    """Compute the Y and Z correction for oblique spray."""
    theta_rad = math.radians(theta_deg)
    dy = h_rot_i * math.tan(theta_rad)
    dz = h_rot_i * (1 - math.cos(theta_rad))
    return y_base + dy, z_base - dz

# -------------------------------
# Main G-code generation
# -------------------------------
def generate_gcode():
    gcode = []
    gcode += gcode_start()

    # Compute base coordinates
    x_center = 0.0
    x_start = x_center - line_length / 2
    x_end = x_center + line_length / 2
    y_base = -y_negative_offset
    z_zero = - (z_offset_total + standoff_distance)

    for i in range(num_layers):
        z_layer = z_zero - i * layer_height
        h_rot_i = h_rot_0 - i * layer_height

        # Main normal pass (A = 90)
        gcode.append(set_axis('A', 90))
        gcode.append(rapid_move(x_start, y_base, z_layer))
        gcode.append(linear_move(x_end, y_base, z_layer, feed_g1))

        # Oblique pass (A = 90 + θ)
        gcode.append(set_axis('A', 90 + theta_deg))
        y_corr, z_corr = get_oblique_position(y_base, z_layer, h_rot_i, theta_deg)
        gcode.append(rapid_move(x_end, y_corr, z_corr))
        gcode.append(linear_move(x_start, y_corr, z_corr, feed_g1))

        # Oblique pass (A = 90 - θ)
        gcode.append(set_axis('A', 90 - theta_deg))
        y_corr, z_corr = get_oblique_position(y_base, z_layer, h_rot_i, -theta_deg)
        gcode.append(rapid_move(x_start, y_corr, z_corr))
        gcode.append(linear_move(x_end, y_corr, z_corr, feed_g1))

    gcode += gcode_end()

    # Write to file
    with open(output_filename, "w") as f:
        for line in gcode:
            f.write(line + "\n")

    print(f"G-code written to: {output_filename}")

# -------------------------------
# Run main
# -------------------------------
if __name__ == "__main__":
    generate_gcode()
