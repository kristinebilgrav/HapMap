import database
import statistics
import sys

'''
find median snvs in individual across a chr. create score above/below
'''


#read genders
genders = {}
for line in open(sys.argv[1]):
	(key, val)= line.rstrip('\n').split('\t')
	genders[key] = val

db = database.DB('misc_hapmap.db')

table = 'unfiltered_snvs'
newtable  = 'unfiltered_snvs_norm'

#for each chr in an indiv find median
data_dict = {}
newins = []
q = ''' SELECT id, chr, GROUP_CONCAT(start), GROUP_CONCAT(stop), GROUP_CONCAT(snvs) FROM {} GROUP BY id, chr ;'''.format(table)
for res in db.query(q):
	#do not count female/males when Y/X
	id = res[0]
	chr = res[1]

	if chr == 'Y' and genders[id] == 'female':
		continue
	if chr == 'X' and genders[id] == 'male': 
		continue
		

	allsnvs = [float(i) for i in res[-1].split(',')]
	start = [j for j in res[2].split(',')]
	stop = [j for j in res[3].split(',')]
	med = statistics.median(allsnvs)

	if med == 0:
		if chr =='Y':
			med = statistics.median([i for i in allsnvs if i != 0])
		else:
			continue

	mymin = min(allsnvs)
	mymax = max(allsnvs)

	for v in range(0, len(allsnvs)-1):
        #vnorm = (allsnvs[v]-mymin)/(mymax-mymin)

		vnorm = allsnvs[v]/med

		if vnorm > 3:
			vnorm = 3

		newcount = (res[0], res[1], start[v], stop[v], vnorm)
		newins.append(newcount)

tables = db.search_table()
if newtable not in tables:
	info = ("CREATE TABLE IF NOT EXISTS {} (id TEXT, chr TEXT, start INTEGER, stop INTEGER, snvs FLOAT)".format(newtable))
	db.create_table(info)
	indx1 = '''CREATE INDEX {}_id_start_stop_snvs ON {} (id, chr, start, stop, snvs) '''.format(newtable, newtable)
	db.create_index_general(indx1)

ins = '''INSERT INTO {} VALUES (?, ?, ?, ?, ?) '''.format(newtable)
db.insert_many_general(ins, newins)
