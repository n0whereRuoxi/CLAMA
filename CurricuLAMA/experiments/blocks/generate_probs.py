import random
import math
import numpy as np

def satisfied(stacks, goal_head, goal_args):
    facts = []
    for stack in stacks:
        if stack:
            facts.append("( on-table b{} )".format(stack[0]))
            for i in range(len(stack)-1):
                facts.append("( on b{} b{} )".format(stack[i+1], stack[i]))
            facts.append("( clear b{} )".format(stack[-1]))
    goal_fact = "( {}".format(goal_head)
    for i in goal_args:
        goal_fact += " b{}".format(i)
    goal_fact += " )"
    if goal_fact in facts:
        print(facts, goal_fact)
        return True
    else:
        return False


def generateProblemsAndSolutions(num_problems, num_blocks):
    for i in range(num_problems):
        blocksIdx = np.random.choice(range(1, 1000), num_blocks, replace = False)
        # random initial stacks
        stacks = [[] for _ in range(num_blocks-2)]
        for block in blocksIdx:
            chosed_stack = random.choice(range(len(stacks)))
            stacks[chosed_stack].append(block)
        print(stacks)

        goal_head = random.choice(["holding", "clear", "on-table", "on"])
        
        if goal_head == "holding":
            goal_args = [random.choice(blocksIdx)]
        elif goal_head == "clear":
            goal_args = [random.choice(blocksIdx)]
            while satisfied(stacks, goal_head, goal_args):
                goal_args = [random.choice(blocksIdx)]
        elif goal_head == "on-table":
            goal_args = [random.choice(blocksIdx)]
            while satisfied(stacks, goal_head, goal_args):
                goal_args = [random.choice(blocksIdx)]
        else:
            goal_args = random.sample(list(blocksIdx), 2)
            while satisfied(stacks, goal_head, goal_args):
                goal_args = random.sample(list(blocksIdx), 2)

        print("selected goal: ", goal_head, goal_args)
        writeProblem(i, blocksIdx, stacks, goal_head, goal_args)
        writeHTNProblem(i, blocksIdx, stacks, goal_head, goal_args)

def writeHTNProblem(problem_num, blocksIdx, stacks, goal_head, goal_args):
    fname = 'htn_probs/prob{}_htn.pddl'.format(problem_num)
    file = open(fname,"w") 
    writeHTNHeader(file)
    writeObjects(file, blocksIdx)
    writeInit(file, blocksIdx, stacks)
    writeTasksInProblem(file, blocksIdx, stacks, goal_head, goal_args)
    file.write(")\n")


def writeProblem(problem_num, blocksIdx, stacks, goal_head, goal_args):
    fname = 'classical_probs/prob{}_strips.pddl'.format(problem_num)
    file = open(fname,"w") 
    writeHeader(file)
    writeObjects(file, blocksIdx)
    writeInit(file, blocksIdx, stacks)
    writeGoal(file, blocksIdx, stacks, goal_head, goal_args)
    file.write(")\n")

def writeHTNHeader(file):
    file.write("( define ( htn-problem probname )\n")
    file.write("  ( :domain blocks4 )\n")
    file.write("  ( :requirements :strips :htn :typing :equality )\n")

def writeHeader(file):
    file.write("( define ( problem probname )\n")
    file.write("  ( :domain blocks4 )\n")
    file.write("  ( :requirements :strips :typing :equality )\n")

def writeObjects(file, blocksIdx):
    file.write("  ( :objects\n")
    for idx in blocksIdx:
        file.write("    b{} - block\n".format(idx))
    file.write("  )\n")

def writeInit(file, blocksIdx, stacks):
    file.write("  ( :init\n")
    file.write("    ( hand-empty )\n")
    for stack in stacks:
        if stack:
            file.write("    ( on-table b{} )\n".format(stack[0]))
            for i in range(len(stack)-1):
                file.write("    ( on b{} b{} )\n".format(stack[i+1], stack[i]))
            file.write("    ( clear b{} )\n".format(stack[-1]))
    file.write("  )\n")

def writeGoal(file, blocksIdx, stacks, goal_head, goal_args):
    goal_fact = "( {}".format(goal_head)
    for i in goal_args:
        goal_fact += " b{}".format(i)
    goal_fact += " )"
    file.write("  ( :goal\n")
    file.write("    ( and\n")
    file.write("      {}\n".format(goal_fact))
    file.write("    )\n")
    file.write("  )\n")

def writeTasksInProblem(file, blocksIdx, stacks, goal_head, goal_args):
    file.write("  ( :tasks\n")
    task = "    ( task-"
    task += goal_head
    for i in range(len(goal_args)):
        task += "-block"
    for i in range(len(goal_args)):
        task += " b{}".format(goal_args[i])
    task += " )"
    file.write(task)
    file.write("  )\n")

if __name__=="__main__":
    generateProblemsAndSolutions(1000,5)
