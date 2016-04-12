
@echo off

:: Parse the input arguments
set usage=F
if "%1" == "help" (set usage=T)
if "%1" == "-h" (set usage=T)
if [%1] == [] (set usage=T)
if [%2] == [] (set usage=T)
if "%usage%" == "T" (
echo ./build-dev-environment.sh CONDA-ENV-NAME CONDA-ENV-FILE
echo     - CONDA-ENV-NAME the desired conda environment name, must not already exist
echo     - CONDA-ENV-FILE the conda environment file that defines that packages to be installed.
exit /B
)

:: Remove the existing environment
echo Removing the existing environment 
conda env remove --yes -n temp

:: Create a new environment
echo Creating a fresh environment 
conda env create -n temp -f emit-env-win python=2.7 

:: activate the environment
activate temp &&^
echo Installing APSW &&^
pip install whl\apsw-3.11.1.post1-cp27-cp27m-win_amd64.whl &&^
echo Installing Shapely &&^
pip install whl\Shapely-1.5.7-cp27-none-win_amd64.whl &&^
echo Installing ODM2PythonAPI &&^
pip install --process-dependency-links git+https://github.com/ODM2/ODM2PythonAPI.git &&^
echo Fresh Development Environment Created &&^ 
deactivate &&^