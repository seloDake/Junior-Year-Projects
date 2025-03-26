""" This will be my main program file for AI lab 2. """
import sys

""" 
Gameplan for program
--------------------
no order...

Resolver...(PL-Resolution in R&N 7.5 on pg 228 for ideas)
Unifictaion...(Unify in R&N 9.2 on pg 285 for ideas)
function to parse through data as either(Clauses, Predicates, Terms)
    -Three helper functions to hanle each of these specific types
    -sort out terms as well 
function to manage clauses
    - needs to store and check if clause has been seen before
    - also needs to store and compare said functions + create them?
Unification function
    -What must be compared?
    -How do you handle substituting a free variable for one of following?
    -Another free variable
    -A constant
    -A function
    -How do you create a new free variable to prevent name conflicts?
    -How will you apply the substitutions to predicates and functions?

sys entry: python3 lab2.py testcases/functions/f1.cnf
output: yes | no

"""

def cnf_parser(f_name):
    ...

def cl_parser(line):
    ...

def pred_parser(lit):
    ...
