""" This will be my main program file for my first AI lab. """
import sys
import numpy as np
import heapq
from PIL import Image, ImageDraw

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

# Set terrain costs
TERRAIN_SPEED = {
    (248, 148, 18): 5.0,   # Open land
    (255, 192, 0): 4.0,    # Rough meadow
    (255, 255, 255): 3.5,  # Easy movement forest
    (2, 208, 60): 3.0,     # Slow run forest
    (2, 136, 40): 2.0,     # Walk forest
    (5, 73, 24): 0.0,      # Impassable vegetation
    (0, 0, 255): 0.0,      # Water
    (71, 51, 3): 6.0,      # Paved road
    (0, 0, 0): 5.5,        # Footpath
    (205, 0, 101): 0.0     # Out of bounds
}

# Function to load in image
def load_img(image):
    img = Image.open(image)
    img.show()
    return img

load_img(r'AI_Project1-Summer Orienteering\terrain.png')

# Function for loading elevation
def load_mapdict(f_path):
    try:
        elev_data = []
        with open(f_path, 'r') as f:
          for line in f:
            values = list(map(float, line.split()))
            elev_data.append(values[:395])  # Ignore last 5 values per line
            print(len(elev_data))
            return np.array(elev_data)
            #return elev_data
    except FileNotFoundError:
        print(f"Error: File '{f_path}' not found.")
        return None
    
#load_mapdict('AI_Project1-Summer Orienteering\mpp.txt')

# load the path to follow
def load_hitpoints(f_path):
    points = []
    with open(f_path, 'r') as f:
        for line in f:
            x, y = map(int, line.split())
            points.append((x, y))
    return points

# path to draw output
