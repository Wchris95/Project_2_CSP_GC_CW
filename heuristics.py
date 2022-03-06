#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 21:59:14 2022

@author: chriswang
"""
# heuristics build out the LCV Heuristic and MRV heuristic
from csp import csp
from ac3 import ac3
from utils import first, argmin_random_tie

def first_unassigned_var(assignment, csp):
    return first([var for var in csp.variables if var not in assignment])

def mrv(assignment, csp):
    return argmin_random_tie([vertex for vertex in csp.variables if vertex not in assignment],
                             key=lambda var: num_legal_values(csp,var,assignment))

def num_legal_values(csp, var, assignment):
