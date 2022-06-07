import sys
import numpy as np

'''

look through graph-indiv matched file, finds paths with lengths > x
and analyze how much of this path the individual covers

create matrix with coverage of each path
'''


#1 binfile
#2 graph vcf
#3 list of individual-mathed files

def read_bins(file, dict, chr):
	for line in open(file):
		thischr = line.split('\t')[0]
		if chr != thischr:
			continue
		start = line.split('\t')[1]
		end= line.rstrip('\n').split('\t')[2]
		dict[start] = end

	return dict


def read_vcf(file, dict, id):


	poslist = []
	for line in open(file):
		if line.startswith('#'):
			continue
		pos = int(line.split('\t')[1])
		poslist.append(pos)

	dict[id] = np.array(poslist)
	return dict




chr = '20'
bin_dict = {}
read_bins(sys.argv[1], bin_dict, chr)


#read full graph - total
total = {}
id = sys.argv[2].split('.')[0]
read_vcf(sys.argv[2], total, id)
total = total[id]

id_to_pos = {}
for file in open(sys.argv[3]):
	file = file.strip('\n')
	id = file.split('/')[-2].split('.')[0]
	read_vcf(file, id_to_pos, id)


output = open(sys.argv[4], 'w')
header = ['id', 'start', 'end', 'fraction_of_total' ]
output.write('\t'.join(header) + '\n')
for bin in bin_dict:
	start = int(bin)
	end = int(bin_dict[bin])

	thistmatch =  np.where(np.logical_and(total>=start, total<=end))
	thistotal = np.where(thistmatch)[0]


	for id in id_to_pos:
		match = np.where(np.logical_and(id_to_pos[id]>=start, id_to_pos[id]<=end))
		rangematch = np.where(match)[0]

		if len(thistotal) == 0:
			cov = 0

		else:
			cov = len(rangematch)/len(thistotal)
		mylst= [id, str(start), str(end) , str(cov) ]
		output.write('\t'.join(mylst) + '\n')
