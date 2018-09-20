from pack.config import *
from pack.db import *
from pack.search import *

def pagerank(pagerank_dbname):
    cur, conn = db_init(pagerank_dbname)
    # Reference from Dr.chuck's py4e.com
    # Find the ids that send out page rank - we only are interested
    # in pages in the SCC that have in and out links

    from_ids = list()
    to_ids = list()
    links = list()  # Relationship

    cur.execute('''SELECT DISTINCT from_id FROM Links''')
    for row in cur:
        from_ids.append(row[0])

    # Find the ids that receive page rank & Store the relationships
    cur.execute('''SELECT DISTINCT from_id, to_id FROM Links''')
    for row in cur:
        from_id = row[0]
        to_id = row[1]
        # Restrict to_id to be inside the web. Restrict By the spider.py
        if from_id == to_id: continue
        if from_id not in from_ids: continue
        # Restrict link outside the range of the Web Table.
        if to_id not in from_ids: continue
        links.append(row)
        if to_id not in to_ids: to_ids.append(to_id)

    # Get latest page ranks for strongly connected component IN DICT prev_ranks
    prev_ranks = dict()
    for node in from_ids:
        cur.execute('''SELECT new_rank FROM Pages WHERE id = ?''', (node,))
        row = cur.fetchone()
        prev_ranks[node] = row[0]

    sval = input('How many iterations:')
    iterations = 1
    if (len(sval) > 0): iterations = int(sval)

    # Sanity check
    if len(prev_ranks) < 1:
        print("Nothing to page rank.  Check data.")
        return

    for i in range(iterations):
        next_ranks = dict();
        total = 0.0
        # Count the Sum of old_rank as total, node is the from_id. Set next_rank all to 0;
        for (node, old_rank) in list(prev_ranks.items()):
            total = total + old_rank
            next_ranks[node] = 0.0

        # Find the number of outbound links and sent the page rank down each
        for (node, old_rank) in list(prev_ranks.items()):

            give_ids = list()  # temp list which is used only during one iteration.
            for (from_id, to_id) in links:
                # Find from_id = node
                if from_id != node: continue
                # Find to_id that satisfy the rule which was established
                if to_id not in to_ids: continue
                # add OK to_id to LIST give_ids
                # count how much the from_id contribute to the outside world
                give_ids.append(to_id)
            # if no give_id is found: skip to next from_id
            if len(give_ids) < 1: continue
            amount = old_rank / len(give_ids)

            # The id who received will has an INCREASE in rank. Increase by amount
            for id in give_ids:
                next_ranks[id] = next_ranks[id] + amount

        # Used to compensate the loss of total rank. assign evap to every node to maintain an overall unchange rank
        newtot = 0
        for (node, next_rank) in list(next_ranks.items()):
            newtot = newtot + next_rank
        evap = (total - newtot) / len(next_ranks)  # Average change in rank for every node.
        for node in next_ranks:
            next_ranks[node] = next_ranks[node] + evap

        newtot = 0
        for (node, next_rank) in list(next_ranks.items()):
            newtot = newtot + next_rank
        # Compute the per-page average change from old rank to new rank
        # As indication of convergence of the algorithm
        totdiff = 0
        for (node, old_rank) in list(prev_ranks.items()):
            new_rank = next_ranks[node]
            diff = abs(old_rank - new_rank)
            totdiff = totdiff + diff

        avediff = totdiff / len(prev_ranks)
        print(i + 1, avediff)

        # rotate
        prev_ranks = next_ranks

    # Put the final ranks back into the database
    # print(list(next_ranks.items())[:5])
    cur.execute('''UPDATE Pages SET old_rank=new_rank''')
    for (id, new_rank) in list(next_ranks.items()):
        cur.execute('''UPDATE Pages SET new_rank=? WHERE id=?''', (new_rank, id))
    conn.commit()
    cur.close()
