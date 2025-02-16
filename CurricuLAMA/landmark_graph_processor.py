import json
import networkx as nx
import re
import pydot
import random
import matplotlib.pyplot as plt
import graphviz

# make a class that read landmark graph from DOT format file and generate subgoals
class LandmarkGraphProcessor:
    def __init__(self, filename, PDDL_Problem):
        self.filename = filename
        self.PDDL_Problem = PDDL_Problem
        self.landmark_graph = self.__load_DOT()
        self.subgoals = self.__get_subgoals()
        self.config = "greedy"

    def save(self):
        # save nx.DiGraph() as png
        nx.draw(self.landmark_graph, with_labels=True)
        plt.savefig("landmark_graph.png")

    def is_lm_true_in_initial_state(self, lm):
        # a lm looks like 'Atom power_avail(sat001)' or 'Atom power_on(inst001-000) | Atom power_on(inst001-003) | Atom power_on(inst001-004)'
        lm_true = False
        if '|' in lm:
            lm_disjunction = lm.split('|')
            for lm in lm_disjunction:
                lm = lm.strip()
                lm_true = self.__is_atom_true_in_initial_state(lm)
                if lm_true:
                    break
        else:
            lm_true = self.__is_atom_true_in_initial_state(lm)
        return lm_true

    def __is_atom_true_in_initial_state(self, atom):
        """
        an atom can be Atom or NegatedAtom, e.g., Atom have_image(dir000, mode000), NegatedAtom have_image(dir000, mode000)
        the initial state dictionary looks like {'pointing(sat000, dir002)': True, 'pointing(sat001, dir003)': True}
        check if the atom is true in initial state
        """
        print('  Evaluating atom: ', atom)
        atom = atom.strip()
        if atom.startswith('Atom'):
            atom = atom[5:].strip()
            print("  " + atom)
            if atom in self.PDDL_Problem.initial_values:
                return self.PDDL_Problem.initial_values[atom]
            else:
                return False
        elif atom.startswith('NegatedAtom'):
            atom = atom[11:].strip()
            print("  " + atom)
            if atom in self.PDDL_Problem.initial_values:
                return not self.PDDL_Problem.initial_values[atom]
            else:
                return True

    # load graphviz DOT format from file
    def __load_DOT(self):
        dot_graph = pydot.graph_from_dot_file(self.filename)[0]
        nx_graph = nx.DiGraph()
        true_lms = []
        for node in dot_graph.get_nodes():
            if node.get_name() != "\"\\n\"":
                node_name = node.get_name()
                node_label = node.get_label().replace('"', '') 
                print("Checking landmark: ", node_name, node_label)
                lm_is_true = self.is_lm_true_in_initial_state(node_label)
                print("It is " + str(lm_is_true) + "\n")
                if not lm_is_true:
                    node_attrs = {'label': node_label}
                    nx_graph.add_node(node_name, **node_attrs)
                else:
                    true_lms.append(node_name)
        for edge in dot_graph.get_edges():
            if edge.get_source() in true_lms or edge.get_destination() in true_lms:
                continue
            # print(edge.get_source(), edge.get_destination(), edge.get_label())
            edge_label = edge.get_label()
            edge_attrs = {'label': edge_label}
            nx_graph.add_edge(edge.get_source(), edge.get_destination(), **edge_attrs)
        return nx_graph
    
    # iterate though the landmark_graph and get subgoals
    def __get_subgoals(self):
        subgoals = []
        while self.landmark_graph.nodes():
            # get a node with no predecessor
            node_feature = {}
            for node in self.landmark_graph.nodes():
                # print(node, len(list(landmark_graph.predecessors(node))))
                if len(list(self.landmark_graph.predecessors(node))) == 0:
                    if node not in node_feature.keys():
                        node_feature[node] = 0
                        for successor in self.landmark_graph.successors(node):
                            # print(self.landmark_graph.edges[node, successor]['label'])
                            # if self.landmark_graph.edges[node, successor]['label'] == "\"n\"":
                            node_feature[node] += 1
                        print(self.landmark_graph.nodes[node]['label'], node_feature[node])
            print("Nodes with no predecessor and its neccessary edges: ", node_feature)
            if not node_feature:
                break
            else:
                # print the nodes with no predecessor and its neccessary edges
                # print("Nodes with no predecessor and its neccessary edges: ", node_feature)
                # choose the one with maximum number of neccessary edges
                node_to_remove = max(node_feature, key=node_feature.get)
            label = self.landmark_graph.nodes[node_to_remove]['label']
            # remove disjunctive nodes
            if '|' in label:
                self.landmark_graph.remove_node(node_to_remove)
                continue
                # label = random.choice(label.split('|')).strip()
            # remove Atom or NegatedAtom from the begining of the label
            if label.startswith('Atom'):
                label = label[5:].strip()
            elif label.startswith('NegatedAtom'):
                label = label[11:].strip()
            subgoals.append(label)
            self.landmark_graph.remove_node(node_to_remove)
        # now the subgoals look like ['power_on(inst001-000)', 'calibrated(inst001-003)', 'have_image(dir000, mode000)']
        # convert the format into [['power_on', 'inst001-000'], ['calibrated', 'inst001-003'], ['have_image', 'dir000', 'mode000']]
        print("Un-cleaned subgoals: ", subgoals)
        subgoals_cleaned = []
        for subgoal in subgoals:
            atom_parse = re.findall(r"[\w-]+", subgoal)
            subgoals_cleaned.append(atom_parse)
        print('Cleaned subgoals: ', subgoals_cleaned)
        return subgoals_cleaned

def read_landmark_graph(filename):
    print("read_landmark_graph...")
    f = open (filename, "r")
    data = json.load(f)
    # print(data)
    landmark_graph = nx.DiGraph()
    for i in data.keys():
        # print(i)
        if not data[i]:
            landmark_graph.add_node(i)
        else:
            for child in data[i]:
                landmark_graph.add_edge(i, child[0])
    f.close()
    # # Convert the DiGraph object to an AGraph object
    # agraph = nx.nx_agraph.to_agraph(landmark_graph)
    # # Write the AGraph object to a file in DOT format
    # agraph.write('graph.dot')
    # dot = nx.drawing.nx_pydot.to_pydot(landmark_graph)
    # dot.write('graph.dot')
    return landmark_graph

def get_subgoals_from_landmark_graph(landmark_graph):
    subgoals = []
    # print(landmark_graph.nodes())
    while landmark_graph.nodes():
        temp = []
        # get a node with no predecessor
        for node in landmark_graph.nodes():
            # print(node, len(list(landmark_graph.predecessors(node))))
            if len(list(landmark_graph.predecessors(node))) == 0:
                temp.append(node)
        for node in temp:
            landmark_graph.remove_node(node)
        # print(temp)
        temp_remove_disjunction = [random.choice(node.split("^")) for node in temp]
        # print(temp_remove_disjunction)
        subgoals += temp_remove_disjunction
    # print("subgoals: ", subgoals)
    subgoals_cleaned = []
    for subgoal in subgoals:
        atom = re.search(r"Atom (.+)", subgoal).group(1)
        # print(atom)
        atom_parse = re.findall(r"[\w-]+", atom)
        # print(atom_parse)
        subgoals_cleaned.append(atom_parse)
    return subgoals_cleaned

if __name__ == "__main__":
    from PDDL_parser import PDDLParser
    # parse_object_types('./experiments/satellite/classical-domain.pddl', './experiments/satellite/classical_probs/prob1_strips.pddl')
    PDDL_problem = PDDLParser('./experiments/satellite/classical-domain.pddl', './experiments/satellite/classical_probs/prob1_strips.pddl')
    print(PDDL_problem.object_types)
    print(PDDL_problem.initial_values)
    lm_processor = LandmarkGraphProcessor('./graph.dot', PDDL_problem)
    subgoals = lm_processor.subgoals 
    # old_subgoals = get_subgoals_from_landmark_graph(lm_processor.landmark_graph)
    print("Subgoals: ", subgoals)
    # print("Old subgoals: ", old_subgoals)
