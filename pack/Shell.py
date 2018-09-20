import os
from pack.db import *
from pack.config import *

class Shell:
    def __init__(self):
        self.command = {}
        self.start_link = None
        self.dbname = dbname
    def run(self):
        print('''
            *** Web-Page-Retrieve Sys. V1.1 ***
            **Commands which can be used:
            * dir - List folder content
            * cd - Change directory
            * starturl [link] - Set Start Link and start the scrape
            * renewdb - Remove database & recreate one
            * status - Show db & web status
            * quit - Exit
            ''')
        while True:
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
            elif cmd.lower().startswith('starturl'):
                start_link = cmd[8:].strip()
                print(f'Start Link Setted {Start_link}')
                return start_link
            elif cmd.lower() == 'renewdb': renew_db()
            elif cmd.strip().lower() == 'status': print(f' - DbName:{dbname}\n - Start-Link:{start_link}')
            elif cmd.strip().lower() == 'quit':
                print('*** Shell ENDs ***')
                return
            else: print('*** COMMAND ERROR ***')


