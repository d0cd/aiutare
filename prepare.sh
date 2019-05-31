#!/bin/bash

# GENERAL:
# Needed for all categories

if [[ ! -d "instances" ]]; then
   # "instances" contains benchmarks and other problem cases
   mkdir instances
fi

if [[ ! -d "tools" ]]; then
   # "tools" contains the programs to run
   mkdir tools
fi

if [[ ! -d "results" ]]; then
   # "results" contains the output of each program in a Mongo database
   mkdir results
fi

if [[ ! -d "images" ]]; then
   # "images" contains graphs generated from the data in "results"
   mkdir images
fi

sudo apt install python3-pip
pip3 install --upgrade pip
pip3 install matplotlib
pip3 install numpy


# CATEGORY-SPECIFIC:
# Iterates through the user-provided installation scripts

selected_categories=( "$@" )

for category_dir in bin/categories
do
   if [[ $# -eq 0 || " ${selected_categories[@]} " =~ " ${category_dir} " ]]; then

      if [[ ! -d "instances/${category_dir}" ]]; then
         mkdir instances/${category_dir}
      fi

      if [[ ! -d "tools/${category_dir}" ]]; then
         mkdir tools/${category_dir}
      fi

      if [[ ! -d "results/${category_dir}" ]]; then
         mkdir results/${category_dir}
      fi

      if [[ ! -d "images/${category_dir}" ]]; then
         mkdir images/${category_dir}
      fi

      for program_dir in ${category_dir}
      do
         bin/categories/${category_dir}/${program_dir}/install.sh
      done

   fi
done