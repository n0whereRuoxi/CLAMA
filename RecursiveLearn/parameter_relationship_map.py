def has_same_relationship(state_list1, state_list2, pair_s1, pair_s2):
    # Dictionary to store predicates for all elements
    s1_dict = {}
    s2_dict = {}

    # Loop through each state and find the predicates of the given pairs
    for state in state_list1:
        predicate, p1, p2 = state.split()
        if p1 not in s1_dict:
            s1_dict[p1] = set()
        s1_dict[p1].add((predicate, p2))

    for state in state_list2:
        predicate, p1, p2 = state.split()
        if p1 not in s2_dict:
            s2_dict[p1] = set()
        s2_dict[p1].add((predicate, p2))

    # Get predicates for specific pairs
    s1_pair_predicates = s1_dict.get(pair_s1[0], set())
    s2_pair_predicates = s2_dict.get(pair_s2[0], set())

    # Intersect predicates to check for common relationships
    common_predicates = {pred for pred, obj in s1_pair_predicates if (pred, pair_s1[1]) in s1_pair_predicates}
    common_predicates &= {pred for pred, obj in s2_pair_predicates if (pred, pair_s2[1]) in s2_pair_predicates}

    return len(common_predicates) > 0

# Test the function with provided data
state_list1 = ["predicate1 px1 px2", "predicate2 px1 pxa4"]
state_list2 = ["predicate1 py1 py2", "predicate3 py1 py4"]
pair_s1 = ("px1", "px2")
pair_s2 = ("py1", "py2")

print(has_same_relationship(state_list1, state_list2, pair_s1, pair_s2))  # Should output: True

# Let's test it with the modified state list where only one relationship matches
state_list2_modified = ["predicate1 py1 py2", "predicate2 py1 py4"]
print(has_same_relationship(state_list1, state_list2_modified, pair_s1, pair_s2))  # Should output: True
