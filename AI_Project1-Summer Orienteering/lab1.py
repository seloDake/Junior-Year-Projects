""" This will be my main program file for my first AI lab. """
import sys
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

# Function to load in image
def load_img(image):
    img = Image.open(image)
    
    # size of the image
    print(img.size)
    # format of the image
    print(img.format)
    
    img.show()

load_img(r'AI_Project1-Summer Orienteering\terrain.png')

# Function for loading elevation
def load_mapdict(f_path):
    try:
        elev_data = [] # open list for data points
        with open(f_path, 'r') as elev:
            for line in elev:
                raw_data = line.split()
                i = 0
                while i <= len(raw_data) - 1:
                    # ignore the last five entries of a line
                    if i in (399, 398, 397, 396, 395):
                        pass
                    else:
                        elev_data.append(raw_data[i])
                    i+=1
            print(len(elev_data))
            return elev_data
    except FileNotFoundError:
        print(f"Error: File '{f_path}' not found.")
        return None

load_mapdict('AI_Project1-Summer Orienteering\mpp.txt')
