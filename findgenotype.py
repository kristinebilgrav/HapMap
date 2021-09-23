import sys
import gzip 
import sqlite3
import os
#os.system('module load bioinfo-tools pysam') 
#import pysam  
import argparse

#name = sys.argv[1].split('.')[0].split('/')[-3]
name = sys.argv[2]

#sqlite3.paramstyle = 'named'

#create database 
#conn = sqlite3.connect(':memory:')
conn = sqlite3.connect('hapmap.db')

cur = conn.cursor()

#create table
def create_table(n):
	with conn:
		cur.execute("CREATE TABLE " + n + " (chr INTEGER, pos INTEGER, Alt TEXT, GT TEXT, PS INTEGER)")

#insert info
def insert(vcf_data, n):
	with conn:
		cur.execute("INSERT INTO " + n + " VALUES (:chr, :pos, :Alt, :GT, :PS)", vcf_data)
#query
def get_item(i, n):
	with conn:
		cur.execute('SELECT * FROM " + n + " WHERE chr=:chr', {'chr':i})
		return cur.fetchall()

create_table(name)

#extract info from file and add to table
if 'gz' in sys.argv[1]:
	for line in gzip.open(sys.argv[1], mode = 'rt'):
		if line.startswith(b'#'):
			continue
		vcf_data = {}
		line = line.strip('\n').split('\t')
		chr = line[0].replace('chr', '')
		try:
			vcf_data['chr'] = int(chr)
		except:
			vcf_data['chr'] = chr #.decode('utf-8')
		pos = line[1]
		vcf_data['pos'] =int( pos)
		info = line[8].split(':')

		#ALT
		alt = line[4] #.decode('utf-8')
		vcf_data['Alt'] = alt

		if 'GT' in info:
			i = info.index('GT')
			GT = line[9].split(':')[i]
			vcf_data['GT'] = GT #.decode('utf-8')

		if 'PS' in info:
			i = info.index('PS')
			PS = line[9].split(':')[i]
			try:
				vcf_data['PS'] = int(PS)
			except:
				vcf_data['PS'] = PS.decode('utf-8')


 		#print(vcf_data)
		insert(vcf_data, name)


w = get_item(1, name)
print(w)
#conn.commit()

