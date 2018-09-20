import os
from pack.db import *
from pack.config import *

class Shell:
    def __init__(self) -> object:
        self.command = {}
        self.start_link = None
        self.dbname = dbname
        self.cur = None
        self.conn = None
    def run(self):
        print('''
    *** Web-Page-Retrieve Sys. V1.1 ***
    **Commands which can be used:
    * dir - List folder content
    * cd - Change directory
    * rm - Remove File
    * starturl [link] - Set Start Link and start the scrape
    ** OR Ignore the [link] to use the default setting.
    * renewdb - Remove database & recreate one
    * status - Show db & web status
    * quit - Exit
            ''')
        while True:
            dprint = os.getcwd()
            cmd = input(str(dprint) + '\n>>>')
            if cmd == 'dir':
                foldercontent = os.listdir()
                for i in foldercontent: print(f'  {i}')
            elif cmd.startswith('cd'):
                if cmd.strip() == 'cd..':
                    os.chdir('..')
                    dprint = os.getcwd()
                else:
                    targetFolder = cmd[2:].strip()
                    try:
                        os.chdir(targetFolder)
                        dprint = os.getcwd()
                    except:
                        print(f'*** CANNOT LOCATE FOLDER [{targetFolder}]')
            elif cmd.lower().startswith('rm'):
                try:
                    os.remove(cmd.lower()[2:].strip())
                except:
                    print('ERROR - File Not Found')
            elif cmd.lower().startswith('starturl'):
                start_link = cmd[8:].strip()
                if len(start_link) < 1: start_link = default_start_link
                print(f'Start Link Setted {start_link}')
                return start_link
            elif cmd.lower() == 'renewdb': renew_db(self.cur)
            elif cmd.strip().lower() == 'status': print(f' - DbName:{dbname}\n - Start-Link:{self.start_link}')
            elif cmd.strip().lower() == 'quit':
                print('*** Shell ENDs ***')
                return
            else: print('*** COMMAND ERROR ***')


