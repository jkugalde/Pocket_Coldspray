# -------------------------------
# Parameters that vary per test
# -------------------------------
feed_g1 = 300.0               # Linear deposition feedrate [mm/min]
feed_g0 = 1500.0              # Rapid move feedrate [mm/min]
standoff_distance = 5.0       # Distance from nozzle to surface [mm]
layer_height = 0.2            # Deposition layer height [mm]
num_layers = 5                # Number of layers to deposit
line_length = 40.0            # Length of each line [mm]
theta_deg = 20.0              # Oblique angle for side passes [degrees]
h_rot_0 = 10.0                # Initial height from rotation axis to substrate [mm]
output_filename = "oblique_test.ngc"