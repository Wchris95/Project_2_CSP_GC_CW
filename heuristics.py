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


def original_value_order(csp, assignment):
    """
    find all variables that have not been assigned and return the first variable
    """
    unassigned_var = [vertex for vertex in csp.variables if vertex not in assignment]
    return unassigned_var[0]

def legal_values(csp, var, assignment):
    if csp.curr_domains:
        return len(csp.curr_domains[var])
    else:
        #Returns a count of the amount of conflicted numbers for the values in the domain
        return sum(map(bool,(csp.conflicted_num(assignment,var,val)==0 for val in csp.curr_domains[var])))
    
def mrv(csp,assignment):
    """
    Minimum remaing values heuristic for ordering variables used
    with the tie breaking rule.
    We want to select the variable with the fewest remaining legal values
    """
    unassign_min_rem_val=[]
    for variable in csp.variables:
        unassign_min_rem_val.append((variable,legal_values(csp, variable, assignment)))
    unassign_min_rem_val.sort(key=lambda unassign_min_rem_val: unassign_min_rem_val[1])
    return unassign_min_rem_val[0][0]
    
def unordered_domain_values(csp, variable, assignment):
    """
    Returns values in whatever order they currently are in
    """
    return csp.curr_domains[variable]

def lcv(csp, variable, assignment):
    """
    LCV sort the values by the amount of conflcits of the assignment in ascending order
    """
    return sorted(csp.curr_domains[variable],key=lambda value: csp.conflicted_num(assignment,variable,value))