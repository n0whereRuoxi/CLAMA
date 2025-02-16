from HTN_parser import PDDLParser
import sys
import argparse
import time
# domain = "blocks_recursion"
def generate_probs(domain, alg, enforce_extra_precondition):
    if alg == 'curriculama':
        base_dir = '/home/rli12314/scratch/CurricuLAMA/experiments'
    else:
        base_dir = '/home/rli12314/scratch/experiment_HTN-Maker'
    # save the run time for each problem
    with open(base_dir + "/{}/time_log_{}.txt".format(domain, domain), "w") as run_time_file:
        # save number of methods in to a txt file 
        with open(base_dir + "/{}/number_of_methods.txt".format(domain), "w") as num_methods_file:
            for i in range(5):
                for j in range(150):
                    print(i,j)
                    # set start time
                    start_time = time.time()
                    domain_dir = base_dir + "/{}/results/result_domain_htn_{}.pddl".format(domain, i*200+j)
                    with open(domain_dir, "r") as pddl_file:
                        pddl_content = pddl_file.read()
                        # print(pddl_content)
                        # Parse the PDDL file
                        parser = PDDLParser(pddl_content, enforce_remove_methods=True, enforce_extra_precondition=enforce_extra_precondition)
                        original_num = len(parser.parsed_methods)
                        parser.generalize_methods()
                        print("\t", original_num, len(parser.generalized_methods), len(parser.generalized_methods) + len(parser.parsed_methods))
                        num_methods_file.write(str(len(parser.generalized_methods) + len(parser.parsed_methods))+ '\n')
                        new_domain_dir = base_dir + "/{}/results/result_domain_htn_{}_generalized.pddl".format(domain, i*200+j)
                        parser.write_PDDL(domain_dir, new_domain_dir)
                        # wait = input("PRESS ENTER TO CONTINUE.")
                    end_time = time.time()
                    # runtime in ms
                    run_time = (end_time - start_time) * 1000
                    run_time_file.write(str(run_time) + '\n')
if __name__ == "__main__":
    # get three arguments, domain (str), alg (str), and enforce_extra_precondition (bool)
    # use argparse
    parser = argparse.ArgumentParser(description='Generate problems for a domain')
    parser.add_argument('domain', type=str, help='The domain to generate problems for')
    parser.add_argument('alg', type=str, help='The algorithm to run')
    parser.add_argument('--enforce_extra_precondition', action='store_true', help='Whether to enforce extra preconditions')
    args = parser.parse_args()
    domain = args.domain
    alg = args.alg
    enforce_extra_precondition = args.enforce_extra_precondition
    print(domain, alg, enforce_extra_precondition)
    # pause the program
    # wait = input("PRESS ENTER TO CONTINUE.")
    generate_probs(domain, alg, enforce_extra_precondition)
    