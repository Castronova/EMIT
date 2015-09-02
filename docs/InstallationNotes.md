# This document contains installation and setup notes for various libraries 


## PySpatialLite

1. install pyspatialite

```
pip install pyspatialite
```

**or** 

* This depends on the `proj_api.h` library which may need to be installed

```
sudo find / -name 'proj_api.h'   
CFLAGS=-I/usr/local/include pip install pyspatialite
```


## Build Local and Testing Databases

1. Execute the loading script to create DLL files

```
cd [path tp project]/EMIT/db/scripts

python build_sql_dump_scripts.py

```

The results are placed in `[path to project]/EMIT/db/tests/data`.  Copy the text contained within these scripts and paste into the SQL editor of your choice.  Alternatively, these DDL scripts can be executed in python:

```

# get the database DDL text
populated_dump_script = open('[path to project]/db/tests/data/populated_dump.sql','r').read()

# create a sqlite database
mySQLiteDb = sqlite3.connect('[path to my sqlite db]') 

# load the DDL text into the databases
mySQLiteDb.executescript(populated_dump_script)
```

## GDAL Setup

1. Install GDAL Libraries

    * Install GDAL on the system (OSX)
    installs to /usr/local/Cellar/gdal/1.11.2_1
    
    ```
    brew install gdal
    ```
 
     
    * Install GDAL on the system (Antergos)
    
    `sudo pacman -S gdal`
    
    * Install GDAL on the system (Manjaro)
    
    `sudo yaourt gdal`  
    
    
2. Install GDAL Python Bindings
    
    * Using Anaconda or Miniconda
 
    ```
    conda install gdal
    ```

    *Note: force it if it asks and you can't get the dependant programs to stop*
    
3. Add GDAL_DATA to PyCharm Path

    * PyCharm -> Edit Configurations
    * Environment Variables
        * GDAL_DATA = [path to conda env]/share/gdal
        * _CONDA_SET_GDAL_DATA=1

    *Note: GDAL_DATA cannot contain relative path or "~"*


