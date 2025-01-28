
"""

##Homework 1

program alg  
-write first word  
-cycle through all possible first changes of the word.  
-check them all for validity  
-look at next exhange and cycle for validity  
-repeat until word has been found
"""

# main files to import
import string

# Load the dictionary and return as a set for fast lookup
def load_dictionary(file_path):
    try:
        with open(file_path, 'r') as f:
            return set(word.strip() for word in f.readlines())
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None

# Validate input words
def validate_word(word, dictionary):
    return word in dictionary

# Generate valid new words by changing one character at a time
def generate_neighbors(word, dictionary, explored, frontier):
    neighbors = []
    alphabet = string.ascii_lowercase

    for i in range(len(word)):
        for char in alphabet:
            if char != word[i]:
                new_word = word[:i] + char + word[i + 1:]
                if new_word in dictionary and new_word not in explored and new_word not in frontier:
                    neighbors.append(new_word)
    return neighbors

# Word ladder solver
def solve_word_ladder(start, target, dictionary):
    if start == target:
        print(start)
        return [start]

    frontier = [start]
    explored = set()
    parent_map = {start: None}  # Track the path to reconstruct the ladder

    while frontier:
        curr_wrd = frontier.pop(0)
        explored.add(curr_wrd)

        for neighbor in generate_neighbors(curr_wrd, dictionary, explored, frontier):
            if neighbor == target:
                # Reconstruct and return the path
                path = [neighbor]
                while curr_wrd:
                    path.append(curr_wrd)
                    curr_wrd = parent_map[curr_wrd]
                return path[::-1]

            frontier.append(neighbor)
            parent_map[neighbor] = curr_wrd

    print("No solution found.")
    return []

# Main execution
if __name__ == "__main__":
    input_data = input()
    try:
        file_path, start_word, target_word = input_data.split()
        dictionary = load_dictionary(file_path)

        if dictionary is None:
            exit()

        if not validate_word(start_word, dictionary):
            exit()

        if not validate_word(target_word, dictionary):
            exit()

        path = solve_word_ladder(start_word, target_word, dictionary)
        if path:
            print("\n".join(path))
    except ValueError:
        print("Error: Invalid input format. Please provide 'dictionary_file start_word target_word'.")

