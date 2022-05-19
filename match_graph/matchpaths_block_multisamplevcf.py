import sys
import gzip as gz
#import database
import statistics
#import os
#import pysam

#match paths in graph (file)  with refrence panel - block
#needs pysam, python3
#use refrence panel


#remove paths that have individuals < X
#save results in DB?

chr = sys.argv[1].split('_')[0]

def count_GT(line, mysnvdict, snv):

	#look at genotype
	GTs = line.split('GT\t')[-1].split('\t')
	total = len(GTs)
	nullnull = GTs.count('0|0')
	GTcount = total - nullnull	

	mysnvdict[snv] += GTcount

	return mysnvdict


def match_withblock(bdict, sampledict):
	for snv in sampledict:
		for pth in bdict:
			if snv in bdict[pth]:
				bdict[pth][snv] += sampledict[snv]
			else:
				continue

	return bdict

#// vcf file
if 'gz' in sys.argv[2]:
	opener = gz.open
else: 
	opener= open



raresnvs = 0
commonsnvs = 0
commonsnvamount = []

allsnvs = 0
snvdict = {'12 92809294 C':50, '12 60199765 A':10}
for snv in opener(sys.argv[2], mode='rt'):
	if snv.startswith('#'):
		continue
	klist = snv.split('\t')[0:2]
	klist.append(snv.split('\t')[4])
	k = ' '.join(klist)

	#count all snvs
	allsnvs += 1

	if k not in snvdict:
		snvdict[k]=0


	#if multiple indiv file (GT info)
	count_GT(snv, snvdict, k)

	#else
	#snvdict[k] += 1



count = 0
blockdict = {}

#graph-connected file
for line in open(sys.argv[1]):
	if line.startswith('pathnumber'):
		continue

	count += 1
	if count % 2 == 0:
		path = line.rstrip('\n').split('\t')
		pathn=path[0]
		if pathn not in blockdict:
			blockdict[pathn] = {}
		for kmer in path[1:]:
			k0 = ' '.join(kmer.split()[0:3])
			if k0 in list(snvdict.keys()):
				blockdict[pathn][k0] = snvdict[k0]
			else:
				blockdict[pathn][k0] = 0


			k1 = ' '.join(kmer.split()[3:])
			if k1 in list(snvdict.keys()):
				blockdict[pathn][k1] = snvdict[k1]

			else:
				blockdict[pathn][k1] = 0



#match with block
#matching_dict = {}
#match_withblock(blockdict, kgpsnvs)


#output = open(sys.argv[3], 'w')
#header = ['pathnumber', 'coverage', 'rare%', 'common%']
#output.write('\t'.join(header) + '\n')

for pth in blockdict:
	#do stats on block
	nrare= 0
	original = blockdict[pth]
	zeros = len([key for (key, value) in blockdict[pth].items() if value == 0])
	coverage = (len(original)-zeros)/len(original)

	nrare= len([key for (key, value) in blockdict[pth].items() if value < 22])
	prare = nrare/len(original)
	pcommon = (len(original)-nrare)/len(original)



#	output.write('\t'.join([pth, str(coverage), str(prare), str(pcommon)]) + '\n')

	#if pcommon > 0.8:
		#classification= 'common_hap'
	


#db = database.DB('/proj/nobackup/sens2017106/kristine/hapmap/hapmap.db')
#make table
# kmer, HRC, Graph, SweGen
# kmer, dataset, amount - generates multiple instances of one

