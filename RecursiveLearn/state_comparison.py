def parse_state(state):
    """
    Parses the state into a dictionary of relationships where each key-value pair represents a relationship between variables.
    The first variable is considered to be related to the second, the second to the third, and so on.
    """
    relationship = {}
    for condition in state:
        # Split the condition into words and ignore the condition name
        variables = condition.split()[1:]
        for i in range(len(variables) - 1):
            relationship[variables[i]] = variables[i + 1]
    return relationship

def compare_entire_structure(s1, s2):
    """
    Compares the entire structure of two states s1 and s2.
    Checks if every relationship in s1 has an equivalent relationship in s2 and vice versa.
    """
    rel_s1 = parse_state(s1)
    rel_s2 = parse_state(s2)

    # Comparing the number of relationships
    if len(rel_s1) != len(rel_s2):
        return False

    # Comparing each relationship
    for key, value in rel_s1.items():
        if key not in rel_s2 or rel_s1[key] != rel_s2[key]:
            return False

    for key, value in rel_s2.items():
        if key not in rel_s1 or rel_s2[key] != rel_s1[key]:
            return False

    return True

if __name__ == "__main__":
    # Define the states
    s1 = [ "condition a b", "other_condition b c d", "condition e f" ]
    s2 = [ "condition x y", "condition y z w", "other_condition v u" ]

    # Compare the entire structures of the states
    print(compare_entire_structure(s1, s2))
    s1 = { "condition a b", "condition b c d", "other_condition e f" }
    s2 = { "condition x y", "condition y z w", "other_condition v u" }
    # Compare the entire structures of the states
    print(compare_entire_structure(s1, s2))