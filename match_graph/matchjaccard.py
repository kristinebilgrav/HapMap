import sys
import statistics

'''

look through file with region of interest,
and analyze how snvs are present in the individual

create matrix with comparion of each individual against each other
'''

#1 vcf with graph inputs of interest
#2 list of files to check
#3 output 

alt_dict = {}
total = 0
for inp in open(sys.argv[1]):
	if inp.startswith('#'):
		continue

	pos = inp.split('\t')[1]
	alt = inp.split('\t')[4]
	total +=1
	if pos not in alt_dict:
		alt_dict[pos] = []

	alt_dict[pos].append(alt)


id_count= {}
for file in open(sys.argv[2]):
	file = file.strip('\n')

	id = file.split('/')[-2].split('.')[0]
	id_count[id] = 0

	chr = file.split('/')[-2].split('.')[1]

	for line in open(file):
		if line.startswith('#'):
			continue

		ipos = line.split('\t')[1]
		ialt = line.split('\t')[4]
		if ipos in alt_dict:
			if ialt in alt_dict[ipos]:
				id_count[id] += 1

output = open(sys.argv[3], 'w')
header = ['id']
rows={}
all = []
for id in id_count:
	id1 = id
	value1 = id_count[id]
	header.append(id1)
	for i in range(0, len(id_count.keys())):
		id2 = list(id_count.keys())[i]
		if id2 not in rows:
			rows[id2] = []
		value2 = list(id_count.values())[i]
		incommon = sorted([value1, value2])[0]
		jacc =  incommon/(value1 + value2 - incommon)
		rows[id2].append(jacc)
		all.append(jacc)

output.write('\t'.join(header) + '\n')

avg=sum(all)/len(all)
std=statistics.stdev(all)

for row in rows:
#	newrow=[str((i-avg)/std) for i in rows[row] ]
#	newrow = '\t'.join(newrow)
	newrow= [str(i) for i in rows[row]]
	newrow = '\t'.join(newrow)
	output.write('\t'.join([row, newrow]) + '\n')
