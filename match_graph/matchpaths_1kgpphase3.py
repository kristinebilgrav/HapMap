import sys
import gzip as gz
#import database
import statistics
#import os
import pysam

#match paths in graph with refrence panel
#needs pysam, python3
#use refrence panel


#remove paths that have individuals < X
#save results in DB?

chr = sys.argv[1].split('_')[0]

count = 0
snvdict = {}

#graph file
for line in open(sys.argv[1]):
	if line.startswith('pathnumber'):
		continue

	count += 1
	if count % 2 == 0:
		path = line.rstrip('\n').split('\t')
		for kmer in path[1:]:
			k0 = ' '.join(kmer.split()[0:3])
			k1 = ' '.join(kmer.split()[3:])
			snvdict[k1] = 0
			snvdict[k0] = 0

#reference // 1kgp
if 'gz' in sys.argv[2]:
	opener = gz.open
else: 
	opener= open


#count rare/swedish
#find stats on snv presence in 1kgp
raresnvs = 0
commonsnvs = 0
commonsnvamount = []
kgpsnvs = {}
for snv in opener(sys.argv[2], mode='rt'):
	if snv.startswith('#'):
		continue
	klist = snv.split('\t')[0:2]
	klist.append(snv.split('\t')[4])
	k = ' '.join(klist)

	#skip those not in graph
	if k not in snvdict:
		continue

	#look at gentotype
	GTs = snv.split('GT\t')[-1]

	GTcount = 0
	nullnull = GTs.count('0|0')
	snvcount = 2504 - nullnull	

	#how many with variant
	GTcount += snvcount
	snvdict[k] = GTcount

	#rare
	if GTcount < 22:
		raresnvs += 1

	#common
	else:
		commonsnvs += 1
		commonsnvamount.append(snvdict[k])
		

#print(snvdict)
	
output = open(sys.argv[3], 'a')

print('rare',raresnvs)
print('common',commonsnvs)

#average/median amount of people with the common variant
average = sum(commonsnvamount)/len(commonsnvamount)
mediancommon = statistics.median(commonsnvamount)

print('average', average)
print('median', mediancommon)

outputline = [str(chr), str(raresnvs), str(commonsnvs),str(average), str(mediancommon), str(len(snvdict)) ]
print(outputline)
output.write('\t'.join(outputline) + '\n')





#match SNVs
#for snv in res:
#	if snv in snvdict:
#		snvdict[snv] += 1

#print(snvdict)
#print(match)
#print(len(snvdict))

#db = database.DB('/proj/nobackup/sens2017106/kristine/hapmap/hapmap.db')
#make table
# kmer, HRC, Graph, SweGen
# kmer, dataset, amount - generates multiple instances of one

