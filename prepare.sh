#!/bin/bash

# GENERAL DIRECTORIES:
# ---------------------
if [[ ! -d "instances" ]]; then
   # "instances" contains benchmarks and other problem cases
   mkdir instances
fi

if [[ ! -d "tools" ]]; then
   # "tools" contains the programs to run
   mkdir tools
fi

if [[ ! -d "results" ]]; then
   # "results" contains the program output data in a Mongo database
   mkdir results
fi

if [[ ! -d "images" ]]; then
   # "images" contains graphs generated from the data in "results"
   mkdir images
fi


# CATEGORY SETUP:
# ---------------------
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


# MONGODB SETUP:
# ---------------------
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4

version=$(lsb_release -r -s)  # Detects Ubuntu version to install correct version of MongoDB
if [[ "${version}" = "16.04" ]]; then
   echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
fi
if [[ "${version}" = "18.04" ]]; then
   echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
fi

sudo apt-get update
sudo apt-get install -y mongodb-org

mkdir results/log
chmod 755 results/log


# ANALYSIS TOOLS:
# ---------------------
sudo apt install python3-pip
pip3 install --upgrade pip
pip3 install matplotlib
pip3 install numpy