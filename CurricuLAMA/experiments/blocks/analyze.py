import csv
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import statistics

dir = "/scratch/zt1/project/nau-lab/user/rli12314/CurricuLAMA/experiments/"
domain = 'blocks'

total_num_train = 150
total_num_test = 50
all_result = []
for i in range(5):
    result = []
    for num_train in range(total_num_train):
        # print(num_train)
        with open(dir + domain + "/results/plans/planmeta_{}.txt".format(num_train+i*200), newline='') as csvfile:
            lines = csv.reader(csvfile, delimiter=',')
            data = list(lines)
            # print(data)
            planning_success_rate = len([1 for row in data if row and int(row[0]) > 0])/total_num_test
            # print(planning_success_rate)
            result.append(planning_success_rate)
    # print(result)
    all_result.append(result)

average = []
std = []
for j in range(total_num_train):
    data = [i[j] for i in all_result]
    average.append(sum(data)/len(all_result))
    std.append(statistics.stdev(data))
y = list(map(sum, zip(*all_result)))
# y = [s/4 for s in y]
x = list(range(len(y)))
# print(y)
print("curriculama_y_all = " + str(average))
print("curriculama_y_std_all = " + str(std))