""" This will be my main program file for AI lab 2. """
import sys
import itertools
""" 
Gameplan for program
--------------------
no order...

Resolver...(PL-Resolution in R&N 7.5 on pg 228 for ideas)
Unifictaion...(Unify in R&N 9.2 on pg 285 for ideas)
^function to parse through data as either(Clauses, Predicates, Terms)
    -Three helper functions to hanle each of these specific types
    -sort out terms as well 
^function to manage clauses
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

sys entry: python3 AI_Project2_Resolution\lab2.py AI_Project2_Resolution/truck.cnf
output: yes | no

"""

"""
Resolvers
"""


def cnf_parser(f_name):
    # This function will read and parse the cnf file
    preds = set()
    variables = set()
    consts = set()
    functs = set()
    clauses = []

    with open(f_name, 'r') as file:
        section = None
        for line in file:
            line = line.strip()
            # Skip empty lines and comments(if statements or switch?)
            if not line or line.startswith("#"): 
                continue
            # put in categories
            if line.startswith("Predicates:"):
                preds.update(line.split(":")[1].split())
            elif line.startswith("Variables:"):
                variables.update(line.split(":")[1].split())
            elif line.startswith("Constants:"):
                consts.update(line.split(":")[1].split())
            elif line.startswith("Functions:"):
                functs.update(line.split(":")[1].split())
            elif line.startswith("Clauses:"):
                section = "clauses"
            elif section == "clauses":
                clauses.append(cl_parser(line))
    # print(preds)
    # print(variables)
    # print(consts)
    # print(functs)
    # print(clauses)
    return preds, variables, consts, functs, clauses


def cl_parser(line):
    # Will parse the individual lines in order tomake clauses
    lits = line.split()
    p_lits = [] # set of my parsed literals after being processed
    for lit in lits:
        negated = lit.startswith("!")
        if negated:
            lit = lit[1:] #gotta get rid of the !
        preds, args = pred_parser(lit)
        p_lits.append((negated, preds, tuple(args)))
    return set(p_lits)

def pred_parser(lit):
    # Seperates the pred name and its args(returns both)
    name, args = lit.split("(")
    args = args[:-1].split(",")  # delete ')' & ','
    return name, args

"""
Unify codes
"""
def unify(term1, term2, subs):
    """
    Whats needed??
    -check if var?
    -check if seen alr?
    -combine vars
    
    begin to process the whole term with subsitution
    if sub works return the sub, else NOne
    """
    ...

def univar(var, term, subs):
    # unify the vars if necessary. Return updated var, if any
    ...

def seen(var, term, subs):
    # check if seen alr to avoid loops. Return Bool
    ...

def var_check(term):
    # is it a var? Return bool
    ...



def main():
    # used to test and finally run this code.
    cnf_file = sys.argv[1]
    cnf_parser(cnf_file)    


if __name__ == "__main__":
    main()