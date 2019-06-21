#!/bin/bash

# TODO: check if mongodb is already installed

   mkdir -p results/log
   mkdir images

   user="$(id -u -n)"
   sudo chown -R ${user} ./results
   sudo chown -R ${user} ./images

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