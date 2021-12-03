import sys
import numpy as np
import database

#connect db
db = database.DB('hapmap.db')


#query ids
#idq = ''' SELECT DISTINCT id, PS FROM haploblock; '''
idq = ''' SELECT id, PS, COUNT(*) FROM haploblock GROUP BY id; '''
idquery = db.get_item(idq)
print(idquery)
quit()

chr_of_interest = list(range(1, 23)) 
chr_of_interest.append('X')
chr_of_interest.append('Y')

master_graph = {}

for res in idquery:
	id = id[0]
	id_graph = {}

	#query for unique PS
	uniquePS = '''SELECT DISTINCT PS FROM haploblock WHERE id = '{}'; '''.format(id)
	uniquePSquery = db.query(uniquePS)

	print(uniquePSquery)
	quit()

	#query db for all PS with more than 3 variants
#	PSq = '''SELECT chr, group_concat(pos ), group_concat(alt), PS FROM haploblock WHERE id = '{}' AND chr = '3' GROUP BY PS  ; '''.format(id) 
	PSq = '''SELECT chr, pos, alt, PS FROM haploblock WHERE id = '{}' AND PS = '{}'; '''.format(id, PS)
	PSquery = db.get_item(PSq)

	print(PSquery)
	#select those with > 3 variants
	for ps in PSquery:
		try:
			chr = int(ps[0])

		except:
			chr = ps[0]

		print('a ps', ps)

		if chr not in chr_of_interest:
			print('chr not in list', chr)
			continue

		positions = ps[1].split(',')

		if len(positions) < 3:
			continue
		else:
			#kmer creation
			for i in range(0, len(positions) - 1):
				alterations = ps[2].split(',')

				# k1
				nextpos = i + 1
				pos1 = positions[i]
				pos2 = positions[nextpos]
				alt1 = alterations[i]
				alt2 = alterations[nextpos]

				kmer = [chr, pos1, alt1, chr, pos2, alt2]
				k0 = kmer[0:3]
				k1 = kmer[3:]

				#search for ids with same kmer
				kq = '''SELECT id FROM haploblock WHERE (chr = '{}' AND pos = '{}' AND alt = '{}') AND (chr = '{}' AND pos = '{}' AND alt = '{}'); '''.format(chr, pos1, alt1, chr, pos2, alt2)
				kquery = db.query(kq)
				#print('kq', kq)
				#print('kquery', kquery)

				if len(kquery) > 0:
					print('kq', kq)
					print(kquery)
					quit()
					#add number of matches to graph
					id_graph[kmer] 
				
					#append kmer/node 
					if kmer not in id_graph:
						id_graph[kmer] = {}
	
					#connect kmers/edges
					for k in id_graph: 
						if k0 in k and k != kmer:
							id_graph[k][kmer] = 0
						id_graph[k][kmer] += len(kquery)

	print(id_graph)
#alt:
#chr_of_interest = np.arange(1, 23, 1))

