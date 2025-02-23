#!/bin/bash

# Install dependencies from requirements.txt
# Python 3.10.10 works without any dependency conflict
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Navigate to /downward directory
cd ./downward
rm -rf builds/release/CMakeCache.txt
rm -rf builds/release/CMakeFiles

# Run the build script with the release argument
./build.py release

# Build HTN-Maker-C
# GCC 8.5.0 should work for compiling HTNMakerC
cd ../HTNMakerC
./configure
make

# Try first experiment 
cd ../CurricuLAMA
python3 train.py --debug 2 blocks
# The learned HTN methods are in Curriculama/experiments/blocks/*.pddl
# The digit in *.pddl correspond to the problem number
