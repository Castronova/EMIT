#!/usr/bin/env bash

if [ "$1" == "help" ] || [ "$1" == "-h" ] || [ -z "$1" ] || [ $# -ne 1 ];
then
    echo "USAGE: "
    echo "./build-dev-environment.sh CONDA-ENV-NAME"
    echo "    - CONDA-ENV-NAME the desired conda environment name, must not exist already."
    exit 1
fi

envs=$(conda env list)
if [[ $envs == *$1* ]];
then
    echo "Conda environment already exists!"
    exit 1
fi

# create a the new conda environment
conda env create -n $1 -f emit-env python=2.7

# activate the environment
source activate $1

# Clone the pysqlite project
git clone https://github.com/ghaering/pysqlite.git

# download the sqlite amalgamation
wget http://www.sqlite.org/snapshot/sqlite-amalgamation-201601111252.zip

# extract sqlite contents into pysqlite directory
unzip sqlite-amalgamation* -d pysqlite

# build sqlite
cd pysqlite
python setup.py install
cd ..

# clean up
rm -rf sqlite-amalgamation*
rm -rf pysqlite

