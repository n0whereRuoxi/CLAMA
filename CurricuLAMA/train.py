# from ast import Is
print("importing packages...")
import os
import sys
# sys.path.append('/home/rli12314/scratch/CurricuLAMA')

current_dir = os.path.dirname(os.path.abspath(__file__))
print("Current Directory: ", current_dir)
root_path = os.path.join(current_dir, '..')

sys.path.append(root_path)
print("root path: ", root_path)

import re
# from parse_landmark_graph import get_subgoals_from_landmark_graph, parse_landmark_graph_topdown, read_landmark_graph
# from parse_problem import get_final_goal_task
# from parse_type_info import parse_object_types
from PDDL_parser import PDDLParser
from landmark_graph_processor import LandmarkGraphProcessor
import argparse
import time
# import tempfile
validator = root_path + "/VAL_bin/bin/Validate -v -t 0.001"
curriculama_dir = root_path + "/CurricuLAMA"
downward_dir = root_path + "/downward/fast-downward.py"
HTN_Maker_C_dir = root_path + "/HTNMakerC/htn-maker"

# There are several decision making points: 
# 1. how to group the subgoals hierarchically?
# 2. how to select subgoal ordering?
# os.chdir("/scratch/zt1/project/nau-lab/user/rli12314/CurricuLAMA/test_folder")
global lm_alg

def write_task(typed, task_file_dir, predicates, parameter_type, task_name):
    print("writting task: ", predicates, task_name)
    print("parameter type: ", parameter_type)
    with open(task_file_dir, "w") as file_task:
        file_task.write("( define\n")
        file_task.write("  ( tasks annotated-tasks )\n")
        file_task.write("  ( :task task-{}\n".format(task_name))
        file_task.write("    :parameters\n")
        file_task.write("    (\n")
        visited = []
        for p in predicates:
            for i in range(1, len(p)):
                if p[i] not in visited:
                    if typed:
                        file_task.write("      ?{} - {}\n".format(p[i], parameter_type[p[i]]))
                    else:
                        file_task.write("      ?{}\n".format(p[i]))
                    visited.append(p[i])
        file_task.write("    )\n")
        file_task.write("    :precondition\n")
        if typed:
            file_task.write("    (\n")
        else:
            file_task.write("    ( and\n")
            visited = []
            for p in predicates:
                for i in range(1, len(p)):
                    if p[i] not in visited:
                        file_task.write("      ( {} ?{} )\n".format(parameter_type[p[i]], p[i]))
                        visited.append(p[i])
        # :precondition
        # ( and
        #   ( OBJ ?obj )
        #   ( LOCATION ?dst )
        # )
        file_task.write("    )\n")
        file_task.write("    :effect\n")
        file_task.write("    ( and\n")
        for p in predicates:
            goal = "      ( " + p[0]
            for i in range(1, len(p)):
                goal += " ?{}".format(p[i])
            file_task.write(goal + " )\n")
        file_task.write("    )\n")
        file_task.write("  )\n")
        file_task.write(")\n") 

def get_task_name_by_predicates(domain, predicates, annotated_tasks, parameter_type):
    assert(len(predicates) == 1)
    task_name = predicates[0][0]
    for i in range(1, len(predicates[0])):
        task_name += '-'
        task_name += parameter_type[predicates[0][i]]
    return task_name

def get_plan_and_next_problem(domain, parameter_type, subgoals, idx, domain_file, problem_file_dir, file_full_plan, annotated_tasks, validator, debug):
    # with tempfile.NamedTemporaryFile(mode='w', delete=False) as file_problem:
    try:
        file_problem = open(problem_file_dir, "r")
    except OSError:
        print("Could not open/read file:", problem_file_dir)
        sys.exit()
    with file_problem:
        next_problem_file_dir = problem_file_dir.replace(".pddl", ".{}.pddl".format(idx))
        try:
            file_next_problem = open(next_problem_file_dir, "w")
        except OSError:
            print("Could not open/read file:", next_problem_file_dir)
            sys.exit()
        with file_next_problem:
            lines = file_problem.readlines()
            if idx is not 0: # replace the initial state with the previous final state
                for line in lines:
                    file_next_problem.write(line)
                    if re.search("init", line):
                        break
                # read final state
                try:
                    file_current_state = open("current_state.state", "r")
                except OSError:
                    print("Could not open/read file:", file_current_state)
                    sys.exit()
                with file_current_state:
                    lines = file_current_state.readlines()
                    for line in lines:
                        file_next_problem.write("    " + line + "\n")
                    file_next_problem.write("  )" + "\n")
            else: # the initial state is the problem initial state
                for line in lines:
                    if re.search("goal", line):
                        break
                    file_next_problem.write(line)
            # replace goal with the current subgoal
            file_next_problem.write("  ( :goal\n")
            file_next_problem.write("    ( and\n")
            subgoal = ""
            for i in subgoals[idx]:
                subgoal += i
                subgoal += " "
            file_next_problem.write("      ( {})\n".format(subgoal))
            file_next_problem.write("    )\n")
            file_next_problem.write("  )\n")
            file_next_problem.write(")\n")
    
    # get intermediate plan name
    match = re.search(r'\d+(?=_)', problem_file_dir)
    if match:
        digit = match.group(0)
        print(digit)
        intermediate_plan = "intermediate_plan_{}_{}.plan".format(digit, idx)

    # run planner 
    print("run planner to get intermediate plan...")
    cmd = "{} --plan-file {} {} {} --search \"astar(blind())\" {}".format(downward_dir,
        intermediate_plan, domain_file, next_problem_file_dir, ">/dev/null 2>&1" if debug < 1 else "")
    print(cmd)
    os.system(cmd)

    # read and save intermediate plan to the full plan
    plan_length = 0
    try:
        print("reading intermediate plan: ", intermediate_plan)
        file_plan = open(intermediate_plan, "r")
    except OSError:
        print("Could not open/read file:", intermediate_plan)
        sys.exit()
    with file_plan:
        lines = file_plan.readlines()
        for line in lines:
            if line[0] != ";": 
                file_full_plan.write("  "+line)
                plan_length += 1
    # get final state
    print("Getting the resulting state after executing the subplan...")
    os.system(validator + " " + domain_file + " " + next_problem_file_dir + " " + intermediate_plan + " >/dev/null 2>&1")
    
    # remove intermediate plan
    print("Removing intermediate plan...")
    os.remove(intermediate_plan)

    # remove next_problem_file
    print("Removing next problem file...")
    os.remove(next_problem_file_dir)

    # do not create anntoated task
    for i in range(len(annotated_tasks)):
        if subgoals[idx][0] == annotated_tasks[i][0]:
            flag = True
            for j in range(1, len(subgoals[idx])):
                if j < len(annotated_tasks[i]):
                    if parameter_type[subgoals[idx][j]] != parameter_type[annotated_tasks[i][j]]:
                        flag = False
                        break
            if flag:
                # do not create anntoated task
                return plan_length, i

    # create annotated task
    print("Creating annotated task ")
    task_name = get_task_name_by_predicates(domain, [subgoals[idx]], annotated_tasks, parameter_type)
    typed = True
    write_task(typed, "task_{}.pddl".format(len(annotated_tasks)), [subgoals[idx]], parameter_type, task_name)
    annotated_tasks.append(subgoals[idx])
    # wait = input("Press Enter to continue.")
    return plan_length, len(annotated_tasks) - 1

# replace this function with parse_parameter_type
def parse_parameter_type(domain, problem_file_dir, parameter_type):
    try:
        file_problem = open(problem_file_dir, "r")
    except OSError:
        print("Could not open/read file:", problem_file_dir)
        sys.exit()
    with file_problem:
        lines = file_problem.readlines()
        start = False
        for line in lines:
            if domain == 'blocks' or domain == "logistics":
                if re.search("objects", line):
                    start = True
                    continue
                if start:
                    search_result = re.search(r"([^\s]+) - ([^\s]+)", line)
                    if search_result:
                        parameter = search_result.groups()
                        # print(parameter)
                        parameter_type[parameter[0]] = parameter[1]
                    else:
                        break
            else:
                if re.search("init", line):
                    start = True
                    continue
                if start:
                    search_result = re.search(r"\((\w+) ([^\s]+)\)", line)
                    if search_result:
                        parameter = search_result.groups()
                        # print(parameter)
                        parameter_type[parameter[1]] = parameter[0]

def curriculama(idx, domain, curriculum_config, strip_domain_file_dir, problem_file_dir, partial_htn_dir, output_HTN_domain_file_dir, annotated_tasks, debug, time_log):
    # domain_name = "Blocks4" if "blocks" in domain else domain
    if domain == "blocks":
        domain_name = "Blocks4"
    elif "minigrid" in domain:
        domain_name = "minigrid"
    else:
        domain_name = domain
    # make sure domain_name does not contain underscore
    domain_name = domain_name.split("_")[0]
    # strip_domain_file_dir = downward_dir + "/misc/tests/benchmarks/{}/domain.pddl".format(domain)
    input_HTN_domain_file_dir = partial_htn_dir
    # parse parameter type
    print('Parsing PDDL problem...')
    PDDL_problem = PDDLParser(strip_domain_file_dir, problem_file_dir)
    start_time = time.time()
    parameter_type = PDDL_problem.object_types
    print("Parsed parameter type from problem file: ", parameter_type)

    if lm_alg == "hm":
        # Use lm-hm to get subgoals
        print("use lm-hm to get subgoals")
        cmd = "{} {} {} --search \"lazy_greedy([lmcount(lm_hm(m=1, conjunctive_landmarks=true, use_orders=true))])\" {}".format(downward_dir, strip_domain_file_dir, problem_file_dir, ">/dev/null 2>&1" if debug < 1 else "")
    elif lm_alg == "rhw":
        print("use lm_rhw to get subgoals")
        cmd = "{} {} {} --search \"lazy_greedy([landmark_sum(lm_rhw(disjunctive_landmarks=false, verbosity=normal, use_orders=true, only_causal_landmarks=true))])\" {}".format(downward_dir, strip_domain_file_dir, problem_file_dir, ">/dev/null 2>&1" if debug < 1 else "")
    elif lm_alg == "hps":
        print("use lm_hps to get subgoals")
        lm_factory = "lm_hm(m=1, conjunctive_landmarks=true, use_orders=true)"
        # lm_factory = "lm_rhw(use_orders=true, only_causal_landmarks=true)"
        # lm_factory = "lm_rhw(disjunctive_landmarks=false, verbosity=normal, use_orders=true, only_causal_landmarks=false)"
        cmd = "{} {} {} --search \"lazy_greedy([landmark_sum(lm_reasonable_orders_hps({}, verbosity=normal\
                    ))])\" {}".format(downward_dir, strip_domain_file_dir, problem_file_dir, lm_factory, ">/dev/null 2>&1" if debug < 1 else "")
    else:
        # use LAMA to get subgoals
        print("use LAMA to get subgoals")
        cmd = "{} --alias lama-first {} {} {}".format(downward_dir, strip_domain_file_dir, problem_file_dir, ">/dev/null 2>&1" if debug < 1 else "")
    print(cmd)
    os.system(cmd)
    # parse subgoals
    lm_graph = LandmarkGraphProcessor("graph.dot", PDDL_problem)
    # move graph.dot to ./experiments/{domain}/debug/graph_{idx}.dot
    os.system("mv graph.dot ./experiments/{}/debug/graph_{}.dot".format(domain, idx))
    # save the digraph  
    # lm_graph.save()
    subgoals = lm_graph.subgoals
    print("subgoals: ", subgoals)
    # press button to continue
    # wait = input("Press Enter to continue.")
    time_log.append(time.time() - start_time)
    # get complete plan by following the subgoals
    solution_file_dir = f"experiments/{domain}/debug/complete_plan_{idx}.plan"
    task_idx_and_subplan_length = []
    try:
        file_full_plan = open(solution_file_dir, "w")
    except OSError:
        print("Could not open/read file:", solution_file_dir)
        sys.exit()
    with file_full_plan:

        file_full_plan.write("( defplan {} Prob01\n".format(domain_name))
        annotated_tasks = []
        for i in range(len(subgoals)):
            # print("About to plan for: ", problem_file_dir)
            print("Planning for subgoal: ", subgoals[i])
            # wait = input("Press Enter to continue.")
            plan_length, task_idx = get_plan_and_next_problem(domain, parameter_type, subgoals, i, 
                strip_domain_file_dir, problem_file_dir, file_full_plan, annotated_tasks, validator, debug)
            print("plan_length and task idx: ", plan_length, task_idx)
            if plan_length:
                task_idx_and_subplan_length.append((task_idx, plan_length))
        file_full_plan.write(")")
        print("task_idx_and_subplan_length: ", task_idx_and_subplan_length)
    
    # skip the loop if plan is empty
    if not task_idx_and_subplan_length:
        print("Skipping the loop because plan is empty")
        os.system("cp {} {}".format(input_HTN_domain_file_dir, output_HTN_domain_file_dir))
        # read last line of number.txt and copy it to the same file
        with open('number.txt', 'r') as f:
            last_line = f.readlines()[-1]
        with open('number.txt', 'a') as f:
            f.write(last_line)
        time_log.append(0)
        time_log.append(0)
        return

    # wait = input("Press Enter to continue.")

    # get the final task
    # final_task = get_final_goal_task(problem_file_dir)
    # print("Getting the final task: ", final_task)
    # write_task("task_final.pddl" , final_task, parameter_type, "final")
    def get_plan_idx(task_idx_and_subplan_length, idx):
        if idx < 0:
            return 0
        plan_idx = 0
        for i in range(idx+1):
            plan_idx += task_idx_and_subplan_length[i][1]
        return plan_idx

    if curriculum_config == "left-recursive":
        # create curriculum (left-recursive)
        current_pos = 0
        curriculum_file_dir = "problem.curriculum"
        print([b for (_,b) in task_idx_and_subplan_length], sum([b for (_,b) in task_idx_and_subplan_length]))
        total_plan_length = sum([b for (_,b) in task_idx_and_subplan_length])
        with open(curriculum_file_dir, "w") as file_curriculum:
            for i in range(len(task_idx_and_subplan_length)):
                (task_idx, plan_length) = task_idx_and_subplan_length[i]
                end_pos = current_pos + plan_length
                file_curriculum.write("{},{},{}\n".format(current_pos, end_pos, task_idx))
                if current_pos != 0:
                    file_curriculum.write("{},{},{}\n".format(0, end_pos, task_idx))
                current_pos = end_pos
    elif curriculum_config == "left-and-right-recursive":
        # create curriculum (left-and-right-recursive)
        current_pos = 0
        curriculum_file_dir = "problem.curriculum"
        print([b for (_,b) in task_idx_and_subplan_length], sum([b for (_,b) in task_idx_and_subplan_length]))
        total_plan_length = sum([b for (_,b) in task_idx_and_subplan_length])
        with open(curriculum_file_dir, "w") as file_curriculum:
            for i in range(len(task_idx_and_subplan_length)):
                # print(i, list(reversed(range(i))))
                (task_idx, plan_length) = task_idx_and_subplan_length[i]
                end_idx = get_plan_idx(task_idx_and_subplan_length, i)
                # print(i, range(1, i+2))
                for j in range(1, i+2):
                    start_idx = get_plan_idx(task_idx_and_subplan_length, i-j)
                    # print(start_idx, end_idx, task_idx)
                    file_curriculum.write("{},{},{}\n".format(start_idx, end_idx, task_idx))
    elif curriculum_config == "all-inclusive-recursive":
        # create curriculum (left-and-right all-inclusive recursive)
        current_pos = 0
        curriculum_file_dir = "problem.curriculum"
        print([b for (_,b) in task_idx_and_subplan_length], sum([b for (_,b) in task_idx_and_subplan_length]))
        total_plan_length = sum([b for (_,b) in task_idx_and_subplan_length])
        with open(curriculum_file_dir, "w") as file_curriculum:
            for i in range(len(task_idx_and_subplan_length)):
                # print(i, list(reversed(range(i))))
                (task_idx, plan_length) = task_idx_and_subplan_length[i]
                end_idx = get_plan_idx(task_idx_and_subplan_length, i)
                # print(i, range(1, i+2))
                for j in reversed(range(end_idx)):
                    start_idx = j
                    # print(start_idx, end_idx, task_idx)
                    file_curriculum.write("{},{},{}\n".format(start_idx, end_idx, task_idx))
    time_log.append(time.time() - start_time - sum(time_log))
    # wait = input("Press Enter to continue.")
    # run HTN-Maker-C to learn HTN methods from curriculum
    configuration = "--partial_generalization --drop_unneeded --curriculum"
    os.system("{} {} {} {} {} {} {} {} {}".format(HTN_Maker_C_dir, 
        configuration, strip_domain_file_dir, curriculum_file_dir, problem_file_dir, 
        solution_file_dir, input_HTN_domain_file_dir, output_HTN_domain_file_dir, "N/A",
        ">/dev/null 2>&1" if debug < 1 else ""))
    time_log.append(time.time() - start_time - sum(time_log))
    
def run_experiments(n, domain, curriculum_configs_idx, debug):
    annotated_tasks = []
    curriculum_configs = ["left-recursive", "left-and-right-recursive", "all-inclusive-recursive"]
    strip_domain_file_dir = curriculama_dir + "/experiments/{}/classical-domain.pddl".format(domain)
    initial_HTN_domain_file_dir = curriculama_dir + "/experiments/{}/htn-domain-empty.pddl".format(domain)
    prob_dir = curriculama_dir + "/experiments/{}/classical_probs".format(domain)
    input_HTN_domain_file_dir = initial_HTN_domain_file_dir
    # digits = [str(i) for i in range(75)]
    # digits = [0]
    for i in range(0,150):
        time_log = []
        i = i + n*200
        output_HTN_domain_file_dir = curriculama_dir + "/experiments/{}/results/result_domain_htn_{}.pddl".format(domain, i)
        print("\nDoing experiments for prob{}_strips.pddl".format(i))
        try:
            curriculama(
                i,
                domain, 
                curriculum_configs[curriculum_configs_idx], 
                strip_domain_file_dir, 
                prob_dir + "/prob{}_strips.pddl".format(i), 
                input_HTN_domain_file_dir, 
                output_HTN_domain_file_dir, 
                annotated_tasks, 
                debug, 
                time_log
            )
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            sys.exit(0)
        input_HTN_domain_file_dir = output_HTN_domain_file_dir
        with open('./experiments/{}/time_log_{}.txt'.format(domain,domain), 'a') as f:
            f.write('{}\n'.format(','.join([str(i) for i in time_log])))
        wait = input("Press Enter to continue.")
        os.system("rm current_state.state current_state.1 task_*.pddl problem.curriculum sas_plan*")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("domain", help="blocks/ logistics", type=str)
    parser.add_argument("--debug", help="debug mode", type=int, default=1)
    parser.add_argument("--lm", help="lm algorithm", type=str, default="hps")
    args = parser.parse_args()
    lm_alg = args.lm
    curriculum_configs_idx = 2
    # clear the time log file if it exists
    os.system('rm ./experiments/{}/time_log_{}.txt'.format(args.domain, args.domain))
    os.system('rm number.txt')
    for i in range(5):
        print("Doing experiments for run {}".format(i))
        run_experiments(i, args.domain, curriculum_configs_idx, args.debug)
    # move number.txt to ./experiments/{domain}/number_of_methods.txt, replace file if it exists
    os.system("mv number.txt ./experiments/{}/number_of_methods.txt".format(args.domain))
