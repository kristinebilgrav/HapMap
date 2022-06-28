import sys

#1 vep annotated file

def find_pathnumber(line):
	#several paths in one
	pathdict= {}
	paths = line.rstrip('\n').split('PATH=')[1:]

	if len(paths) > 1:
		for p in paths:
			pathnumber = p.split(',')[0]
			kmer = p.split(',')[1]
			pathdict[pathnumber] = kmer
	else:
		pathnumber = paths[0].split(',')[0]
		kmer= paths[0].split(',')[1]
		pathdict[pathnumber] = kmer

	return pathdict


def identify_exons(line):
	ananno = line.rstrip('\n').split('CSQ=')[-1].split(',')
	for an i ananno:
		exons = an.split('|')[-2].split('&')
		if len(exons) > 0:
			for exon in exons:
				if exon not in exon_to_path:
					exon_to_path[exon] = {}

				thesepaths = find_pathnumber(line)

				for pathnumber in thesepaths:
					if pathnumber not in exon_to_path[exon]:
						exon_to_path[exon][pathnumber] = []
					exon_to_path[exon][pathnumber].append(thesepaths[pathnumber])


type_to_path = {}
exon_to_path= {}
tf_to_path= {}
total = 0
chr = ''
for line in open(sys.argv[1]):
	if line.startswith('#'):
		continue

	chr = line.split('\t')[0]

	vepinfo = line.rstrip('\n').split('CSQ=')[-1].split(',')
	total += 1
	for vep in vepinfo:
		type = vep.split('|')[7]
		consequence = vep.split('|')[1]
		interest = type
		if len(interest) > 1:
			if interest not in type_to_path:
				type_to_path[interest] = {}

			thesepaths = find_pathnumber(line)

			for pathnumber in thesepaths:
				if pathnumber not in type_to_path[interest]:
					type_to_path[interest][pathnumber] = []
				#add kmer to pathnumber
				type_to_path[interest][pathnumber].append(thesepaths[pathnumber])

		tf = vep.split('|')[-1]



print('total', total)
for t in type_to_path:
	for pn in type_to_path[t]:
		print(chr, t, pn,  type_to_path[t][pn])

print(exon_to_path)
