# This script will generate frames to be compiled into a movie 
# It will demo how the human V-ATPase rotates as well as how hydrogen ions are transported by the V-ATPase
# It will first fetch 6WM2 (the full V-ATPase complex) and then isolate the A-B dimer (hydrolitic subunits) as well as the c subunits (rotor portion)
# It will cause these subunits to rotate in 60 degree increments at a time
# Next, a hydrogen ion will be loaded into the system
# The hydrogen ion will start in the cytoplasm, lower until it is in the a subunit, and then begin to move with the c subunits
# After it has rotated 300 degrees, it will begin moving downward into the lumen

# First, reinitialize pymol
reinitialize
delete all

# Load the complex
@generate_complex.pml

# Begin python portion
python

import sys
from pathlib import Path
import importlib

# Find the directory in which this file sits
current_dir = Path.cwd()

# Add this directory
if str(current_dir) not in sys.path:
    # If this directory is not in the system paths (that would be searched for modules)
    sys.path.insert(0, str(current_dir)) # Add it and set it as the first one (highest priority)

import run_simulation # Load the run_simulation file now that the main directory is available
importlib.reload(run_simulation) # Reload the module to allow for editing

run_simulation.run_simulation(run_time,current_dir) # Run the simulation, inputting run_time and the current directory

# End python portion
python end