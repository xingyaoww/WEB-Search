from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pack.db import *
from Shell import *

import ssl

def SSLerrorsIgnore():
    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

def scrape_init(start_link,cur,conn):
    # Process link and store it in db
    # Check to see if we are already in progress...
    cur.execute('SELECT id,url FROM Pages WHERE html is NULL and error is NULL ORDER BY RANDOM() LIMIT 1')
    row = cur.fetchone()
    if row is not None:
        print("** Restarting existing crawl **")
    if len(start_link) >1:
        # row is None - Start Initialization

        # Checking & Modify URLs
        if start_link.endswith('/'): start_link = start_link[:-1]
        if start_link.endswith('.htm') or start_link.endswith('.html'):
            pos = start_link.rfind('/')
            start_link = start_link[:pos]

        # If start_link VALID & EXISTS, INSERT TO TABLES
        if len(start_link) > 1:
            cur.execute('INSERT OR IGNORE INTO Webs (url) VALUES ( ? )', (start_link,))
            cur.execute('''INSERT OR IGNORE INTO Pages (url, html, new_rank) 
                        VALUES ( ?, NULL, 1.0 )''', (start_link,))
            conn.commit()

    # Get the current webs - netloc
    cur.execute('''SELECT url FROM Webs''')
    global webs
    webs = list()
    for row in cur: webs.append(str(row[0]))
    print(webs)
    # Initializing Complete - start_link is stored in db.

def Scarpe(start_link,dbname):
    ctx = SSLerrorsIgnore()
    cur, conn = db_init(dbname)
    global shell
    shell = Shell()
    shell.cur = cur
    shell.conn = conn
    scrape_init(start_link, cur, conn)


    # Start Looping for more sites
    iterationTimes = 0
    tcount = 0
    while True:
        # Iteration Control
        if iterationTimes!= -1 and iterationTimes < 1:
            print('* Input [all] to access all pages available * \n* Hit [enter] to End *')
            sval = input('How many pages:')
            if sval.lower() == 'all': print(f'Visiting all links in netloc: \n {webs}')
            if len(sval) < 1: break
            try: iterationTimes = int(sval)
            except:
                iterationTimes = -1
                print('*** ACCESSING ALL LINKS ***')
        if sval.lower() != 'all': iterationTimes = iterationTimes - 1

        # Get unvisited pages in db. Find if there is unretrieved page ?
        cur.execute('SELECT id,url FROM Pages WHERE html is NULL and error is NULL ORDER BY RANDOM() LIMIT 1')
        try:
            row = cur.fetchone()
            fromid = row[0]
            url = row[1]
        except:
            print('No unretrieved HTML pages found')
            print(f' {tcount} URL VISITED ')
            iterationTimes = 0
            break

        print(fromid, url, end=' ')

        # If we are retrieving this page, there should be no links from it
        cur.execute('DELETE from Links WHERE from_id=?', (fromid, ) )

    # Open & Save URL - find if it is OK
        tcount += 1
        try:
            document = urlopen(url, context=ctx)
            html = document.read()

            if document.getcode() != 200:
                print("Error on page: ",document.getcode())
                cur.execute('UPDATE Pages SET error=? WHERE url=?', (document.getcode(), url))

            if 'text/html' != document.info().get_content_type():
                print("Ignore non text/html page")
                # cur.execute('DELETE FROM Pages WHERE url=?', ( url, ) )
                cur.execute('UPDATE Pages SET error=0 WHERE url=?', (url, ) )
                conn.commit()
                continue
            soup = BeautifulSoup(html, "html.parser")
            print(f' Length:{str(len(html))}', end=' ')
        except KeyboardInterrupt:
            print('')
            print('Program interrupted by user...')
            break
        except:
            print("Unable to retrieve or parse page")
            cur.execute('UPDATE Pages SET error=-1 WHERE url=?', (url, ) )
            conn.commit()
            continue

        # Fill in the HTML Info.
        cur.execute('INSERT OR IGNORE INTO Pages (url, html, new_rank) '
                    'VALUES ( ?, NULL, 1.0 )', (url, ))
        cur.execute('UPDATE Pages SET html=? WHERE url=?', (memoryview(html), url ) )
        # memory view : it is a buffer, can increase speed and efficiency.
        conn.commit()


        # Retrieve all of the anchor tags -- Find next pages
        tags = soup('a')
        count = 0
        # print(f'***{tags}***')
        for tag in tags:
            # print(f'  * WORKING ON {tag}')
            href = tag.get('href', None)
            if href is None: continue

            # Resolve relative references like href="/contact"
            up = urlparse(href)

            if len(up.scheme) < 1: href = urljoin(url, href) # No scheme 'HTTP://' is detected
            ipos = href.find('#')
            if ipos > 1: href = href[:ipos]
            if href.endswith('.png') or href.endswith('.jpg') or href.endswith('.gif'): continue
            if href.endswith('/'): href = href[:-1]
            if len(href) < 1: continue


            # Check if the URL is in any of the webs
            # Restrict the newly find link in a single web domain.
            found = False
            for web in webs:
                if href.startswith(web) :
                    found = True
                    break
            if not found: continue

            cur.execute('''INSERT OR IGNORE INTO Pages (url, html, new_rank) 
                        VALUES ( ?, NULL, 1.0 )''', (href, ))
            count += 1
            conn.commit()

            cur.execute('SELECT id FROM Pages WHERE url=? LIMIT 1', ( href, ))
            try:
                row = cur.fetchone()
                toid = row[0]
            except:
                print('Could not retrieve id')
                continue
            # print fromid, toid
            cur.execute('INSERT OR IGNORE INTO Links (from_id, to_id) VALUES ( ?, ? )', ( fromid, toid ) )


        print(f'# {count} Links Found')

    print(f' {tcount} URL VISITED ')
    cur.close()
