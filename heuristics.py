#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 21:59:14 2022

@author: chriswang
"""
# heuristics build out the LCV Heuristic and MRV heuristic
from csp import csp
from ac3 import ac3

def inference(csp, variable, assignment)