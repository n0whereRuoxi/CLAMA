import os, sys
# List of domains
domains = [
    'blocks_counter',
    # 'depots_counter'
    ]
# List of algorithms
algorithms = [
    # 'curriculama',
    'htnmaker'
    ]
# List of configurations
generalization_configurations = [
    False,
    True
    ]
# List of phases
phases = [
    'initialization', 
    'training', 
    'testing', 
    'analyzing'
    ]
# problem sizes:
problem_sizes = [
    1, 
    2, 
    3
    ]
# number of runs
num_runs = 5
# Iterate over domains, algorithms, configurations, and phases
for domain in domains:
    for problem_size in problem_sizes:
        # generate random problems
        generator_dir = f'/home/rli12314/scratch/CurricuLAMA/experiments/{domain}'
        # go to dir
        os.chdir(generator_dir)
        # generate problems
        os.system(f'python3 generate_problems.py --difficulty {problem_size}')
        for algorithm in algorithms:
            if algorithm != 'curriculama':
                base_dir = '/home/rli12314/scratch/experiment_HTN-Maker'
                exp_dir = f'{base_dir}'
            else:
                base_dir = '/home/rli12314/scratch/CurricuLAMA'
                exp_dir = f'{base_dir}/experiments'
            for generalization_configuration in generalization_configurations:
                for phase in phases:
                    # Run the experiment for the current combination
                    print(f"Running experiment for domain: {domain}, algorithm: {algorithm}, generalzation: {generalization_configuration}, phase: {phase}")
                    # Add your experiment code here
                    if phase == 'initialization' and problem_size == 1:
                        # print info about current phase
                        # remove old results from base_dir
                        os.chdir(exp_dir + f'/{domain}/results')
                        # remove files that has the convention result_domain_htn_*.pddl if generalization_configuration is false, otherwise remove result_domain_htn_*_generalized.pddl, make sure result_domain_htn_*_generalized.pddl is not removed when generalization_configuration is false
                        if generalization_configuration:
                            os.system(f'rm result_{domain}_htn_*_generalized.pddl')
                        else:
                            os.system("find . -type f -name 'result_*_htn_*.pddl' ! -name '*_generalized.pddl' -exec rm {} +")
                    if phase == 'training' and problem_size == 1:
                        if generalization_configuration:
                            # call /home/rli12314/scratch/RecursiveLearn/main.py with the following arguments: {domain}  {algorithm} --enforce_extra_precondition if 'counter' in domain, otherwise without --enforce_extra_precondition
                            os.chdir('/home/rli12314/scratch/RecursiveLearn')
                            os.system(f"main.py {domain} {algorithm} {'--enforce_extra_precondition' if 'counter' not in domain else ''}")
                        else:
                            # call base_dir/train.py with the following arguments: {domain}
                            os.chdir(base_dir)
                            print('Now at', base_dir)
                            os.system(f"python3 train.py {domain} {'--lm hm' if domain == 'minigrid_counter' and algorithm == 'curriculama' else ''}")
                    if phase == 'testing':                        
                        # remove everything in exp_dir + f'/{domain}/results/plans'
                        os.system(f'rm {exp_dir}/{domain}/results/plans/*')
                        # call evaluate_all.py in exp_dir
                        os.chdir(exp_dir)
                        os.system(f"python3 evaluate_all.py {domain} {'--generalized' if generalization_configuration else ''} --runs {num_runs}")
                    if phase == 'analyzing':
                        os.chdir('/home/rli12314/scratch')
                        for analysis in ['convergence', 'plan_length', 'plan_time']:
                            os.system(f"python3 analyze.py {algorithm} {domain} {analysis} {'True' if generalization_configuration else 'False'} --runs {num_runs} > /home/rli12314/scratch/ICAPS24/final_results/{domain}/{algorithm}_{analysis}{'_generalized' if generalization_configuration else ''}_x{problem_size}.txt")