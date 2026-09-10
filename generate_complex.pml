# This pymol script serves to generate the 6WM2, human V-ATPase, and prepare it for the simulation

# first, load the human V-ATPase and wait until it is finished loading
fetch 6WM2, async = 0

# Apply the b factor putty preset on the complex
preset.b_factor_putty(selection='6WM2')

# Next, isolate the c subunits
# Create an object containing the rotating subunits from the original complex
create rotating_subunits, 6WM2 and (chain 0 or chain 1 or chain 2 or chain 3 or chain 4 or chain 5 or chain 6 or chain 7 or chain 8 or chain 9 chain E or chain F or chain G or chain Q or chain X or chain Y or chain Z)
# Then, delete those subunits from the main complex
remove 6WM2 and (chain 0 or chain 1 or chain 2 or chain 3 or chain 4 or chain 5 or chain 6 or chain 7 or chain 8 or chain 9 chain E or chain F or chain G or chain Q or chain X or chain Y or chain Z)

# Set the desired initial viewing angle
set_view (\
     0.505418479,   -0.540049851,   -0.672973037,\
    -0.178233713,   -0.828442812,    0.530954540,\
    -0.844263673,   -0.148408175,   -0.514965057,\
    -0.000589307,   -0.001607418, -831.217468262,\
   198.441970825,  203.633316040,  199.557174683,\
  -14003.028320312, 15665.442382812,  -20.000000000 )