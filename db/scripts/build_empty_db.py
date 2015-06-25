__author__ = 'tonycastronova'

import os
import pyspatialite.dbapi2 as sqlite3
import subprocess

# remove db file if it already exists
print 'Removing existing odm2.sqlite database...',
dbpath = os.path.abspath('odm2_empty.sqlite')
if os.path.exists(dbpath):
    os.remove(dbpath)
print 'done'


# connect to the sqlite database
conn = sqlite3.connect(dbpath)
c = conn.cursor()

# build database schema
print 'Building Database Schemas...',
ddl = open('ODM2_for_SQLite.sql','r').read()
c.executescript(ddl)
conn.commit()
print 'done'

# load controlled vocabularies
subprocess.call(["python cvload.py sqlite:///"+dbpath], shell=True)

# close database connection
c.close()
conn.close()

print 'Finished'
