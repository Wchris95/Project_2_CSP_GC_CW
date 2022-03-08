
"""
    create general constraint class: 
    create genearl csp class: variables, domains
    """ 
from abc import ABC, abstractmethod
from typing import Dict, List
from collections import defaultdict

class gen_constraint(ABC):
    def __init__(self, variables: List)->None:
        self.variables = variables
        
    @abstractmethod
    def is_satisfied(self, assignment: dict)->bool:
        pass

class csp(ABC):
    """This class describes finite domain CSP. 
    A CSP is specified by the following inputs:
        variables A list of variables (the vertex or vertices)
        domains A dict of {vertex:[next possible neighbors, ...]} entries
        constraints: mapping variables to constraints, modified by 
        add_constraint method
    """
    
    def __init__(self, variables: List, domains: Dict):
        self.variables = variables
        self.domains = domains
        self.constraints = defaultdict(list)
        self.assignment = {}
    
    #sanity check if the variables within our constraints is within our set of variables
    def add_constraint(self, constraint: gen_constraint) -> None:
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable in constraint not in CSP")
            else:
                self.constraints[variable].append(constraint)
                
    #check if the value assignment is consistent by checking all the 
    #constraints against it
    def is_consistent(self, variable, assignment: dict)-> bool:
        for constraint in self.constraints[variable]:
            if not constraint.is_satisfied(assignment):
                return False
        return True
      
    def backtrack(self, assignment: dict = {}):
        #if we have finished assigning values to our variables return assignment
        if len(assignment) == len(self.variables):
            return assignment
        # get all variables in the CSP but not in the assignment
        #inital set up to go through assignments
        unassigned = [vertex for vertex in self.variables if vertex not in assignment]
        #we set the first variable to check
        first = unassigned[0]
        #We go through our first key's domain from the domain dictionary
        for value in self.domains[first]:
            temp_assignment = assignment.copy()
            temp_assignment[first] = value
            # Check if assignment is consistent
            if self.is_consistent(first, temp_assignment):
                # We want to continue if the assignemnt is consistent
                # resursively go through the search again
                result = self.backtrack(temp_assignment)
                #if the result is not found we return None else return the result
                if result is not None:
                    return result
        return None
        