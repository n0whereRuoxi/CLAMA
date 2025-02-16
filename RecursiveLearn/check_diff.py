import difflib

def read_file(file_path):
    # Read a file and remove all whitespace (spaces, tabs, newlines)
    with open(file_path, 'r') as file:
        return ''.join(file.read().split())

root_dir = "/home/rli12314/scratch/CurricuLAMA/experiments/blocks_recursion/results"
file1 = f"{root_dir}/result_domain_htn_20.pddl"
file2 = f"{root_dir}/result_domain_htn_20_generalized.pddl"

file1_content = read_file(file1)
file2_content = read_file(file2)


# count how many string "method" in each file
print(file1_content.count("method"))
print(file2_content.count("method"))
