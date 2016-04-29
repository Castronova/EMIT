import sqlite3 as lite
from gui.controller.UserCtrl import UserCtrl
import environment
import coordinator.engineAccessors as engine
from gui.views.EMITView import EMITView
from sprint import *
from utilities import gui


class EMITViewCtrl(EMITView):
    def __init__(self, parent):

        EMITView.__init__(self, parent)
        self.FloatCanvas = self.Canvas.FloatCanvas

        connections_txt = environment.getDefaultConnectionsTextPath()
        script_path = environment.getDefaultScriptPath()
        filepath = environment.getDefaultLocalDBPath()

        # connect to known databases
        # if the database is not found in the dir (dev mode) or app (install mode), create it
        if not os.path.exists(filepath):
            conn = lite.connect(filepath)
            script = open(script_path)
            with conn:
                cur = conn.cursor()
                cur.executescript(script.read())
            script.close()

        # connect to databases defined in the connections file
        dbs = gui.read_database_connection_from_file(connections_txt)
        for db in dbs:
            usr, pwd = self.decrypt_db_username_password(db['address'], db['database'], db['username'], db['password'])
            if usr is not None:
                engine.connectToDb(db['name'],db['description'],db['engine'],db['address'],db['database'],usr,pwd)

        # load the local database into the engine
        engine.connectToDb(title='ODM2 SQLite (local)',desc='Local SQLite database',engine='sqlite',address=filepath, dbname=None, user=None, pwd=None, default=True)
        self.check_users_json()

    def check_users_json(self):
        UserCtrl.create_user_json()
        if UserCtrl.is_user_json_empty():
            controller = UserCtrl(self)
            controller.CenterOnScreen()
            controller.Show()


    def decrypt_db_username_password(self, address, dbname,  uhash, phash):

        import secret
        import encrypt
        cipher = encrypt.AESCipher(secret.key)
        usr = cipher.decrypt(uhash) or None
        pwd = cipher.decrypt(phash)

        if usr is None:
            msg = 'Could not resolve database username for %s/%s.  Make sure secret.py is created correcly.' % (address, dbname)
            sPrint(msg, MessageType.ERROR)

        return usr, pwd
