#ifndef LANDMARKS_LANDMARK_GRAPH_H
#define LANDMARKS_LANDMARK_GRAPH_H

#include "landmark.h"

#include "../task_proxy.h"

#include "../utils/hash.h"
#include "../utils/memory.h"

#include <cassert>
#include <list>
#include <map>
#include <set>
#include <unordered_map>
#include <unordered_set>
#include <vector>

namespace landmarks {
enum class EdgeType {
    /*
      NOTE: The code relies on the fact that larger numbers are stronger in the
      sense that, e.g., every greedy-necessary ordering is also natural and
      reasonable. (It is a sad fact of terminology that necessary is indeed a
      special case of greedy-necessary, i.e., every necessary ordering is
      greedy-necessary, but not vice versa.
    */
    NECESSARY = 3,
    GREEDY_NECESSARY = 2,
    NATURAL = 1,
    REASONABLE = 0
};

class LandmarkNode {
    int id;
    Landmark landmark;
public:
    LandmarkNode(Landmark &&landmark)
        : id(-1), landmark(std::move(landmark)) {
    }

    std::unordered_map<LandmarkNode *, EdgeType> parents;
    std::unordered_map<LandmarkNode *, EdgeType> children;

    int get_id() const {
        return id;
    }

    // TODO: Should possibly not be changeable
    void set_id(int new_id) {
        assert(id == -1 || new_id == id);
        id = new_id;
    }

    // TODO: Remove this function once the LM-graph is constant after creation.
    Landmark &get_landmark() {
        return landmark;
    }

    const Landmark &get_landmark() const {
        return landmark;
    }
};

class LandmarkGraph {
public:
    /*
      TODO: get rid of this by removing get_nodes() and instead offering
      functions begin() and end() with an iterator class, so users of the
      LandmarkGraph can do loops like this:
        for (const LandmarkNode &n : graph) {...}
     */
    using Nodes = std::vector<std::unique_ptr<LandmarkNode>>;
private:
    int num_conjunctive_landmarks;
    int num_disjunctive_landmarks;

    utils::HashMap<FactPair, LandmarkNode *> simple_landmarks_to_nodes;
    utils::HashMap<FactPair, LandmarkNode *> disjunctive_landmarks_to_nodes;
    Nodes nodes;

    void remove_node_occurrences(LandmarkNode *node);

public:
    /* This is needed only by landmark graph factories and will disappear
       when moving landmark graph creation there. */
    LandmarkGraph();

    // bool is_fact_true_in_state(FactPair the_fact_pair, State initial_state){
    //     for (std::size_t i = 0; i < initial_state.size(); i++) {
    //         FactProxy fact_proxy = initial_state[i];
    //         FactPair fact_pair = fact_proxy.get_pair();
    //         if (the_fact_pair == fact_pair) {
    //             return true;
    //         }
    //     }
    //     return false;
    // }
    // // pretty print
    // void print_landmarks(const std::shared_ptr<AbstractTask> &task) {
    //     utils::g_log << "printing landmarks..." << "\n";        
    //     for (auto &node : nodes) {
    //         Landmark lm = node->get_landmark();
    //         for (auto &fact : lm.facts) {
    //             utils::g_log << task->get_fact_name(fact) << " ";
    //         }
    //         for (const auto &child : node->children) {
    //             utils::g_log << "child: ";
    //             LandmarkNode &child_node = *(child.first);
    //             Landmark lmchild = child_node.get_landmark();
    //             for (auto &fact : lmchild.facts) {
    //                 utils::g_log << task->get_fact_name(fact) << " ";
    //             }
    //         }
    //         utils::g_log << "\n";
    //     }
    // }
    // // save landmarks
    // void save_landmarks(const std::shared_ptr<AbstractTask> &task) {
    //     std::string filename = "landmark_graph.json";
    //     utils::g_log << "Saving filtered landmark graph to " << filename << std::endl;
    //     std::ofstream outfile(filename);
    //     if (outfile.rdstate() & std::ofstream::failbit) {
    //         std::cerr << "Failed to open plan file: " << filename << std::endl;
    //         utils::exit_with(utils::ExitCode::SEARCH_INPUT_ERROR);
    //     }
    //     outfile << "{";
    //     TaskProxy task_proxy(*task);
    //     State initial_state = task_proxy.get_initial_state();
    //     int i = 0;
    //     int j = 0;
    //     int k = 0;
    //     int l = 0;
    //     for (auto &node : nodes) {
    //         Landmark lm = node->get_landmark();
    //         // assert(lm.facts.size() == 1);
    //         bool l_bIsInInitialState = true;
    //         for (auto &fact : lm.facts) {
    //             if (not is_fact_true_in_state(fact, initial_state)) 
    //                 l_bIsInInitialState = false;
    //         }
    //         if (not l_bIsInInitialState) {
    //             if (i != 0) outfile << ",";
    //             l = 0;
    //             outfile << "\"";
    //             for (auto &fact : lm.facts) {
    //                 if (l != 0) outfile << "||";
    //                 outfile << task->get_fact_name(fact);
    //                 l = l + 1;
    //             }
    //             outfile << "\":";
    //             outfile << "[";
    //             j = 0;
    //             for (const auto &child : node->children) {
    //                 if (j != 0) outfile << ",";
    //                 LandmarkNode &child_node = *(child.first);
    //                 Landmark lmchild = child_node.get_landmark();
    //                 k = 0;
    //                 outfile << "[";
    //                 if (not is_fact_true_in_state(lmchild.facts[0], initial_state)) {
    //                     for (auto &fact : lmchild.facts) {
    //                         if (k != 0) outfile << ",";
    //                         outfile << "\"" << task->get_fact_name(fact) << "\"";
    //                         k = k + 1;
    //                     }
    //                 }
    //                 outfile << "]";
    //                 j = j + 1;
    //             }
    //             outfile << "]";
    //             i = i + 1;
    //         }
    //     }
    //     outfile << "}";
    // }


    // std::string find_atom_name(std::string s_fact_pair) {
    //     int start = s_fact_pair.find(" ");
    //     int end = s_fact_pair.find("(");
    //     std::string token = s_fact_pair.substr(start + 1, end - start - 1);
    //     // utils::g_log << "Predicate: " << token << "\n";
    //     return token;
    // }

    // std::string find_atom_parameter(std::string s_fact_pair) {
    //     int start = s_fact_pair.find("(");
    //     int end = s_fact_pair.find(")");
    //     std::string token = s_fact_pair.substr(start + 1, end - start - 1);
    //     // utils::g_log << "Parameter: " << token << "\n";
    //     return token;
    // }


    // needed by both landmarkgraph-factories and non-landmarkgraph-factories
    const Nodes &get_nodes() const {
        return nodes;
    }
    // needed by both landmarkgraph-factories and non-landmarkgraph-factories
    int get_num_landmarks() const {
        return nodes.size();
    }
    /* This is needed only by landmark graph factories and will disappear
       when moving landmark graph creation there. */
    int get_num_disjunctive_landmarks() const {
        return num_disjunctive_landmarks;
    }
    /* This is needed only by landmark graph factories and will disappear
       when moving landmark graph creation there. */
    int get_num_conjunctive_landmarks() const {
        return num_conjunctive_landmarks;
    }
    /* This is needed only by landmark graph factories and will disappear
       when moving landmark graph creation there. */
    int get_num_edges() const;

    // only needed by non-landmarkgraph-factories
    LandmarkNode *get_node(int index) const;
    // only needed by non-landmarkgraph-factories
    LandmarkNode *get_node(const FactPair &fact) const;
    /* This is needed only by landmark graph factories and will disappear
       when moving landmark graph creation there. */
    LandmarkNode &get_simple_landmark(const FactPair &fact) const;
    /* This is needed only by landmark graph factories and will disappear
       when moving landmark graph creation there. */
    LandmarkNode &get_disjunctive_landmark(const FactPair &fact) const;

    /* This is needed only by landmark graph factories and will disappear
       when moving landmark graph creation there.  It is not needed by
       HMLandmarkFactory*/
    bool contains_simple_landmark(const FactPair &lm) const;
    /* Only used internally. */
    bool contains_disjunctive_landmark(const FactPair &lm) const;
    /* This is needed only by landmark graph factories and will disappear
       when moving landmark graph creation there.  It is not needed by
       HMLandmarkFactory*/
    bool contains_overlapping_disjunctive_landmark(const std::set<FactPair> &lm) const;
    /* This is needed only by landmark graph factories and will disappear
       when moving landmark graph creation there. */
    bool contains_identical_disjunctive_landmark(const std::set<FactPair> &lm) const;
    /* This is needed only by landmark graph factories and will disappear
       when moving landmark graph creation there.  It is not needed by
       HMLandmarkFactory*/
    bool contains_landmark(const FactPair &fact) const;

    /* This is needed only by landmark graph factories and will disappear
       when moving landmark graph creation there. */
    LandmarkNode &add_landmark(Landmark &&landmark);
    /* This is needed only by landmark graph factories and will disappear
       when moving landmark graph creation there. */
    void remove_node(LandmarkNode *node);
    void remove_node_if(
        const std::function<bool (const LandmarkNode &)> &remove_node_condition);

    /* This is needed only by landmark graph factories and will disappear
       when moving landmark graph creation there. */
    void set_landmark_ids();
};
}

#endif
