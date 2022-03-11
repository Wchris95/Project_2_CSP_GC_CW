#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
based on AIMA code base
https://github.com/aimacode/aima-python/blob/master/csp.py
"""
from sortedcontainers import SortedSet
from collections import defaultdict

def forward_check(csp, variable, value, assignment, removals):
    """
    Remove neighbor domain values that are inconsistent with the variable that has been assigned
    As the neighbor values that are connected through a contraint
    we need to have the value we are assigning to be deleted
    from those neighbor's domain to maintian arc consistency
    """
    removals = defaultdict(list)
    value = assignment[variable]
    for neighbor in csp.neighbors[variable]:
        if neighbor not in assignment:
            for domain_val in csp.curr_domains[neighbor]:
                if not csp.check_constraints(variable, value, neighbor, domain_val):
                    csp.prune(neighbor, domain_val, removals)
            #check if the domain is empty
            if not csp.curr_domains[neighbor]:
                for_check=False
                return removals, for_check
    for_check = True
    return removals,for_check;
    
def dom_j_up(csp, queue):
    return SortedSet(queue, key=lambda t: -(len(csp.curr_domains[t[1]])))
    
def ac3(csp,removals,queue=None):
    removals=defaultdict(list)
    if queue is None:
        queue = [(current_var,neighbor_var) for current_var in csp.variables for neighbor_var in csp.neighbors[current_var]]
    while queue:
        (value1, value2) = queue.pop()
        revised, rev_bool = revise(csp, value1, value2,removals)
        if rev_bool:
                removals[value1].extend(revised)
                if not csp.curr_domains[value1]:
                    arc3_bool = False
                    return removals, arc3_bool
                for neighbor_var2 in csp.neighbors[value1]:
                    if neighbor_var2 != value2:
                        queue.append((neighbor_var2,value1))
    arc3_bool = True
    return removals, arc3_bool;
            
def revise(csp, Xi, Xj, removals):
    revise_bool = False
    revised = []
    for x in csp.curr_domains[Xi]:
    # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
    # if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
       conflict = False
       for y in csp.curr_domains[Xj]:
           #check the if Xi and Xj conflict if this is true the value is exists and does not conflict
           if csp.check_constraints(Xi, x, Xj, y):
               conflict = True;
           if conflict:
               break
        #else if it conflicts we want to prune the value and add it to our removal val
       if not conflict:
           revise_bool = True   
           revised.append(x)
    return revised, revise_bool;

def maintain_arc_cons(csp, variable,value, assignment, removals, constraint_propgation=ac3):
    return constraint_propgation(csp,removals,queue=[(variable, var_neigh) for var_neigh in csp.neighbors[variable]])