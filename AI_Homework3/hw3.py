""" Code for solving hw3 """
import sys
import math
from collections import Counter, defaultdict

""" Read the data file and parse the info """
def reader(d_file):
   data = []
   with open(d_file, 'r') as f:
        for line in f:
            sects = line.strip().split()
            attributes = sects[:-1]
            label = sects[-1]
            #update the data for the code as booleans
            data.append((list(map(lambda x: x == "True", attributes)), label))
   return data

def main():
    ...