
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
conda env remove --yes -n %1

:: Create a new environment
echo Creating a fresh environment 
conda env create -n %1 -f %2 python=2.7 

set dashed="-------------------------------------------------------------"


:: activate the environment
activate %1 &&^
echo %dashed% &&^
echo Installing GeoAlchemy &&^
echo %dashed% &&^
pip install  git+https://github.com/ODM2/geoalchemy.git@v0.7.3#egg=geoalchemy-0.7.3 &&^
echo %dashed% &&^
echo Installing odm2api &&^
echo %dashed% &&^
pip install  git+https://github.com/ODM2/ODM2PythonAPI.git &&^
echo %dashed% &&^
echo Installing APSW &&^
echo %dashed% &&^
pip install whl\apsw-3.11.1.post1-cp27-cp27m-win_amd64.whl &&^
echo %dashed% &&^
echo Installing Shapely &&^
echo %dashed% &&^
pip install whl\Shapely-1.5.7-cp27-none-win_amd64.whl &&^
echo %dashed% &&^
echo Installing GDAL &&^
echo %dashed% &&^
pip install whl\GDAL-1.11.2-cp27-none-win_amd64.whl &&^
echo %dashed% &&^
echo Fresh Development Environment Created &&^ 
echo %dashed% &&^
deactivate &&^

:: notes
:: conda create -n temp python=2.7
:: conda install pandas sqlalchemy networkx wxpython pyshp suds psycopg2 netcdf4 matplotlib seaborn pil requests geoalchemy2 
:: pip install  git+https://github.com/ODM2/geoalchemy.git@v0.7.3#egg=geoalchemy-0.7.3
:: pip install  git+https://github.com/ODM2/ODM2PythonAPI.git
:: pip install whl\Shapely-1.5.7-cp27-none-win_amd64.whl
:: pip install whl\GDAL-1.11.2-cp27-none-win_amd64.whl
:: pip install whl\apsw-3.11.1.post1-cp27-cp27m-win_amd64.whl





