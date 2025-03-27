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
parselyssss
"""

# ---------------------------
# CNF Parser and Helper Functions
# ---------------------------
def cnf_parser(f_name):
    # Read and parse the CNF file into its components.
    preds = set()
    variables = set()
    consts = set()
    functs = set()
    clauses = []
    
    with open(f_name, 'r') as file:
        section = None
        for line in file:
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue
            # Process categories based on file labels
            if line.startswith("Predicates:"):
                preds.update(line.split(":", 1)[1].split())
            elif line.startswith("Variables:"):
                variables.update(line.split(":", 1)[1].split())
            elif line.startswith("Constants:"):
                consts.update(line.split(":", 1)[1].split())
            elif line.startswith("Functions:"):
                functs.update(line.split(":", 1)[1].split())
            elif line.startswith("Clauses:"):
                section = "clauses"
            elif section == "clauses":
                clauses.append(cl_parser(line))
    return preds, variables, consts, functs, clauses

def cl_parser(line):
    # Parse a line into a clause, represented as a set of literals.
    lits = line.split()
    p_lits = []  # parsed literals will be stored here
    for lit in lits:
        negated = lit.startswith("!")
        if negated:
            lit = lit[1:]  # remove the '!' symbol
        pred, args = pred_parser(lit)
        p_lits.append((negated, pred, tuple(args)))
    return set(p_lits)

def pred_parser(lit):
    # Split the predicate from its arguments.
    if "(" in lit and lit.endswith(")"):
        name, args = lit.split("(", 1)
        args = args[:-1].split(",")  # remove trailing ")" and split arguments
        p_args = [fun_parser(arg) for arg in args]
        return name, p_args
    else:
        return lit, ()  # no arguments present

def fun_parser(term):
    # Parse a function term into a tuple (name, (args, ...))
    if "(" in term and term.endswith(")"):
        name, args = term.split("(", 1)
        args = args[:-1].split(",")  # remove trailing ")" and split arguments
        return (name, tuple(args))
    return term

# ---------------------------
# Unification Functions
# ---------------------------
def is_function_term(term):
    # Check if the term is a function term of the form (name, (args,...))
    return isinstance(term, tuple) and len(term) == 2 and isinstance(term[0], str) and isinstance(term[1], tuple)

def unify(term1, term2, subs):
    # Attempt to unify term1 and term2 using the current substitution dictionary.
    if term1 == term2:
        return subs
    # Handle function terms specially.
    if is_function_term(term1) and is_function_term(term2):
        if term1[0] != term2[0] or len(term1[1]) != len(term2[1]):
            return None
        for t1, t2 in zip(term1[1], term2[1]):
            subs = unify(t1, t2, subs)
            if subs is None:
                return None
        return subs
    # If both terms are sequences (but not function terms), unify element-by-element.
    if isinstance(term1, (list, tuple)) and isinstance(term2, (list, tuple)) and not (is_function_term(term1) or is_function_term(term2)):
        if len(term1) != len(term2):
            return None
        for t1, t2 in zip(term1, term2):
            subs = unify(t1, t2, subs)
            if subs is None:
                return None
        return subs
    # If term1 is a variable, bind it.
    if var_check(term1):
        return univar(term1, term2, subs)
    # If term2 is a variable, bind it.
    if var_check(term2):
        return univar(term2, term1, subs)
    return None

def univar(var, term, subs):
    # Bind a variable to a term if possible.
    if var in subs:
        return unify(subs[var], term, subs)
    if term in subs:
        return unify(var, subs[term], subs)
    if seen(var, term, subs):
        return None  # Prevent infinite loops
    subs[var] = term
    return subs

def seen(var, term, subs):
    # Check if 'var' appears in 'term' to avoid circular substitutions.
    if var == term:
        return True
    if term in subs:
        return seen(var, subs[term], subs)
    if isinstance(term, tuple):
        return any(seen(var, st, subs) for st in term[1])
    return False

def var_check(term):
    # A variable is defined as a nonempty string starting with a lowercase letter.
    return isinstance(term, str) and term and term[0].islower()

# ---------------------------
# Resolution Functions
# ---------------------------
def resolve(cl1, cl2):
    # Attempt to resolve two clauses.
    for lit1 in cl1:
        for lit2 in cl2:
            neg1, pred1, args1 = lit1
            neg2, pred2, args2 = lit2
            # Look for complementary literals with the same predicate.
            if pred1 == pred2 and neg1 != neg2:
                subs = unify(args1, args2, {})
                if subs is not None:
                    # Create a new clause by removing the resolved literals and applying substitutions.
                    ncl = (cl1 - {lit1}) | (cl2 - {lit2})
                    ncl = ap_subs(ncl, subs)
                    # Return an empty set for an empty clause (i.e., contradiction).
                    return ncl if ncl else set()
    return None

def ap_subs(cl, subs):
    # Apply the substitution dictionary 'subs' to every literal in the clause.
    ncl = set()
    for neg, pred, args in cl:
        new_args = tuple(sub_term(arg, subs) for arg in args)
        ncl.add((neg, pred, new_args))
    return ncl

def sub_term(term, subs):
    # Recursively apply substitutions to a term.
    if is_function_term(term):
        return (term[0], tuple(sub_term(arg, subs) for arg in term[1]))
    elif isinstance(term, (list, tuple)):
        return type(term)(sub_term(t, subs) for t in term)
    else:
        return subs.get(term, term)

def res_loop(cl):
    # Main resolution loop: repeatedly resolve pairs of clauses.
    new_cl = set(frozenset(c) for c in cl)
    while True:
        new_pairs = list(itertools.combinations(new_cl, 2))
        new_res = set()
        for cl1, cl2 in new_pairs:
            res = resolve(cl1, cl2)
            if res is not None:
                # An empty clause (represented as an empty set) signals contradiction.
                if not res:
                    return "no"
                new_res.add(frozenset(res))
        if new_res.issubset(new_cl):
            return "yes"
        new_cl.update(new_res)

# ---------------------------
# Main Function
# ---------------------------
def main():
    # Get the CNF file name from the command line.
    cnf_file = sys.argv[1]
    # Parse the CNF file (once) to get all components.
    preds, variables, consts, funs, cl = cnf_parser(cnf_file)
    # Run the resolution loop to decide satisfiability.
    result = res_loop(cl)
    print(result)

if __name__ == "__main__":
    main()
