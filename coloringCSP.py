#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Tuple, List, Union, Set
from fileParser import file_parse
from collections import defaultdict

class GraphColoringRestraint:
    """
    GraphColoringRestraint class to set up constraints
    variables -> the vertices given to us from the file parser
    domains -> our colors set as a list
    assignments -> set up as a dict where vertex is the key and color is value
    constraints -> the vertices that are adjacent to each other(edges) from
    our file parser
    """
    def __init__(self, vertex1, vertex2):
        self.variables = [vertex1, vertex2] 
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        
    def is_satisfied(self, assignment:dict)-> bool:
        #checks if either vertcies have been assigned a color if not then return true
        if self.vertex1 not in assignment or self.vertex2 not in assignment:
            return True
        #if both have been assigned check that both are not the same color
        return assignment[self.vertex1] != assignment[self.vertex2]

class GraphColoringCSP:
    """
    GraphColoringCSP
    inputs:
        edges -> Edges we obtain from our text file
        vertices -> the variables we create from the file parser module
        colors -> initially a int value we use range(colors) to product domains
        we then use add_constraint from the csp module with the use of the 
        GraphcoloringRestraint subclass to form the vertex 1 and vertex 2 
        We don't have to worry about repeating edges such as (1,5) (5,1) as
        we filter these out within the file_parse module
    """
    def __init__(self, vertices: set, edges: Union[list, set], colors: int, neighbors:dict=None) -> None:
        self.edges = edges     
        self.constraints = defaultdict(list)
        self.colors = colors
        self.neighbors = neighbors
        self.variables = vertices
        self.domains =  {vertex: list(range(colors)) for vertex in self.variables}
        self.curr_domains = self.domains
        self.nassigns = 0
        for v1, v2 in self.edges:
            self.add_constraint(GraphColoringRestraint(v1,v2))
            
    def add_constraint(self, constraint) -> None:
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable in constraint not in CSP")
            else:
                self.constraints[variable].append(constraint)
    #check if the value assignment is consistent by checking all the 
    #constraints against it
    def assign(self, var, val, assignment):
        """add {var: val} to assignment; discard the old val if any"""
        assignment[var] = val
        self.nassigns +=1
    
    """
    Removes the value based on variable key passed in
    """
    def unassign(self, var, assignment):
        if var in assignment:
            del assignment[var]
 
    def is_consistent(self, variable, assignment: dict)-> bool:
        #all(con.holds(assignment)
                   #for con in self.constraints
                   #if all(v in assignment for v in con.scope))
        """
        Check all constraints 
        if the constraint is satisfied by checking if each constraint(vertex1,vertex2)
        has been assigned yet if both of them have been assigned then check that they
        are not the same color
        """
        for constraint in self.constraints[variable]:
            if not constraint.is_satisfied(assignment):
                return False
        return True
    
    def check_constraints(self, X, x, Y, y):
        return x != y
    
    def display(self, assignment):
        print('CSP:',self,'with assignment:',assignment)
    
    def suppose(self, var, value):
        """Start acculamting inferences from asssuming var = value"""
        removals = [(var,comp_val) for comp_val in self.curr_domains[var] if comp_val != value]
        self.curr_domains[var] = [value]
        return removals
    
    def prune(self, var, val, removals):
        """Rule out var = value"""
        self.curr_domains[var].remove(val)
        if removals is not None:
            removals[var].append(val)
        return removals
    
    def conflicted_num(self, assignment, var, val):
        #def conflict(var2):
           #return var2 in assignment and not self.constraints(var, val, var2, assignment[var2])

        #return count(conflict(v) for v in self.neighbors[var])
        assignment_check = assignment.copy()
        assignment_check[var] = val
        conflict_count = 0
        for neighbor in self.neighbors[var]:
            if neighbor in assignment and not self.is_consistent(neighbor, assignment):
                conflict_count+=1
        return conflict_count
      
    def restore(self, removals):
        """Undo a supposition and all inferences on it"""
        for B, b in removals.items():
            self.curr_domains[B].append(b)
   
    def is_solution(self, assignment):
        #we want to check if the assignment is empty first
        if not assignment:
            return False
        return (len(assignment) == len(self.variables)
                and all(self.conflicted_num(assignment,variables, assignment[variables]) == 0
                        for variables in self.variables))
    
    def apply_removals(self,removals):
        for variable, values in removals.items():
            for value in values:
                self.curr_domains[variable].remove(value)
            
    @classmethod
    def from_file(cls, filename):
        fileData = file_parse(filename=filename)
        return cls(**fileData.parsed_data)
            