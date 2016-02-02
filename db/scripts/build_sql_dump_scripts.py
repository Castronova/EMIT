import os
import cvload
import load_wof_to_ODM2
import apsw as sqlite3
import io

print 'This script will perform the following tasks: '
print '1. Create an ODM2 database '
print '2. Load the ODM2 CV terms '
print '3. Create a database load script containing no sample data (../tests/data/empty_dump.sql)'
print '4. Load sample data into the ODM2 database '
print '5. Create a database load script containing sample data (../tests/data/populated_dump.sql) \n\n'


# cannot get in-memory, shared cache to work!

# remove db file if it already exists
print 'Removing existing temp.sqlite database...',
dbpath = os.path.abspath('temp.sqlite')
if os.path.exists(dbpath):
    os.remove(dbpath)
print 'done'

# connect to the sqlite database
conn = sqlite3.Connection(dbpath)
c = conn.cursor()

# build database schema
print 'Building Database Schemas...',
ddl = open('ODM2_for_SQLite.sql','r').read()
c.execute(ddl)
print 'done'

# load controlled vocabularies
# cvload.load_cv("sqlite:///"+dbpath)

output = io.StringIO()
shell=sqlite3.Shell(stdout=output, db=conn)
shell.process_command(".dump")
with open('build_empty.sql', 'w') as f:
    lines = output.getvalue().split('\n')
    new_data = '\n'.join(lines)
    f.writelines(new_data)
del shell

# # create empty database SQL dump file
# with open('../tests/data/empty_dump.sql', 'w') as f:
#     for line in conn.iterdump():
#         try:
#             # handle unicode characters such as greek letters
#             line = line.encode('ascii', 'ignore')
#             f.write('%s\n' % line)
#         except Exception, e:
#             print e

# load some data
load_wof_to_ODM2.load_wof(dbpath)

# add some people
print 'Adding Person Records...',
ddl = open('insert_people.sql','r').read()
c.execute(ddl)
# conn.commit()
print 'done'

# add some simulation data
print 'Adding Simulation Records...',
ddl = open('insert_simulation.sql','r').read()
c.execute(ddl)
# conn.commit()
print 'done'

# add some observations data
print 'Adding Observation Records...',
ddl = open('insert_observation.sql','r').read()
c.execute(ddl)
# conn.commit()
print 'done'

# # create populated database SQL dump file
# with open('../tests/data/populated_dump.sql', 'w') as f:
#     for line in conn.iterdump():
#         try:
#             # handle unicode characters such as greek letters
#             line = line.encode('ascii', 'ignore')
#             f.write('%s\n' % line)
#         except Exception, e:
#             print e

output = io.StringIO()
shell=sqlite3.Shell(stdout=output, db=conn)
shell.process_command(".dump")
with open('populated_dump.sql', 'w') as f:
    lines = output.getvalue().split('\n')
    new_data = '\n'.join(lines)
    f.writelines(new_data)
del shell

# close database connection
c.close()
conn.close()


# remove temp sqlite database
print 'Cleaning...',
dbpath = os.path.abspath('temp.sqlite')
if os.path.exists(dbpath):
    os.remove(dbpath)
print 'done'

print 'Finished'
