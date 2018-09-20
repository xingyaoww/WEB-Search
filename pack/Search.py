from pack.db import *
from pack.config import *
import codecs
import json
from bs4 import BeautifulSoup
import re


def HTML_search(searchFor, resultName):
    cur, conn = db_init()
    cur.execute('SELECT id,url,html FROM Pages WHERE html IS NOT NULL AND error IS NULL')
    fhand = codecs.open(str(resultName), 'w', 'utf-8');
    fhand.write('searchResult={[')
    print(f'* Searching For {searchFor}')
    for icur in cur:
        id = icur[0]
        url = icur[1]
        html = icur[2]
        htmlstr = html.decode()
        find = re.findall('.{0,20}'+str(searchFor)+'.{0,20}',htmlstr)
        pos = htmlstr.find(str(searchFor))
        if len(find)<1: continue
        resultstr = {
        "id":id,
        "url":url,
        "str":find,
        "pos":pos,
        "html":htmlstr
        }
        jsonstr = json.dumps(resultstr)
        fhand.write(jsonstr)
        print(f''' * FOUND [{find}] IN URL [{url}] # POS:{pos}''')
    fhand.write(']}')
    fhand.flush()
    fhand.close()
    print(f'[{resultName}] - File Write Complete, [quit] to save file.\n')