import unittest
from search import backtrack_search, no_inf_backtrack_search
from heuristics import mrv, lcv, original_value_order, unordered_domain_values
from inferences import forward_check, maintain_arc_cons, revise, ac3
from coloringCSP import GraphColoringCSP
from fileParser import file_parse
from collections import defaultdict

class FileParserUnitTests(unittest.TestCase):
    def fileParseUnitTest(self):
        exp_colors = 4,
        exp_edges = [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), 
            (2, 4), (2, 6), (2, 7), (3, 5), (3, 6), (3, 7), (4, 5),
            (4, 6), (4, 7), (5, 6), (5, 7), (6, 7)]
        exp_vertices = [1,2,3,4,5,6,7]
        exp_neighbors = {1: {2, 3, 4, 5}, 
                     2: {1, 3, 4, 6, 7}, 
                     3: {1, 2, 5, 6, 7}, 
                     4: {1, 2, 5, 6, 7}, 
                     5: {1, 3, 4, 6, 7}, 
                     6: {2, 3, 4, 5, 7}, 
                     7: {2, 3, 4, 5, 6}}
        filename = "gc_1378296846561000.txt"
        file_class_obj = file_parse(filename)
        dataload = file_class_obj.parsed_data
        file_colors = dataload['colors']
        file_edges = dataload['edges']
        file_vertices = dataload['vertices']
        file_neighbors = dataload['neighbors']
        self.assertEqual(file_colors, exp_colors, "Unexpected colors: {colors}")
        self.assertEqual(len(exp_edges), len(file_edges), "Unexpected edge length: {len(file_edges)}")
        for edge in file_edges:
            self.assertIn(edge, exp_edges, "Unexpected edge: {edge}")
        self.assertEqual(len(exp_vertices),len(file_vertices),"Unexpected vertices length: {len(file_vertices)}")
        for vertex in file_vertices:
            self.assertIn(vertex,exp_vertices, "Unexpected vertex: {vertex}")
        self.assertDictEqual(file_neighbors,exp_neighbors, "Neighbor Error")
        
class testColoringCsp(unittest.TestCase):
    def test_count_conflicts(self):
        assignment = {
            0: 0,
            1: 2
        }
        csp = GraphColoringCSP.from_file("simple_test.txt")
        for variable in assignment:
            csp.assign(variable, assignment[variable],assignment)
        #there should be one conflict as within the text file one neighbor is 1,2
        conflicts = csp.conflicted_num(assignment, 2, 2)
        self.assertEqual(conflicts, 1, f"Expected 1 conflict, got {conflicts}")

class testHeuristics(unittest.TestCase):
    def test_lcv(self):
        assignment = {
            0: 0,
            1: 2
        }
        csp = GraphColoringCSP.from_file("simple_test.txt")
        for variable, value in assignment.items():
            csp.suppose(variable, value)
        self.assertEqual(lcv(csp,2,assignment)[0],1,"Value should be 0")
    
    def test_mrv(self):
        csp = GraphColoringCSP.from_file("simple_test.txt")
        assignment = {}
        variable = mrv(csp,assignment)
        self.assertEqual(variable, 2, f'MRV Test failed: value should be 2, value: {variable}')

class testInferenceAc3(unittest.TestCase):
    def test_forward_check(self):
        csp = GraphColoringCSP.from_file("simple_test.txt")
        assignment = {}
        removals=defaultdict(list)
        variable = 0
        value = 0
        csp.assign(variable, value, assignment)
        removals = csp.suppose(variable,value)
        removals, check_removals = forward_check(csp, variable=variable,value=value, assignment=assignment,removals=removals)
        self.assertTrue(check_removals)
        """domains should be 
        {0: [0]
         1: [1,2]
         2: [1,2]
         3: [0,1,2]}"""
        expected_domains = {0: [0],
         1: [1,2],
         2: [1,2],
         3: [0,1,2]}
        self.assertDictEqual(csp.curr_domains, expected_domains, "Domain values do not match")

        variable = 1
        value = 2
        removals=defaultdict(list)
        csp.assign(variable, value, assignment)
        removals = csp.suppose(variable,value)
        removals, check_removals = forward_check(csp, variable=variable,value=value,  assignment=assignment,removals=removals)
        self.assertTrue(check_removals)
        """
        domains should be 
        {0: [0]
         1: [2]
         2: [1]
         3: [0,1,2]}
        """
        expected_domains = {0: [0],
         1: [2],
         2: [1],
         3: [0,1,2]}
        self.assertDictEqual(csp.curr_domains, expected_domains, "Domain values do not match")
        """
        THIS PART SHOULD FAIL
        {0: [0]
         1: [2]
         2: []
         3: [1}
        """
        variable = 3
        value = 1
        removals=defaultdict(list)
        csp.assign(variable, value, assignment)
        removals = csp.suppose(variable,value)
        removals, check_removals = forward_check(csp, variable=variable,value=value, assignment=assignment,removals=removals)      
        self.assertFalse(check_removals)
        
    def test_revise(self):
        csp = GraphColoringCSP.from_file("simple_test.txt")
        assignment = {}
        removal = defaultdict(list)
        variable = 0
        value = 0
        csp.assign(variable, value, assignment)
        removals=csp.suppose(variable,value)
        expected_domains = {0: [0],
         1: [1,2],
         2: [1,2],
         3: [0,1,2]}
        # Loop through the neighbors to revise as needed
        queue = [(x, variable) for x in csp.neighbors[variable]]
        for vertex1, vertex2 in queue:
            revised, revise_bool = revise(csp, vertex1, vertex2)
            csp.apply_removals({vertex1:revised})
        self.assertDictEqual(csp.curr_domains, expected_domains)
    
    def test_ac3(self):
        csp = GraphColoringCSP.from_file("simple_test.txt")
        assignment = {}
        variable = 0
        value = 0
        csp.assign(variable, value, assignment)
        removals = csp.suppose(variable, value)
        expected_domains = {0: [0],
         1: [1,2],
         2: [1,2],
         3: [0,1,2]}
        queue = [(x, variable) for x in csp.neighbors[variable]]
        removals,ac3_bool = ac3(csp,removals,queue)
        csp.apply_removals(removals)
        self.assertDictEqual(csp.curr_domains, expected_domains)
        
class TestBacktracking(unittest.TestCase):
    """
    Unit tests for backtracking search. These tests are executed on the test files (more than just the Australia example)
    """
    def test_backtracking_search_no_inference(self):
        """
        Unit test for backtracking search without inference.
        This is implemented in a slightly different way via the 
        backtracking_search_no_inference method
        """
        files =["gc_78317094521100.txt",
        "gc_78317097930400.txt",
        "gc_78317097930401.txt",
        "gc_78317100510400.txt",
        "gc_78317103208800.txt",
        "gc_1378296846561000.txt"]
        no_solution = "gc_78317097930401.txt"
        for file in files:
            csp = GraphColoringCSP.from_file(file)
            solution = no_inf_backtrack_search(csp, assignment={},value_heuristic=mrv,domain_heuristic=unordered_domain_values) 
            if file == no_solution:
                self.assertIsNone(solution)
            else:
                self.assertTrue(csp.is_solution(solution))
    
    def test_backtracking_search_forward_checking(self):
        """
        Unit test for backtracking search with forward checking
        """
        files = ["gc_78317094521100.txt",
        "gc_78317097930400.txt",
        "gc_78317097930401.txt",
        "gc_78317100510400.txt",
        "gc_78317103208800.txt",
        "gc_1378296846561000.txt"]
        no_solution = "gc_78317097930401.txt"
        for file in files:
            csp = GraphColoringCSP.from_file(file)
            solution = backtrack_search(csp, assignment={},inference=forward_check)
            if file == no_solution:
                self.assertIsNone(solution)
            else:
                self.assertTrue(csp.is_solution(solution))
    
    def test_backtracking_search_mac(self):
        """
        Unit test for backtracking search with maintaining arc consistency using ac3
        """
        files = [
            "gc_78317094521100.txt",
            "gc_78317097930400.txt",
            "gc_78317097930401.txt",
            "gc_78317100510400.txt",
            "gc_78317103208800.txt",
            "gc_1378296846561000.txt"
            ]
        no_solution = "gc_78317097930401.txt"
        for file in files:
            csp = GraphColoringCSP.from_file(file)
            solution = backtrack_search(csp, assignment={},inference=maintain_arc_cons)
            if file == no_solution:
                self.assertIsNone(solution, f"Search returned solution for file {file}, although no solution exists")
            else:
                self.assertIsNotNone(solution, f"Search returned no solution for file {file}, although a solution exists")
                self.assertTrue(csp.is_solution(solution))
if __name__ == "__main__":
    test = unittest.main()
    
    