import sys
import numpy as np
import database

#read connected file, count snvs in bin

count=0
pos=[]
chr = ''
for li in open(sys.argv[2]):
	if li.startswith('pathnumber'):
		continue

	count += 1
	#path stats lines
	if count % 2 == 0:
		kmers = li.split('\t')
		for kmer in kmers[1:]:
			poses = kmer.split()
			chr=poses[0]
			mypos = int(poses[1])
			if mypos in pos:
				continue
			pos.append(mypos)
			mypos2 = int(poses[4])
			if mypos2 in pos:
				continue
			pos.append(mypos2)
pos=np.array(pos)

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

if 'connectedA' not in tables:
	print('create table connectedA')
	info = ("CREATE TABLE IF NOT EXISTS connectedA (chr TEXT, start INTEGER, stop INTEGER, snvs INTEGER)")
	db.create_table(info)
	indx1 = '''CREATE INDEX connectedA_db_start_stop_snvs ON graph (chr, start, stop, snvs) '''
	db.create_index_general(indx1)


ins = '''INSERT INTO connectedA VALUES (? , ?, ?, ?) '''
db.insert_many_general(ins, putit)



