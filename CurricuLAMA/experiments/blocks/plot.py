import csv
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import statistics

dir = "/scratch/zt1/project/nau-lab/user/rli12314/CurricuLAMA/experiments/"
domain = 'blocks'

all_result = []
for i in range(4):
    result = []
    for num_train in range(75):
        with open(dir + domain + "/results/plans/planmeta_{}.txt".format(num_train+i*100), newline='') as csvfile:
            lines = csv.reader(csvfile, delimiter=',')
            data = list(lines)
            # print(data, [1 for row in data])
            planning_success_rate = len([1 for row in data if int(row[0]) > 0])/25
            # print(planning_success_rate)
            result.append(planning_success_rate)
    print(result)
    all_result.append(result)

average = []
std = []
for j in range(75):
    data = [i[j] for i in all_result]
    average.append(sum(data)/len(all_result))
    std.append(statistics.stdev(data))
y = list(map(sum, zip(*all_result)))
y = [s/4 for s in y]
x = list(range(len(y)))
print(y)
print(average)
print(std)