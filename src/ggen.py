import math
from param_var import *
from param_fix import *
from start_end import *
from movements import *
from linewall import *
# -------------------------------
# Main G-code generation
# -------------------------------
def generate_gcode(): #lineas superpuestas
    gcode = []
    gcode += gcode_start()
    gcode=linewall(gcode);  
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
