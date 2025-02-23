import os

# -a <num>    number of airplanes
# -c <num>    number of cities (minimal 1)
# -s <num>    city size (minimal 1)
# -p <num>    number of packages (minimal 1)
# -t <num>    number of trucks (optional, default and minimal: same as number of cities;
#             there will be at least one truck per city)
# -r <num>    random seed (minimal 1, optional)

for i in range(1000):
    for hierarchical in [0,1]:
        folder = "classical_probs" if not hierarchical else "htn_probs"
        problem_type = "strips" if not hierarchical else "htn"
        random_seed = i+1
        os.system("../../../pddl-generators/logistics_typed/logistics -a 1 -c 3 -s 2 -p 1 -r {} -h {} > ./{}/prob{}_{}.pddl".format(
            random_seed, hierarchical, folder, i, problem_type))