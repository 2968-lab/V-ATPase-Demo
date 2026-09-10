# This script runs the simulation that creates the proton conveyorbelt

import importlib
import proton_conveyorbelt_class
from pymol import cmd
from config import run_time

# Reload the proton_conveyorbelt file to allow for editing
importlib.reload(proton_conveyorbelt_class)

def take_image(frame_number,frame_folder):
    # Defines function that takes an image, inputting the frame number and file folder
    cmd.ray # Activate ray tracing
    cmd.png(str(frame_folder / f'frame_{frame_number}.png'))

def run_simulation(directory):
    # Script to run the simulation given the main working directory
    # Runs at 30 fps

    # Open Frames folder
    frame_folder = directory / 'Frames' # Create directory for storing frames
    frame_folder.mkdir(parents='True',exist_ok='True') # Generate any non-existing directories, but don't replace them if they do exist

    num_frames = round(run_time * 30) # Convert seconds to frames

    conveyorbelt = proton_conveyorbelt_class.Proton_conveyorbelt() # Generate a proton conveyorbelt object

    counter = 0 # Initialize counter for determining when rotation occurs
    for frame in range(num_frames):
        # Run once for each frame

        if counter > 24: # 25 frames after the last rotation
        # Slowly rotate the image over 5 frames
            rotation = True # Set rotation equal to true
            cmd.rotate('y',7.2,'rotating_subunits') # Rotate the rotating subunits by 36 degrees across 5 frames (7.2 degrees per frame)
            conveyorbelt.update_conveyorbelt(rotation) # Update proton positions, indicating that roation occurs
            take_image(frame+1,frame_folder) # Take an image
        else:
            rotation = False # Set rotation to False
            conveyorbelt.update_conveyorbelt(rotation) # Update proton positions, indicating that rotation does not occur
            take_image(frame+1,frame_folder) # take an image
        if counter == 29:
            # Once the 30th frame has been taken, reset the counter
            counter = 0
            continue

        counter += 1 # Increase the counter by 1