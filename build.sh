#!/bin/bash

# Install dependencies from requirements.txt
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Navigate to /downward directory
cd ./downward
rm -rf builds/release/CMakeCache.txt
rm -rf builds/release/CMakeFiles

# Run the build script with the release argument
./build.py release
