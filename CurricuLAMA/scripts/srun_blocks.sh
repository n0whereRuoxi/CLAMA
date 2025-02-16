#!/bin/bash
#SBATCH --job-name=myjob
#SBATCH --output=log.txt
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=10:00:00
# Run command 
srun python3 train.py blocks