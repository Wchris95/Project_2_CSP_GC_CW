from time import time

from search import backtrack_search, no_inf_backtrack_search
from heuristics import mrv, lcv, original_value_order, unordered_domain_values
from inferences import forward_check, maintain_arc_cons
from coloringCSP import GraphColoringCSP
import argparse 

def solve(filepath,value_heuristics, domain_heuristics):
    csp = GraphColoringCSP.from_file(filepath)
    start = time()
    solution = backtrack_search(csp,{},value_heuristic=value_heuristics,domain_heuristic=domain_heuristics)
    end = time()
    print("Parsing Time: ", end-start)
    return solution

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CSP Graph Color Program")
    parser.add_argument('-variable','--varHeuristic', 
                        choices=['mrv','original_value_order'],
                        default='mrv'
                        )
    parser.add_argument('-value','--valHeuristic',
                    choices=['lcv', 'orignal_order'],
                    default="lcv")
    parser.add_argument('-inf','--inference',
                    choices=['maintain_arc_cons', 'forward_check','None'],
                    default="forward_check")
    varHeuristicDict = {'mrv':mrv,'original value order':original_value_order}
    valueHeuristicDict = {'lcv':lcv, 'orignal_order':unordered_domain_values}
    inferenceDict = {'maintain_arc_cons':maintain_arc_cons,'forward_check':forward_check, 'None':None}
    arguments = parser.parse_args()
    varHeuristic = varHeuristicDict.get(arguments.varHeuristic)
    valHeuristic = valueHeuristicDict.get(arguments.valHeuristic)
    inference = inferenceDict.get(arguments.inference)
    files = ["gc_78317094521100.txt",
    "gc_78317097930400.txt",
    "gc_78317097930401.txt",
    "gc_78317100510400.txt",
    "gc_78317103208800.txt",
    "gc_1378296846561000.txt"]
    no_solution = "gc_78317097930401.txt"
    for file in files:
        csp = GraphColoringCSP.from_file(file)
        if inference == None:
            start_time = time()
            solution = no_inf_backtrack_search(csp,assignment={},value_heuristic=varHeuristic,domain_heuristic=valHeuristic)
            end_time = time()
            print(f'Search Time: {end_time-start_time}')
        else:
            start_time = time()
            solution = backtrack_search(csp, assignment={}, value_heuristic=varHeuristic,domain_heuristic=valHeuristic,inference=inference)
            end_time = time()
            print(f'Search Time: {end_time-start_time}')
        if solution:
            print(f"\nSolution for {file} {solution}\n")
        else:
            print(f"\nNo solution for {file} \n")
