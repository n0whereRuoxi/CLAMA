#!/bin/bash
#SBATCH --job-name=myjob
#SBATCH --output=%j.out
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=72:00:00

# Run command 
srun stdbuf -o0 -e0 python3 run_all_exp.py
