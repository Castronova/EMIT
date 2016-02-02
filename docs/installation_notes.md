

# Packaging

#### Building a new environment

Install conda-env

`([my_env_name])$ conda install -c conda conda-env`

#### Create a new environment and install dependencies 

`$ conda env create -n [my_env_name] -f emit-env python=2.7`

#### Freezing current environment

`$ conda env export -n [my_env_name] -f emit-env`



# apsw (Another Python Sqlite Wrapper)

#### Installing dependencies

**OSX**

> `brew install libspatialite`  

> `brew install spatialite-tools`


#### Installing the apsw package

1. `git clone https://github.com/rogerbinns/apsw.git`

2. `echo "define=EXPERIMENTAL" >> ./apsw.setup.cfg`

3. `python setup.py fetch --all build --enable-all-extensions install`

#### Testing the installation

**make sure extension support is enabled**
    >>> import apsw
    >>> conn = apsw.Connection(':memory:')
    >>> getattr(conn, 'enableloadextension')
    <built-in method enableloadextension of apsw.Connection object at 0x1020c3f48>

**load spatialite**

Make sure mod_spatialite* exists on your system.  This should have been installed with `libspatialite`:

    $ find /usr/local/Cellar -type f -name 'mod_spatialite'*
    /usr/local/Cellar/libspatialite/4.3.0a_1/lib/mod_spatialite.7.dylib

    $ python
    >>> import apsw
    >>> conn = apsw.Connection(':memory:')
    >>> conn.enableloadextension(1)
    >>> conn.loadextension('mod_spatialite')
    >>> cur = conn.cursor()
    >>> cur.execute('select 1 where Equals( GeomFromText("POINT(1 1)"), GeomFromText("POINT(1 1)") )').fetchall()
    >>> [(1,)]
    
    
    >>> cur.execute('select InitSpatialMetaData()')
    >>> cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    
    

---

# Installing pysqlite 

#### Pysqlite2 on Windows

`pip install pysqlite2`

#### Pysqlite on OSX
*http://gis.stackexchange.com/questions/101383/problem-loading-spatialite-extension-with-sqlite3-python-connector*  
*https://github.com/ghaering/pysqlite/issues/60*  
*http://stackoverflow.com/questions/1545479/force-python-to-forego-native-sqlite3-and-use-the-installed-latest-sqlite3-ver*


1. `xcode-select --install`

2. `git clone https://github.com/ghaering/pysqlite.git`

3. `wget http://www.sqlite.org/snapshot/sqlite-amalgamation-201601111252.zip`

4. `unzip sqlite-amalgamation-201601111252.zip -d pysqlite`

5. `rm -rf sqlite-amalgamation-201601111252.zip`

6. `cd pysqlite`

7. `vim setup.cfg`

        [build_ext]
        libraries=sqlite3
        # define=SQLITE_OMIT_LOAD_EXTENSION

8. `source activate [MyEnv]`  

9. `python setup.py install`


#### Testing


`$ python`  
    
    >>> from pysqlite2 import dbapi2 as sqlite3  
    
    >>> con = sqlite3.connect(":memory:")  
    
    >>> con.enable_load_extension(1)  
    
    >>> conn.execute("select load_extension('mod_spatialite')")
    
    >>> conn.execute('select 1 where Equals( GeomFromText("POINT(1 1)"), GeomFromText("POINT(1 1)") )').fetchall()
    





