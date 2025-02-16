import csv
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import statistics
import argparse
import numpy as np
parser = argparse.ArgumentParser()
parser.add_argument("alg", help="one of two algorithms", type=str)
parser.add_argument("domain", help="one of five domains", type=str)
parser.add_argument("config", help="one of two configurations", type=str)
parser.add_argument("generalized", help="methods generalized?", type=str, default="False")
# add a argument indicating the number of runs, default is 5
parser.add_argument("--runs", help="number of runs", type=int, default=5)
args = parser.parse_args()
alg = args.alg
domain = args.domain
config = args.config

if alg == "curriculama":
    dir = "/home/rli12314/scratch/CurricuLAMA/experiments/"
else:
    dir = "/home/rli12314/scratch/experiment_HTN-Maker/"

# print("alg: {}, domain: {}, config: {}, generalized: {}".format(alg, domain, config, args.generalized))

######### planning success rate ###########
total_num_train = 150
total_num_test = 50
all_result_planning_success_rate = []
all_results_plan_length = []
all_results_plan_time = []
n_runs = args.runs
for i in range(n_runs):
    # print("doing set {}".format(i))
    result = []
    result_plan_length = []
    result_plan_time = []
    for num_train in range(total_num_train):
        # print("\tdoing prob {}".format(num_train+i*200))
        with open(dir + domain + "/results/plans/planmeta_{}{}.txt".format(num_train+i*200, "_generalized" if args.generalized == "True" else ""), newline='') as csvfile:
            lines = csv.reader(csvfile, delimiter=',')
            data = list(lines)[:50]
            # print("\t\t",data)
            plan_length = np.mean([int(row[0]) for row in data if row and int(row[0]) >= 0])
            planning_success_rate = len([1 for row in data if row and int(row[0]) >= 0])/total_num_test
            # print("planning_success_rate", planning_success_rate)
            plan_time = np.mean([float(row[1]) for row in data])
#            print(plan_time)
            result.append(planning_success_rate)
            result_plan_length.append(plan_length)
            result_plan_time.append(plan_time)
#    print(result_plan_time)
    all_result_planning_success_rate.append(result)
    all_results_plan_length.append(result_plan_length)
    all_results_plan_time.append(result_plan_time)

average = []
std = []
if config == 'convergence':
    all_result = all_result_planning_success_rate
elif config == 'plan_length':
    all_result = all_results_plan_length
else:
    all_result = all_results_plan_time
for j in range(total_num_train):
    data = [i[j] for i in all_result]
    average.append(sum(data)/len(all_result))
    std.append(statistics.stdev(data) if len(data) > 1 else 0)
y = list(map(sum, zip(*all_result)))
x = list(range(len(y)))

y_label = "curriculama_y_all = " if alg == "curriculama" else "htnmaker_y = "
y_err_label = "curriculama_y_std_all = " if alg == "curriculama" else "htnmaker_y_std = "
print(y_label + str(average))
print(y_err_label + str(std))

