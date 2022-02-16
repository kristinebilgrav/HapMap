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


	#filter file

	#filter 10x vep annotated file on SNPs/SVs not present in either 1KGP, SweGen or have rs number for gnomad (ex rs112750067 )
	#SweGen_AF last -1 
	#Several 1KGP AFs (for each population) from pos -10 - -6
	#dontpass = ['10X_QUAL_FILTER', '10X_RESCUED_MOLECULE_HIGH_DIVERSITY', '10X_ALLELE_FRACTION_FILTER', '10X_PHASING_INCONSISTENT', '10X_HOMOPOLYMER_UNPHASED_INSERTION']

	save = False

	quality = False

	#allele frequency in databases
	swegen = line.strip('\n').split(';CSQ=')[-1].split('\t')[0].split('|')[-1]
	kgp = line.strip('\n').split(';CSQ=')[-1].split('\t')[0].split('|')[-10:-5]
	
	threshold = 0.01
	if len(swegen) > 0:
		if float(swegen) > threshold:
			save = True
			quality = True	
	for p in kgp:
		if len(p) > 0 and float(p) > threshold:
			save = True
			quality = True

	#remove non-snps
	type = line.split(';TYPE=')[-1].split(';')[0]
	if type != 'snp':
		quality = False


	#filter depth
	dp = float(line.split(';DP=')[-1].split(';')[0])
	if dp < 5:
		quality = False


	#filter on PASS 
	passit = ['PASS']
	filter = line.strip('\n').split('\t')[6]


	if filter in passit and quality == True:
		save = True
	
	else:
		save = False



	if save == True:


		#extract SNP
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

