import sys
import gzip as gz 
import sqlite3
import os
import argparse

import database

#input: 

#create database 

db = database.DB('hapmap.db')

#create table
tables = db.search_table()

if 'haploblock' not in tables:
	info = ("CREATE TABLE IF NOT EXISTS haploblock (id TEXT, chr TEXT, pos INTEGER, alt TEXT, GT TEXT, PS INTEGER)")
	db.create_table(info)
else:
	db.drop_index('pos')
	db.drop_index('phaseset')



vcf_data = []

#extract info from file and add to table
if sys.argv[1].endswith('gz'):
	opener = gz.open
else: 
	opener = open

for line in opener(sys.argv[1], mode = 'rt'):
	if line.startswith('#'):
		if line.startswith('#CHROM'):
			id = line.rstrip('\n').split('\t')[-1]
		continue

	line = line.strip('\n').split('\t')

	#chr
	chr = line[0]

	#ALT
	alt = line[4] 

	#pos
	pos = int(line[1])

	info = line[8].split(':')

	#GT
	if 'GT' in info:
		gi = info.index('GT')
		GT = line[9].split(':')[gi]

	#PS
	if 'PS' in info:
		pi = info.index('PS')

		PS = int(line[9].split(':')[pi])

		
	vcf_data.append((id, chr, pos, alt, GT, PS))



#insert many
db.insert_many(vcf_data)


#create index
db.create_index(name ='phaseset', columns = '(PS, chr, pos, alt, id)')
db.create_index(name ='pos', columns = '(chr, pos, PS, alt, id)')

