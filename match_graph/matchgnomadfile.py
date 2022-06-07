import sys
import gzip as gz

'''
40 or more CAG repeats = full penetrance 
36-39 repeats = incomplete or reduced penetrance allele
27 - 35 repeats = intermediate allele not associated with syptomatic disease but could with further expansion
<26 not associated with HD
'''
#gnomad /ref file
HTT = {}
chr = ''
pos_to_rs = {}
for line in open(sys.argv[1]):
	if line.startswith('#'):
		continue
	if line.startswith('Chromo'):
		continue

	pos = line.split('\t')[1]
	ref = line.split('\t')[3]
	alt= line.split('\t')[4]
	chr = line.split('\t')[0]
	rsid = line.split('\t')[2]

	pos_to_rs[pos] = rsid

	if pos not in HTT:
		HTT[pos] = []

	HTT[pos].append(alt)


print(len(HTT.keys()))



#patient file /graph file
if 'gz' in sys.argv[2]:
	opener = gz.open
else:
	opener = open

paths= {}
match = 0
alt_to_af = {} 
for line in opener(sys.argv[2], mode = 'rt'):
	if line.startswith('#'):
		continue

	schr =  line.split('\t')[0]
	if schr != chr:
		continue
	pos = line.split('\t')[1]
	alt= line.split('\t')[4]
	fullalt = str(pos) + '_' + alt


	if pos in HTT:
		if alt in HTT[pos]:
			match +=1
#			print(line)
			if 'PATH' in line: 
				pathnumber = line.split('PATH=')[-1].split(',')[0]
				if pathnumber not in paths:
					paths[pathnumber] = []
				kmer = line.split('PATH=')[-1].split(',')[1]
				paths[pathnumber].append(kmer)

				AF =line.split('PATH=')[-1].split(',')[2]

				rs = pos_to_rs[pos]
				alt_to_af[rs] = AF	
#print(alt_to_af)
#print(paths)

#print(len(paths.keys()))
#print(match)


output = open(sys.argv[3], 'w')
for rs in alt_to_af:
	output.write('\t'.join([rs, str(alt_to_af[rs])]) + '\n'  )
	
