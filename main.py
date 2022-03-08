from time import time

from search import backtrack_search
from heuristics import mrv, lcv, original_value_order, unordered_domain_values
from ac3 import forward_check, maintain_arc_cons
from coloringCSP import GraphColoringCSP

def solve(filepath,value_heuristics, domain_heuristics):
    csp = GraphColoringCSP.from_file(filepath)
    start = time()
    solution = backtrack_search(csp,{},value_heuristic=value_heuristics,domain_heuristic=domain_heuristics)
    end = time()
    print("Parsing Time: ", end-start)
    return solution

if __name__ == "__main__":
    filepath = "gc_78317103208800.txt"
    value_h = mrv
    value_order = lcv
    inference_methods = None
    solution = solve(
        filepath=filepath,
        value_heuristics=value_h,
        domain_heuristics=value_order
        )
    if solution:
        print(solution)
    else:
        print("No Solution Found")