
# create csp class: variables, domains, constraints
# domains will be in regard to the neighbors of the current vertex
# constraints will need it's own separate class that is pulled into the
# csp class as the constraints for this problem is complex
# need to build out prune function to prune out values
from abc import ABC, abstractmethod
from typing import Dict, List
from colections import defaultdict

class gen_constraint(ABC):
    def __init__(self, variables: List())->None:
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
    #def get_arc_constraint(self):
          
    def backtrack(self, assignment: dict = {}):
        if len(assignment) == len(self.variables):
            return assignment

        # get all variables in the CSP but not in the assignment
        unassigned = [vertex for vertex in self.variables if vertex not in assignment]
        #we set the first variable to check
        first = unassigned[0]
        
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
        