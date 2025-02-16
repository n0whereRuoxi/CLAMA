# Import the PDDLReader and PDDLWriter classes from ../unified_planning/io.py
import sys
sys.path.append('/home/rli12314/scratch/')
sys.path.append('/home/rli12314/scratch/CurricuLAMA')
from unified_planning.io import PDDLReader, PDDLWriter

# make a class for PDDL parsing
class PDDLParser:
    def __init__(self, domain_file_dir, problem_file_dir):
        self.domain_file_dir = domain_file_dir
        self.problem_file_dir = problem_file_dir
        self.reader = PDDLReader()
        self.pddl_problem = self.reader.parse_problem(self.domain_file_dir, self.problem_file_dir)
        # print(self.pddl_problem)
        self.object_types = self.parse_object_types()
        self.initial_values = self.parse_initial_values()
        # self.goal = self.parse_goal()

    def parse_goal(self):
        goal = str(self.pddl_problem.goals[0])
        return goal

    def parse_object_types(self):
        object_types = {}
        for ty in self.pddl_problem.user_types:
            objects = list(self.pddl_problem.objects(ty))
            for o in objects:
                object_types[str(o)] = str(ty)
        return object_types

    # parse initial values
    def parse_initial_values(self):
        initial_values = {}
        for k, v in self.pddl_problem.explicit_initial_values.items():
            # print(type(k))
            initial_values[str(k)] = bool(v)
        # print(initial_values)
        return initial_values
    
    def write_pddl(self, problem_dir, domain):
        pddl_writer = PDDLWriter(self.pddl_problem)
        print("writing to " + problem_dir)
        pddl_writer.write_problem(problem_dir, domain)

if __name__ == "__main__":
    from landmark_graph_processor import LandmarkGraphProcessor
    # parse_object_types('./experiments/satellite/classical-domain.pddl', './experiments/satellite/classical_probs/prob1_strips.pddl')
    pddl_parser = PDDLParser('./experiments/satellite/classical-domain.pddl', './experiments/satellite/classical_probs/prob1_strips.pddl')
    print(pddl_parser.object_types)
    print(pddl_parser.initial_values)
    lm_processor = LandmarkGraphProcessor('./graph.dot')
    subgoals = lm_processor.subgoals 
    print(subgoals)