import sys
import gzip as gz

"""
count switches between known maternal or paternal haplotypes that should not occur. 
phase set of each site is compared with upstream neighboring phased sites. 
Switch Error Rate (SER) defined as number of errors divided nby oppertunities for errors. 
from this further classified as long, point and undetermined. 
"""


def find_chr_ser(mydict, poss):
	switch = 0
	sortedpos = sorted(list(mydict.keys()))
	ps = ''
	for p in sortedpos:
		pps = mydict[p]
		if pps != ps:
			ps = pps
			switch += 1
	SER = (switch-1)/poss
	return SER


#1 genome file
if 'gz' in sys.argv[1]:
	opener = gz.open
else: 
	opener =  open

possible = 0
pos_ps = {}
mainchr = '1'
id = sys.argv[1].split('/')[-3]
output = open(sys.argv[2], 'a')
for line in opener(sys.argv[1], mode = 'rt'):
	if line.startswith('#'):
		continue

	if 'PASS' != line.split('\t')[6]:
		continue

	possible += 1
	chr = line.split('\t')[0]
	if 'GL' in chr or 'MT' in chr:
		continue
	if chr != mainchr:
		chrser = find_chr_ser(pos_ps, possible)
		possible = 0
		pos_ps = {}
		newline= [id, mainchr, str(chrser)]
		output.write('\t'.join(newline) + '\n')
		mainchr = chr

	ps_index = line.split('\t')[8].split(':').index('PS')
	ps = line.rstrip('\n').split('\t')[9].split(':')[ps_index]

	pos = line.split('\t')[1]
	
	pos_ps[pos] = ps


Y_ser = find_chr_ser(pos_ps, possible)
newline= [id, mainchr, str(chrser)]
output.write('\t'.join(newline)	+ '\n')
