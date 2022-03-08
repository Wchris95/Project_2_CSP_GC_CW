#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
based on AIMA code base

"""
from sortedcontainers import SortedSet

def forward_check(csp, variable, value, assignment, removals):
    """
    Remove neighbor domain values that are inconsistent with the variable that has been assigned
    As the neighbor values that are connected through a contraint
    we need to have the value we are assigning to be deleted
    from those neighbor's domain to maintian arc consistency
    """
    value = assignment[variable]
    for neighbor in csp.neighbors[variable]:
        if neighbor not in assignment:
            for domain_val in csp.curr_domains[neighbor]:
                if not csp.check_constraints(variable, value, neighbor, domain_val):
                    csp.prune(neighbor, domain_val, removals)
            #check if the domain is empty
            if len([value for value in csp.curr_domains[variable] if not value in removals[variable]])==0:
                return False
    return True
    
def dom_j_up(csp, queue):
    return SortedSet(queue, key=lambda t: -(len(csp.curr_domains[t[1]])))
    
def ac3(csp,queue,removals):
    if queue is None:
        queue = {(current_var,neighbor_var) for current_var in csp.variables for neighbor_var in csp.neighbors[current_var]}
    while queue:
        value1, value2 = queue.pop()
        revised = revise(csp, value1, value2, removals)
        if revised:
            if not csp.curr_domains[value1]:
                return False
            for neighbor_var in csp.neighbors[value1]:
                if neighbor_var != value2:
                    queue.add((neighbor_var,value2))
    return True
            
def revise(csp, Xi, Xj, removals):
    revise = False
    for x in csp.curr_domains[Xi]:
    # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
    # if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
       conflict = True
       for y in csp.curr_domains[Xj]:
           #check the if Xi and Xj conflict if this is true the value is exists and does not conflict
           if csp.check_constraints(Xi, x, Xj, y):
               conflict = False
               break
        #else if it conflicts we want to prune the value and add it to our removal val
       if conflict:
           csp.prune(Xi, x, removals)
           revise = True                   
    return revise

def maintain_arc_cons(csp, var, value, assignment, removals, constraint_propgation=ac3):
    return constraint_propgation(csp, {(var_neigh, var) for var_neigh in csp.neighbors[var]},removals)