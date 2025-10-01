# -------------------------------
# G-code utility functions start and end
# -------------------------------
def gcode_start():
    return [
        "%",
        "G21",                      # Set units to millimeters
        "G90",                      # Set absolute positioning
        "G28",                      # Go to machine home
        "G0 X0 Y0 Z0 A90",          # Move A to 90 deg (tool normal to surface)
    ]

def gcode_end():
    return [
        "G53 Z0",                   # Move Z to absolute machine zero
        "G53 X0 Y0 A0 B0",          # Present part
        "M30",                      # Program end
        "%"
    ]