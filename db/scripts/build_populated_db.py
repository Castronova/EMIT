import os
import pyspatialite.dbapi2 as sqlite3
import subprocess
import cvload

# remove db file if it already exists
print 'Removing existing odm2.sqlite database...',
dbpath = os.path.abspath('odm2_pop.sqlite')
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
cvload.load_cv("sqlite:///"+dbpath)
# subprocess.call(["python cvload.py sqlite:///"+dbpath], shell=True)

# load some data
subprocess.call(["python load_wof_to_ODM2.py"], shell=True)

# add some people
print 'Adding Person Records...',
ddl = open('insert_people.sql','r').read()
c.executescript(ddl)
conn.commit()
print 'done'

# add some simulation data
print 'Adding Simulation Records...',
ddl = open('insert_simulation.sql','r').read()
c.executescript(ddl)
conn.commit()
print 'done'

# add some observations data
print 'Adding Observation Records...',
ddl = open('insert_observation.sql','r').read()
c.executescript(ddl)
conn.commit()
print 'done'

# close database connection
c.close()
conn.close()

print 'Finished'
