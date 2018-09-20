import os
from pack.db import *
from pack.config import *
from pack.WebPageRetrieve import *
from pack.Search import *

class Shell:
    def __init__(self) -> object:
        self.command = {}
        self.start_link = None
        self.scrape_db_name = None
        self.search_result_name = None
        self.cur = None
        self.conn = None

    def cmdhelp(self):
        print('''
*** Web-Page-Retrieve Sys. V2.0 ***
**Commands which can be used:
* dir - List folder content
* cd - Change directory
* rm - Remove File
* scrape [link] - Start scrape at [Link]
** Ignore the [link] to visit the Default link
* search [content] - start search for [content] in db. Regex is supported.
* renewdb - Remove database & recreate one
* status - Show db & web status
* help - For command help
* quit - Exit
                    ''')
    def run(self):
        self.cmdhelp()
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
                    print('ERROR - File Not Found or is occupied')

            elif cmd.lower().strip()=='scrape':
                # Database File Name Set
                dbName = ''
                try:
                    dbName = str(input('Hit [enter] to use the default setting.\n> Database File Name Save As: '))
                except:
                    print('* Wrong File Name *')
                if len(dbName) < 1: dbName = default_dbname
                self.scrape_db_name = dbName

                # Start Link Set
                start_link = cmd[8:].strip()
                if len(start_link) < 1:
                    print('* Default Link Set')
                    start_link = default_start_link
                print(f'* Start Link Setted {start_link}')

                Scarpe(start_link,dbName)

            elif cmd.lower().startswith('search'):
                # Result File Name Set
                resultName = ''
                try: resultName = str(input('Hit [enter] to use the default setting.\n> Result File Name Save As: '))
                except: print('* Wrong File Name *')
                if len(resultName)<1 : resultName = default_result_name
                self.search_result_name = resultName

                searchFor = cmd.lower().strip()[6:].strip()
                HTML_search(searchFor, resultName)

            elif cmd.lower() == 'renewdb':
                # Problem Unsolved
                try: renew_db(self.cur,self.conn)
                except: print('UNKNOWN ERROR. Database is not Connected. Start Scrape First.')

            elif cmd.strip().lower() == 'status':
                print(f' - DbName:{dbname}\n - Start-Link:{self.start_link}')

            elif cmd.lower().strip() == 'quit':
                print('*** Shell ENDs ***')
                return

            elif cmd.lower().strip() == 'help': self.cmdhelp()

            else: print('*** COMMAND ERROR ***')

if __name__ == '__main__':
    print('--- SYSTEM START ---')
    Shell = Shell()
    Shell.run()
    print('--- SYSTEM END ---')