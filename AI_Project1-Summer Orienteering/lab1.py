""" This will be my main program file for my first AI lab. """
import sys

""" 
Gameplan for program
--------------------
no order...
function to create dictionary map of the terrain
    - parse the 400 x 500 elevation file
      ignore last 5 nums of each line
    - sync each pixel of terrain file to corresponding value in
      terrain txt file. (395 x 500)
function to solve
    - parse the instruction file
      probably a helper function
      The nums represent coords that must be visited in order
    - Set values for speed of travel through various terrains
      each color in map is a unique terrain
    - utilize A* search for solver
      assume that theres no diff in walking on inclined, declined,
      or flat land
    - create a helper heuristic function
      sets h value for how close pixel is to another
    - inputs for sys should be terrain-image, elevation-file, path-file, output-image-filename
      should look something like *terrain.png mpp.txt red.txt redOut.png*

"""