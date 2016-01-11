

# Packaging

#### Building a new environment

Install conda-env

`([my_env_name])$ conda install -c conda conda-env`

#### Create a new environment and install dependencies 

`$ conda env create -n [my_env_name] -f emit-env python=2.7`

#### Freezing current environment

`$ conda env export -n [my_env_name] -f emit-env`


# Installing pysqlite 

#### Pysqlite2 on Windows

`pip install pysqlite2`

#### Pysqlite on OSX
*http://gis.stackexchange.com/questions/101383/problem-loading-spatialite-extension-with-sqlite3-python-connector*  
*https://github.com/ghaering/pysqlite/issues/60*  
*http://stackoverflow.com/questions/1545479/force-python-to-forego-native-sqlite3-and-use-the-installed-latest-sqlite3-ver*


`xcode-select --install`

`git clone https://github.com/ghaering/pysqlite.git`

`wget http://www.sqlite.org/snapshot/sqlite-amalgamation-201601111252.zip`

`unzip sqlite-amalgamation-201601111252.zip -d pysqlite`

`rm -rf sqlite-amalgamation-201601111252.zip`

`cd pysqlite`

`vim setup.cfg`
```
[build_ext]
libraries=sqlite3
# define=SQLITE_OMIT_LOAD_EXTENSION
```

`source activate [MyEnv]`

`python setup.py install`


#### Testing

```
$ python  
>>> from pysqlite2 import dbapi2 as sqlite3  
>>> con = sqlite3.connect(":memory:")  
>>> con.enable_load_extension(1)  
>>> conn.execute('select 1 where Equals( GeomFromText("POINT(1 1)"), GeomFromText("POINT(1 1)") )').fetchall()
```




