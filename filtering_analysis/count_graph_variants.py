import sys
import numpy as np
import json
import database

#count variants from graph file (json) in certain bin

#read dictionary and add vars
f = open(sys.argv[2])
my_vars = json.load(f)

pos = []
chr = ''
for ch in my_vars:
	chr = str(ch)
	for i in my_vars[chr]:
		ia = int(i.split()[1])
		if ia in pos:
			continue
		pos.append(ia)
		for j in my_vars[chr][i]:
			j = int(j.split()[1])
			if j in pos:
				continue
			pos.append(j)
		
pos = np.array(pos)

#read bin file
putit = []
for line in open(sys.argv[1]):
	line = line.split('\t')
	binchr = str(line[0])
	if binchr != chr:
		continue
		
	start = int(line[1])
	end = int(line[2])

	#match arrays
	match = np.where(np.logical_and(pos>=start, pos<=end))
	rangematch = np.where(match)[0]
	putit.append((binchr, start, end, len(rangematch)))

db = database.DB('misc_hapmap.db')

#create table
tables = db.search_table()

if 'graph' not in tables:
	print('create table graph')
	info = ("CREATE TABLE IF NOT EXISTS graph (chr TEXT, start INTEGER, stop INTEGER, snvs INTEGER)")
	db.create_table(info)
	indx1 = '''CREATE INDEX graph_db_start_stop_snvs ON graph (chr, start, stop, snvs) '''
	db.create_index_general(indx1)


ins = '''INSERT INTO graph VALUES (? , ?, ?, ?) '''
db.insert_many_general(ins, putit)


