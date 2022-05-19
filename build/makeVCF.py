import sys
import pysam
import database

#connectedA


def findAF(chr, pos, alt):
	q = '''SELECT COUNT(DISTINCT id) FROM cleanblock WHERE chr = '{}' AND pos = {} AND alt ='{}';  '''.format(chr, pos, alt)
	res = db.get_item(q)
	return res[0][0]

def find_ref(chr, pos, file):
	res = pysam.faidx(file, '{}:{}-{}'.format(chr, pos, pos))
	return res.split()[-1]

db = database.DB('hapmap.db')

#total individuals 
#idq = '''SELECT COUNT(DISTINCT id) FROM cleanblock; '''
#ids = db.get_item(idq)[0][0]
ids = 62


#read connection file
old_to_new = {} #each pathnumber leads to new path
for pth in open(sys.argv[2]):
	if pth.startswith('new_pathnumber'):
		continue
	newpath = int(pth.split('\t')[0])
	conpath = pth.rstrip('\n').split('\t')[1].replace(',', '-')

	oldnumbers = conpath.split('-')
	for old in oldnumbers:
		if old not in old_to_new:
			old_to_new[old] = []
		
		if conpath not in old_to_new[old]:
			old_to_new[old].append(conpath)

count = 0
altdict = {}
print('reading graph')
for line in open(sys.argv[1]):
	if line.startswith('pathnumber'):
		continue

	count += 1 
	if count % 2 == 0:
		line = line.split('\t')
		pathn = line[0]
		totalkmers = len(line[1:])
		for kmer in line[1:]:
			thiskmer = line[1:].index(kmer)+1

			alt1 = ' '.join(kmer.split()[0:3])
			alt2 =' '.join(kmer.split()[3:])
			if alt1 not in altdict:
				altdict[alt1] = {}
			if alt2 not in altdict:
				altdict[alt2] = {}
			
			altdict[alt1][pathn] = []
			altdict[alt1][pathn].append(str(thiskmer)+'/'+str(totalkmers))
			chr1=kmer.split()[0:3][0]
			pos1 = kmer.split()[0:3][1]
			var1 = kmer.split()[0:3][2]
			AF = findAF(chr1, pos1, var1) /ids
			altdict[alt1][pathn].append(AF)
			ref = find_ref(chr1, pos1, sys.argv[4])
			altdict[alt1][pathn].append(ref)

			altdict[alt2][pathn] = []
			altdict[alt2][pathn].append(str(thiskmer)+'/'+str(totalkmers))
			chr2 = kmer.split()[3:][0]
			pos2 = kmer.split()[3:][1]
			var2 = kmer.split()[3:][2]
			AF2 = findAF(chr2, pos2, var2) /ids
			altdict[alt2][pathn].append(AF2)
			ref2 = find_ref(chr2, pos2, sys.argv[4])
			altdict[alt2][pathn].append(ref2)

output = open(sys.argv[3], 'w')
print('writing vcf')
aaline = '''##fileformat=VCFv4.1'''
output.write(aaline + '\n')
aline = '##source=happyHAP'
output.write(aline + '\n')
bline = '''##INFO=<ID=PATH=,Number=.,Type=String,Description="Pathnumber, kmer/total kmers,allele frequency and connecting paths Format: PATHNUMBER,KMER/TOTAL,AF,PATHCONNECTIONS">'''
output.write(bline + '\n')
header = ['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO']
output.write('\t'.join(header) + '\n')
for var in altdict:
	chr = var.split()[0]
	pos = var.split()[1]
	alt = var.split()[2]
	ref = 'N'
	allinfo =[]
	for pth in altdict[var]:
		if ref != 'N' and ref != altdict[var][pth][2]:
			print('ref change', ref, altdict[var][pth][2])
		ref = altdict[var][pth][2]
		connections = ','.join(old_to_new[pth])
		info= ['PATH='+pth, altdict[var][pth][0], str(altdict[var][pth][1]), connections ]
		info= ','.join(info)
		allinfo.append(info)

	allinfo = ';'.join(allinfo)
	line = [chr, str(pos), '.', ref, alt, '.', '.', allinfo ]
	output.write('\t'.join(line) + '\n')


