""" Code for solving hw3 """
import sys
import math
from collections import Counter, defaultdict

"""python AI_Homework3\hw3.py AI_Homework3\dtree-data.dat.txt"""
""" Read the data file and parse the info """
def reader(d_file):
   data = []
   with open(d_file, 'r') as f:
        for line in f:
            sects = line.strip().split()
            attributes = sects[:-1]
            AoB = sects[-1]
            #update the data for the code as booleans
            data.append((list(map(lambda x: x == "True", attributes)), AoB))
   return data

"""Check to see what to strata on"""
def checker(data):
    ...

def main():
    d_file = sys.argv[1]
    rdata = reader(d_file)
    #print(rdata[1][0][1])
    ...

if __name__ == "__main__":
    main()