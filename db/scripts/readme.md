# Setup Instructions


#### Install Prereqs 

* install pyspatialite

```
pip install pyspatialite
```

**or** 

* This depends on the `proj_api.h` library which may need to be installed

```
sudo find / -name 'proj_api.h`    
CFLAGS=-I/usr/local/include pip install pyspatialite
```

#### Build Database

```
python load_data.py
```


