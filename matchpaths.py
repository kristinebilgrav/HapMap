import sys
import gzip
import multiprocessing
#import database
import os
#os.system('module load bioinfo-tools pysam')
import pysam

#match paths in graph with refrence panel (HRC)
#needs pysam, python3
#use refrence panel


#remove paths that have individuals < X
#save results in DB?

def matching_function(chr):

	all_vars = []
	reads = f.fetch(chr, multiple_iterators = True)
	for read in reads:
	#for i in range(0, len(reads) -1):
		#print(reads[i])
		klist = read.split('\t')[0:2]
		klist.append(read.split('\t')[4])
		k = ' '.join(klist)
		all_vars.append(k)
	return all_vars



count = 0
pathdict = {}
snvdict = {}

chr = sys.argv[1].split('_')[0]

for line in open(sys.argv[1]):
	if line.startswith('start'):
		continue

	count += 1
	if count % 2 == 0:
		path = line.rstrip('\n').split('\t')
		for kmer in path:
			k0 = ' '.join(kmer.split()[0:3])
			k1 = ' '.join(kmer.split()[3:])
			snvdict[k1] = 0
			snvdict[k0] = 0

			pathdict[kmer] = 0

f = pysam.TabixFile(sys.argv[2])
res = matching_function(chr)
print(len(res))

#make kmers out of variants
#for i in range(0, len(res)-1):
#	j = i + 1
#	kmer = ' '.join([res[i], res[j]])
#
#	if kmer in pathdict:
#		pathdict[kmer] += 1

#match SNVs
for snv in res:
	if snv in snvdict:
		snvdict[snv] += 1

match = 0
for key in snvdict:
	if snvdict[key] ==1:
		match += 1
#print(snvdict)
print(match)
print(len(snvdict))

#db = database.DB('/proj/nobackup/sens2017106/kristine/hapmap/hapmap.db')
#make table
# kmer, HRC, Graph, SweGen
# kmer, dataset, amount - generates multiple instances of one

