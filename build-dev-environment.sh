#!/usr/bin/env bash

if [ "$1" == "help" ] || [ "$1" == "-h" ] || [ -z "$1" ] || [ $# -ne 2 ] || [[ $2 != "emit-env-"* ]];
then
    echo "USAGE: "
    echo "./build-dev-environment.sh CONDA-ENV-NAME CONDA-ENV-FILE"
    echo "    - CONDA-ENV-NAME the desired conda environment name, must not already exist"
    echo "    - CONDA-ENV-FILE the conda environment file that defines that packages to be installed."
    exit 1
fi



envs=$(conda env list)
for i in $envs; do
    if [[ $i == $1 ]];
        then
            echo "Conda environment already exists!"
            
            while true; do
                read -p "Do you want the remove this conda environment? [yes/no]" yn
                case $yn in
                    [Yy]* ) conda env remove --yes -n $1;break;;
                    [Nn]* ) exit 1;;
                    * ) echo "Please answer yes or no.";;
                esac
            done
    fi
done

{ # try catch block

    # create a the new conda environment
    conda env create -n $1 -f $2 python=2.7 &&

    # activate the environment
    source activate $1 &&

    echo 'Conda environment set up successfuly.'
} ||
{
    echo 'An error was encountered when creating the conda environment.'
    exit 1
}



# clone the apsw project
echo 'Cloning the apsw project'
git clone https://github.com/rogerbinns/apsw.git

# add EXPERIMERTAL to setup.cfg, otherwise enableloadextension fails
echo "define=EXPERIMENTAL" >> ./apsw/setup.cfg

# build apsw
cd apsw

{ # try catch block

    python setup.py fetch --all build --enable-all-extensions install 

} ||
{
    while true; do
        read -p 'No Checksum is available for SQLite. Do you want to continue without a checksum? [yes/no]' yn
        case $yn in 
            [Yy]* ) python setup.py fetch --all --missing-checksum-ok build --enable-all-extensions install;break;;
            [Nn]* ) rm -rf ./apsw;exit 1;;
            * ) echo "Please answer yes or no.";;
        esac
    done
}
cd ..



# install odm2api
pip install --process-dependency-links git+https://github.com/ODM2/ODM2PythonAPI.git


# clean up
echo 'Cleaning up the build directory.'
rm -rf apsw


echo '#'
echo '# To activate this environment, use:'
echo '# $ source activate' $1
echo '#'
echo '# To deactivate this environment, use:'
echo '# $ source deactivate' $1
echo '#'
