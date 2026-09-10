# This is a script that defines the proton_conveyorbelt class
# This class will make an entry in the proton subclass for each proton
# The conveyorbelt class will keep track of how many protons there are, which is the last in the chain, and when a new one needs to be created
# The proton subclass will keep track of a proton's coordinates, angle, name, etc. (the origin being in the center of the c subunits)

from pymol import cmd
import math

class Proton_conveyorbelt:
    # Class to manage the conveyorbelt of protons

    def __init__(self):
        # Generate a first proton
        new_proton = self.Proton(1)
        self.proton_list = [new_proton] # Define the list of protons and add the first one to the list
        self.number_of_protons = 1 # Record the number of protons (1 right now)
        self.last_proton = new_proton # Record the first proton as the last proton in the list

    def add_proton(self):
        # Method to add a new proton
        new_proton = self.Proton(self.number_of_protons+1) # Generate a new proton
        self.proton_list.append(new_proton) # Add the new proton to the list of protons
        self.number_of_protons += 1 # Increment the number of protons by 1
        self.last_proton = new_proton # Record the newly created proton as the last proton in the conveyorbelt

    def update_conveyorbelt(self, rotating_frame):
        # Method to update every proton on the conveyorbelt
        # rotating_frame is a logical value that tells you whether rotation needs to occur

        for proton in self.proton_list:
            # Loop through each loaded proton
            proton.update_proton_position(rotating_frame) # Update the proton's position, passing along whether there is a rotating frame
            if proton.coordinates[1] <= -100:
                # If the current proton is below -100 in the y
                cmd.delete(proton.name) # Delete the proton object from pymol
                self.proton_list.remove(proton) # Remove the proton from the conveyorbelt

        if self.last_proton.coordinates[0] >= -115:
            # If the last proton's x coordinate is greater than or equal to -115 (there is room for a new proton)
            self.add_proton() # Add a new proton

    class Proton:
        # Class to generate instances for specific protons

        proton_spawn_displacement = [0,-75,0] # Displacement needed to get a proton to the origin from its spawn position
        proton_relative_spawn_coordinates = [-145,60,0] # Coordinates of the proton's starting position relative to the center of the c subunits (origin)

        def __init__(self,number):
            # Generate a new proton, inputting what number proton it is
            self.name = f'proton_{number}' # Generate a named string, incorportaing the proton's number
            cmd.pseudoatom(self.name, elem='H') # Add a pseudoatom, representing a proton
            cmd.show('spheres', self.name) # Display the pseudoatom ('proton')

            # Alter the proton's size and color
            cmd.set('sphere_scale',5,self.name) # Set the size
            cmd.color('red',self.name) # Set the color

            # Adjust the proton's position
            cmd.translate(self.proton_spawn_displacement,self.name,camera=1) # Translate from spawn to the origin
            cmd.translate(self.proton_relative_spawn_coordinates,self.name,camera=1) # Translate from the origin to the proton's starting position

            # Define the coordinates
            self.coordinates = self.proton_relative_spawn_coordinates.copy()

            # Initializes the proton as moving to the right
            self.movement = 'right'

            # Initialize the proton's angle as 0 degrees
            self.angle = 0

        def update_proton_position(self,rotating_frame):
            # Method that is used to update the position of a proton, inputing whether or not we are rotating this frame
            match self.movement:
                # Consider which case the proton's movement attribute is in
                case 'right':
                    # If the proton is moving to the right
                    cmd.translate([1,0,0],self.name,camera=1) # Translate the proton one to the right, based on the camera's axes
                    self.coordinates[0] += 1 # Update the proton's coordinates
                    if self.coordinates[0] >= -35:
                        # Once the proton reaches -35 on its x, it is ready to begin moving downward for the first time
                        self.movement = 'first down'
                        self.radius = -35 # Set the radius of rotation to -35
                case 'first down':
                    # If the proton is moving down for the first time
                    cmd.translate([0,-1,0],self.name,camera=1) # Translate the proton down
                    self.coordinates[1] -= 1 # Decrease its y coordinate
                    if self.coordinates[1] <= 0:
                        # Once the proton reachs 0 on its y, it is ready to begin rotating
                        self.movement = 'rotating'
                case 'rotating':
                    if rotating_frame:
                        # If rotation is occuring this frame
                        self.angle -= 7.2 # Decrease the proton's angle by 7.2 degrees
                        new_x,new_y,new_z = self.calculate_rotating_coordinates() # Calculate the new coordinates
                        old_x,old_y,old_z = self.coordinates # Pull the old coordinates
                        displacement = [new_x-old_x,new_y-old_y,new_z-old_z] # Calculate the displacement
                        cmd.translate(displacement,self.name,camera=1) # Translate the proton by the calculated displacement
                        self.coordinates = [new_x,new_y,new_z] # Save the new coordinates

                        if self.angle <= -324:
                            # If the proton has rotated -312 degrees
                            self.movement = 'second down' # Transition to going down again
                    else:
                        return
                case 'second down':
                    # If the proton is moving down for the second time
                    cmd.translate([0,-1,0],self.name,camera=1) # Translate the proton down
                    self.coordinates[1] -= 1 # Decrease its y coordinate

        def calculate_rotating_coordinates(self):
            # Method designed to calculate the cartesian coordinates a proton needs to go to based on its current angle
            new_x = self.radius * math.cos(math.radians(self.angle)) # Calculate the new x position, first converting the angle to radians
            new_z = self.radius * math.sin(math.radians(self.angle)) # Same as before, but for the z coordinate
            return [new_x, 0, new_z] # Return the new coordinates