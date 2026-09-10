# This is the main script that initializes and runs the visualization

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

if str(current_dir) not in sys.path:
    # If this directory is not in the system paths (that would be searched for modules)
    sys.path.insert(0, str(current_dir)) # Add it and set it as the first one (highest priority)

import run_visualization # Load the run_visualization file
importlib.reload(run_visualization) # Reload the module to allow for editing

from config import run_time

run_visualization.run_visualization(current_dir,run_time) # Run the visualization, inputting the current directory and run time

# End python portion
python end