#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
based on AIMA code
Variable heuristics:
    - Original order: Grabs all the remaing unassigned variables and returns the
    first one without any sort of sort applied
    - MRV: Choose variable with the least legal values left in its domain
    allows us to encounter failure quickly before diving deeper into the tree
    if the wrong setp has been selected
Value Order heuristics:
    - Ordinary domain values: retursn values without sorting or any type of ordering
    - LCV: Least constraining value that sorts by the amount of conflicts by ascending
    order
"""
# heuristics build out the LCV Heuristic and MRV heuristic

#VARIABLE ORDERING
def original_value_order(csp, assignment):
    """
    find all variables that have not been assigned and return the first variable
    """
    unassigned_var = [vertex for vertex in csp.variables if vertex not in assignment]
    return unassigned_var[0]

def mrv(csp,assignment):
    """
    Minimum remaing values heuristic for ordering variables used
    with the tie breaking rule.
    We want to select the variable with the fewest remaining legal values
    """
    #return argmin_random_tie([v for v in csp.variables if v not in assignment],
                             #key=lambda var: num_legal_values(csp, var, assignment))
    unassign_min_rem_val=[]
    for variable in csp.variables:
        if variable not in assignment:
            #amount of legal values left
            domain_count = len(csp.curr_domains[variable])
            constraint_count = len(csp.constraints[variable])
            unassign_min_rem_val.append((variable,domain_count,constraint_count))
    #first sort by the domain amount from legal Values
    unassign_min_rem_val.sort(key=lambda x: x[1])
    #Then sort by the highest amount of constraints
    unassign_min_rem_val.sort(key=lambda x: x[2],reverse=True)
    #return the value at index 0 within the variable index
    return unassign_min_rem_val[0][0]
    
#VALUE ORDERING
    

def unordered_domain_values(csp, variable, assignment):
    """
    Returns values in whatever order they currently are in
    """
    return csp.domains[variable]

def lcv(csp, variable, assignment):
    """
    LCV sort the values by the amount of conflcits of the assignment in ascending order
    """
    # Least constraining value heuristic.
    # Consider values with fewer conflicts first.
    return sorted(csp.curr_domains[variable],key=lambda value: csp.conflicted_num(assignment,variable,value))