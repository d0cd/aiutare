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
all_categories=(bin/categories/*)

for category_dir in "${all_categories[@]}"
do
   trimmed_cat=${category_dir##*/}
   if [[ $# -eq 0 || " ${selected_categories[@]} " =~ " ${trimmed_cat} " ]]; then

      if [[ ! -d "instances/${trimmed_cat}" ]]; then
         mkdir instances/${trimmed_cat}
      fi

      if [[ ! -d "tools/${trimmed_cat}" ]]; then
         mkdir tools/${trimmed_cat}
      fi

      if [[ ! -d "results/${trimmed_cat}" ]]; then
         mkdir results/${trimmed_cat}
      fi

      if [[ ! -d "images/${trimmed_cat}" ]]; then
         mkdir images/${trimmed_cat}
      fi

      all_programs=(${category_dir}/*)

      for program_dir in "${all_programs[@]}"
      do
         trimmed_dir=${program_dir##*/}
         bin/categories/${trimmed_cat}/${trimmed_dir}/install.sh
      done

   fi
done