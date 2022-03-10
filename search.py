from heuristics import lcv, mrv, original_value_order, unordered_domain_values
from inferences import maintain_arc_cons, forward_check
from collections import defaultdict
from coloringCSP import GraphColoringCSP
"""
Follows AIMA implementation of backtrack search
Within this module we want to bring together the backtrack search from csp
Then uses mrv and lcv from heuristics module
Also incorporate ac3 within our backtracking funciton that incorporates all these modules
"""

def backtrack_search(csp, assignment, value_heuristic=mrv, domain_heuristic=lcv,inference = maintain_arc_cons):
    if csp.is_solution(assignment):
        return assignment
    variable = value_heuristic(csp, assignment)
    for value in domain_heuristic(csp, variable, assignment):
        if csp.conflicted_num(assignment, variable, value) == 0:
            csp.assign(variable, value, assignment)
            removals = csp.suppose(variable, value)
            removals, infer_check = inference(csp, variable, value, assignment, removals)
            if infer_check and csp.is_consistent(variable, assignment):
                #instead of applying the removals within the inferences 
                #applying it within the search helps track it easier
                result = backtrack_search(csp, assignment, value_heuristic, domain_heuristic, inference)
                if result is not None:
                    return result
                csp.restore(removals)
            csp.unassign(variable, assignment)
    return None

    
def no_inf_backtrack_search(csp, assignment, value_heuristic, domain_heuristic):
    if csp.is_solution(assignment):
        return assignment
    variable = value_heuristic(csp, assignment)
    for value in domain_heuristic(csp, variable, assignment):
        temp_assignment = assignment.copy()
        temp_assignment[variable] = value
        # Check if assignment is consistent
        if csp.is_consistent(variable, temp_assignment):
              # We want to continue if the assignemnt is consistent
              # resursively go through the search again
              result = no_inf_backtrack_search(csp, temp_assignment, value_heuristic, domain_heuristic)
              #if the result is not found we return None else return the result
              if result is not None:
                  return result
    return None
if __name__ == "__main__":
    files = ["gc_78317103208800.txt"]
    no_solution = "gc_78317097930401.txt"
    for file in files:
        csp = GraphColoringCSP.from_file(file)
        solution = backtrack_search(csp, assignment={},inference=maintain_arc_cons)
        print(f"{file} ->{solution}\n")
