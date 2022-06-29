
import sys

"""
performs analysis of annotated graph
"""

def find_pathnumber(line):

	"""
	one SNP can be involved in several paths.
	function finds all numbers and connects with which kmer the SNP has
	"""

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


def identify_effect(line, mydict):
	'''
	finds consequence or type of SNP - identified by VEP
	'''

	vepinfo = line.rstrip('\n').split('CSQ=')[-1].split(',')
	thesepaths = find_pathnumber(line)
	for vep in vepinfo:
		biotype = vep.split('|')[7]
		consequence = vep.split('|')[1]
		interest = biotype

		if len(interest) < 1:
			continue

		if interest not in mydict:
			mydict[interest] = 0

		mydict[interest] += 1

	#	for pathnumber in thesepaths:
	#		if pathnumber not in mydict[interest]:
	#			mydict[interest][pathnumber] = []
	#		mydict[interest][pathnumber].append(thesepaths[pathnumber])

	return mydict

def identify_exons(line, mydict):
	"""
	finds exons in the particular SNP
	"""


	vep = line.rstrip('\n').split('CSQ=')[-1].split(',')
	for an in vep:
		exons = list(set(an.split('|')[-2].split('&') ))

		if len(exons) < 1:
			continue

		thesepaths = find_pathnumber(line)
		for exon in exons:
			if exon not in mydict:
				mydict[exon] = {}


			for pathnumber in thesepaths:
				if pathnumber not in mydict[exon]:
					mydict[exon][pathnumber] = []
				mydict[exon][pathnumber].append(thesepaths[pathnumber])

	return mydict

def loop_dictionary(mydict, total):

	"""
	loop through dictionary and print 
	"""

	output = open(sys.argv[2], 'w')
	for t in mydict:
	#	for pn in mydict[t]:
	#		path_length = int(sorted(mydict[t][pn])[-1].split('/')[-1]) + 1

	#		coverage = len(mydict[t][pn])/path_length
	#		if coverage > 1.0:
	#			print(pn, mydict[t][pn])
	#			coverage = 1.0
		coverage = mydict[t]/total
		lst= [chr, t, str(mydict[t]), str(coverage)]
		output.write('\t'.join(lst) + '\n')



## main
type_to_path = {}
exon_to_path= {}
tf_to_path= {}
total = 0
chr = ''
for line in open(sys.argv[1]):
	if line.startswith('#'):
		continue

	chr = line.split('\t')[0]

	total += 1

	identify_effect(line, type_to_path)
	identify_exons(line, exon_to_path)


print('total', total)

types = loop_dictionary(type_to_path, total)

#exons = loop_dictionary(exon_to_path)
#print(exons)
#print(list(set(exon_to_path.keys())))
