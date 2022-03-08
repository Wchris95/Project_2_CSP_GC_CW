from heuristics import lcv, mrv, original_value_order, unordered_domain_values
from ac3 import maintain_arc_cons, forward_check


"""
Within this module we want to bring together the backtrack search from csp
Then uses mrv and lcv from heuristics module
Also incorporate ac3 within our backtracking funciton that incorporates all these modules
"""
def backtrack_search(csp, assignment, value_heuristic=mrv, domain_heuristic=lcv,inference = maintain_arc_cons):
    if csp.is_solution(assignment):
        return assignment
    variable = value_heuristic(csp, assignment)
    if inference == None:
        for value in domain_heuristic(csp, variable, assignment):
            temp_assignment = assignment.copy()
            temp_assignment[variable] = value
            # Check if assignment is consistent
            if csp.is_consistent(variable, temp_assignment):
                # We want to continue if the assignemnt is consistent
                # resursively go through the search again
                result = backtrack_search(csp, assignment, value_heuristic, domain_heuristic)
                #if the result is not found we return None else return the result
                if result is not None:
                    return result
        return None
    else:
        for value in domain_heuristic(csp, variable, assignment):
            if csp.conflicted_num(assignment, variable, value):
                csp.assign(variable, value, assignment)
                removals = csp.suppose(variable, value)
                if inference(csp, variable, value, assignment, removals):
                    result = backtrack_search(csp, assignment, value_heuristic, domain_heuristic, inference)
                    if result is not None:
                        return result
                csp.restore(removals)
        csp.unassign(variable, assignment)
        return None
    