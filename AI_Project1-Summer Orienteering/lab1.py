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
TERRAIN_COSTS = {
    (248, 148, 18): 1.0,   # Open land
    (255, 192, 0): 1.2,    # Rough meadow
    (255, 255, 255): 1.5,  # Easy movement forest
    (2, 208, 60): 2.0,     # Slow run forest
    (2, 136, 40): 2.5,     # Walk forest
    (5, 73, 24): float('inf'),  # Impassable vegetation
    (0, 0, 255): 2.7,  # Water
    (71, 51, 3): 0.8,      # Paved road
    (0, 0, 0): 0.9,        # Footpath
    (205, 0, 101): float('inf') # Out of bounds
}

# Function to load in image
def load_img(image):
    img = Image.open(image)
    img = img.convert('RGB')
    img.show()
    return img

#load_img(r'AI_Project1-Summer Orienteering\terrain.png')

# Function for loading elevation
def load_mapdict(f_path):
    try:
        elev_data = []
        with open(f_path, 'r') as f:
          for line in f:
            values = list(map(float, line.split()))
            elev_data.append(values[:395])  # Ignore last 5 values per line
            #print(len(elev_data))
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

# get the terrain costs
def get_terrain_cost(terrain, x, y):
    color = terrain.getpixel((x, y))[:3]  # Get RGB
    return TERRAIN_COSTS.get(color, 1.0)  # Default cost = 1.0 if unknown

# Calculate my heuristic
def heuristic(a, b, elev):
    x1, y1 = a
    x2, y2 = b
    z1 = elev[y1, x1]
    z2 = elev[y2, x2]
    return np.sqrt(((x2 - x1)*10.29) ** 2 + ((y2 - y1)*7.55) ** 2 + (z2 - z1) ** 2)

# path to draw output
def draw_path(image, path, output_path):
    draw = ImageDraw.Draw(image)
    for i in range(len(path) - 1):
        draw.line([path[i], path[i + 1]], fill=(161, 70, 221), width=1)
    image.save(output_path)

# implement A* search
def as_search(start, goal, terrain, elevation):
    # basics
    lookat = []
    heapq.heappush(lookat, (0, start))
    history = {}
    #traveled = {start: 0}
    cost_so_far = {start: 0}

    while lookat:
        _, curr = heapq.heappop(lookat)
        if curr == goal:
            break
        
        x, y = curr
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            neighbor = (x + dx, y + dy)
            if 0 <= neighbor[0] < terrain.width and 0 <= neighbor[1] < terrain.height:
                t_cost = get_terrain_cost(terrain, *neighbor)
                if t_cost == 'inf':
                    continue  # Skip impassable terrain
                
                #distance = heuristic(curr, neighbor) + traveled[curr]
                move_cost = heuristic(curr, neighbor, elevation) * t_cost
                new_cost = cost_so_far[curr] + move_cost
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    #traveled[neighbor] = distance
                    priority = new_cost + heuristic(goal, neighbor, elevation)
                    heapq.heappush(lookat, (priority, neighbor))
                    history[neighbor] = curr

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = history.get(current, start)
    path.append(start)
    path.reverse()
    return path

# main function
def main():
    terrain_img = load_img(sys.argv[1])
    elev_data = load_mapdict(sys.argv[2])
    stops = load_hitpoints(sys.argv[3])
    output_file = sys.argv[4]

    t_dist = 0
    full_path = []
    for i in range(len(stops) - 1):
        path = as_search(stops[i], stops[i + 1], terrain_img, elev_data)
        full_path.extend(path)
        t_dist += sum(heuristic(path[j], path[j+1], elev_data) / get_terrain_cost(terrain_img, *path[j]) for j in range(len(path)-1))
    
    draw_path(terrain_img, path, output_file)
    print(t_dist)
    
if __name__ == "__main__":
    main()