import sys

'''

look through graph-indiv matched file, finds paths with lengths > x
and analyze how much of this path the individual covers

create matrix with coverage of each path
'''


#1 vcf with graph inputs that match individual


def write_covfile(path_dict, pos_dict, outfile):

	'''
	output file with pathnumber, idnumber, %coverage and which kmers present
	'''
	output = open(outfile, 'w')
	header = ['#chrom', 'start', 'end', 'id', 'pathnumber', 'total_path_kmerlength', 'coverage', 'kmers_found']
	output.write('\t'.join(header) + '\n')

	for path in path_dict:
		for tot in path_dict[path]:
			poslist = sorted(pos_dict[path])
			cov = len(path_dict[path][tot])/int(tot)
			kmerstring =','.join([str(i) for i in path_dict[path][tot]])
			newline = [chr, str(poslist[0]), str(poslist[-1]),id,  path, str(tot), str(cov), kmerstring]

			output.write('\t'.join(newline) + '\n')
	return output



def write_matrix(path_dict, idlist, outfile):
	'''
	finds coverage of a path in an individual
	'''

	output = open(outfile, 'w')
	header = ['graph']
	for pthn in path_dict:
		head = 'P' + str(pthn) 
		header.append(head)
		for tot in path_dict[pthn]:
			for id in idlist:
				if id in path_dict[pthn][tot]:
					coverage = len(path_dict[pthn][tot][id])/tot
					idlist[id].append(str(coverage))

				else:
					idlist[id].append('0')

	output.write('\t'.join(header) + '\n')
	for i in idlist:
		id = read_id(i, kgp_dict)
		kmers = '\t'.join(idlist[i])
		newline = '\t'.join([id, kmers]) 
		output.write(newline + '\n')

	return output	


def write_cov_to_pos(path_dict, idlist, pth_pos, outfile ):

	output = open(outfile, 'w')

	newdict = {}
	for pthn in path_dict:
		#find binrange
		rangeset = pth_pos[pthn]
		bin0 = str(list(sorted(rangeset))[0])
		bin1 = str(list(sorted(rangeset))[-1])
		bin = '-'.join([bin0, bin1])
		if bin not in newdict: 
			newdict[bin] = {}

		#find coverage
		for tot in path_dict[pthn]:
			for id in idlist:
				if id not in newdict[bin]:
					newdict[bin][id] = []

				if id in path_dict[pthn][tot]:
					coverage = len(path_dict[pthn][tot][id])/tot
					newdict[bin][id].append(str(coverage))

				else:
					newdict[bin][id].append('0')

	header = ['bins','bine', 'id', 'coverage' ]
	output.write('\t'.join(header) + '\n')
	binset = set([])
	for bin in newdict:
		for id in newdict[bin]:
			binset.add(bin.split('-')[0])
			newline = [bin.split('-')[0], bin.split('-')[1], id, newdict[bin][id][0]]
			output.write('\t'.join(newline) + '\n')

	print(binset)
	print(len(binset))
	print(len(newdict.keys()))		
def read_id(id, dict):
	if id in dict:
		id = dict[id]
	else:
		id = 'SWE'
	return id


def read_id_file(file, dict):
	for line in open(file):
		id = line.split('\t')[0]
		pop = line.rstrip('\n').split('\t')[-1]
		dict[id] = pop
	return dict




#dictionary with path:pathlength:[kmernumber present]

kgp_dict = {}
#read_id_file(sys.argv[3], kgp_dict)


path_cov= {}
path_pos = {}
id_matrix = {}
path_ultimatepath = {}
for file in open(sys.argv[1]):
	file = file.strip('\n')

	id = file.split('/')[-2].split('.')[0]
	id_matrix[id] = []

	chr = file.split('/')[-2].split('.')[1]

	for line in open(file):
		if line.startswith('#'):
			continue
		paths = line.rstrip('\n').split('\t')[-1].split(';')
		for thepath in paths:
			pathn = thepath.split('PATH=')[-1].split(',')[0]
			pos = int(line.split('\t')[1])
			try:
				kmer = thepath.split('PATH=')[-1].split(',')[1]
			except:
				print(file, line)
			total = int(kmer.split('/')[-1]) + 1
			kmernum = kmer.split('/')[0]
			if total > 40:
				if pathn not in path_cov:
					path_cov[pathn] = {}
					path_cov[pathn][total] = {}
					path_pos[pathn] = {}
					path_ultimatepath[pathn] = set([])

				if id not in path_cov[pathn][total]:
					path_cov[pathn][total][id] = []
					path_pos[pathn][id] = []

				path_cov[pathn][total][id].append(kmernum)
				path_pos[pathn][id].append(pos)
				path_ultimatepath[pathn].add(pos)


#write_covfile(path_cov, path_pos, sys.argv[2])
#write_matrix(path_cov, id_matrix, sys.argv[2])
write_cov_to_pos(path_cov,id_matrix, path_ultimatepath, sys.argv[2])
