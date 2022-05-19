import database
import statistics
import sys

'''
find median snvs in individual across a chr. create score above/below
'''

db = database.DB('misc_hapmap.db')

table = 'graph'
newtable  = 'graph_norm'

#for each chr in an indiv find median
data_dict = {}
newins = []
q = ''' SELECT chr, GROUP_CONCAT(start), GROUP_CONCAT(stop), GROUP_CONCAT(snvs) FROM {} GROUP BY chr ;'''.format(table)
for res in db.query(q):

	allsnvs = [float(i) for i in res[-1].split(',')]
	start = [j for j in res[1].split(',')]
	stop = [j for j in res[2].split(',')]
	median = statistics.median(allsnvs)

	if median == 0:
		if res[0] == 'Y':
			median=statistics.median([i for i in allsnvs if i != 0])
		else:
			continue

	mymin = min(allsnvs)
	mymax = max(allsnvs)

	for v in range(0, len(allsnvs)-1):
        #vnorm = (allsnvs[v]-mymin)/(mymax-mymin)

		vnorm = allsnvs[v]/median

		if vnorm > 3:
			vnorm = 3

		newcount = (res[0], start[v], stop[v], vnorm)
		newins.append(newcount)

tables = db.search_table()
if newtable not in tables:
	info = ("CREATE TABLE IF NOT EXISTS {} ( chr TEXT, start INTEGER, stop INTEGER, snvs FLOAT)".format(newtable))
	db.create_table(info)
	indx1 = '''CREATE INDEX {}_id_start_stop_snvs ON {} (chr, start, stop, snvs) '''.format(newtable, newtable)
	db.create_index_general(indx1)

ins = '''INSERT INTO {} VALUES (?, ?, ?, ?) '''.format(newtable)
db.insert_many_general(ins, newins)
