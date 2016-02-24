

### OSX Instructions

1. Clone project
    
    `$ git clone https://github.com/Castronova/EMIT.git`

1. Move into the emit directory

    `$cd path/to/emit`
    

1. Build environment clean environment

    `$ ./build-dev-enivronment.sh emit emit-env-osx`

1. Activate environment

    `$ source activate emit`

1. Run EMIT to make sure it works
    
    `(emit)$ pythonw EMIT.py`
    
1. install spatialite-tools

    `(emit)$ brew install spatialite-tools libspatialite`
       
1. Remove user info so that it is not bundled into the installer

    `$ rm app_data/config/users.json`
    
1. Build the installer

    `$ pyinstaller emit.spec -y —-clean`
    
1. Test the installation by navigating into installer folder

    - double click on emit.app


---

### Windows Instructions

*coming soon*


---

### Linux Instructions

*coming soon*