import sys
import numpy as np
import database

#connect db
db = database.DB('hapmap.db')


#query ids and related PS with > 3 variants
#idq = ''' SELECT DISTINCT id, PS FROM haploblock; '''
idq = ''' SELECT id, PS, COUNT(pos) FROM haploblock GROUP BY id, PS HAVING COUNT(pos) >=3; '''
idquery = db.get_item(idq)

chr_of_interest = list(range(1, 23)) 
chr_of_interest.append('X')
chr_of_interest.append('Y')

master_graph = {}

id_graph ={}
id_kmers= {}
for res in idquery:
	#print(res)
	id = res[0]
	if id not in id_graph:
		id_graph[id] = {}

	PS = res[1]

	print(id, PS)

	#query the PS 
	thePS = '''SELECT chr, pos, alt FROM haploblock WHERE id = '{}' AND PS='{}' ; '''.format(id, PS)
	PSquery = db.query(thePS)

	#create kmers
	for  i in range( 0, len(PSquery) -1):
		
		k0 = PSquery[i]
		k1 = PSquery[i+1]


		try:
			chr = int(k0[0])

		except:
			chr = k0[0]

		if chr not in chr_of_interest:
			print('chr not in list', chr)
			continue

		if chr not in id_graph[id]:
			id_graph[id][chr] = {}

		pos1 = k0[1]
		pos2 = k1[1]

		alt1 = k0[2]
		alt2 = k1[2]

		kmer = (chr, pos1, alt1, chr, pos2, alt2)

		#search for ids with same kmer
		k0q = '''SELECT DISTINCT id FROM haploblock WHERE chr = '{}' AND pos = '{}' AND alt = '{}' '''.format(chr, pos1, alt1) #cannot combine two using UNION
		k0query = db.get_item(k0q)
		k1q = '''SELECT DISTINCT id FROM haploblock WHERE chr = '{}' AND pos = '{}' AND alt = '{}' '''.format(chr, pos2, alt2) 
		k1query = db.get_item(k1q)

		k0ids = np.array([i[0] for i in k0query])
		k1ids = np.array([id[0] for id in k1query])
		matching= np.intersect1d(k0ids, k1ids)

		#add number of matches to graph
		if len(matching) > 1:

			#append kmer/node 
			if kmer not in id_graph[id][chr]:
				id_graph[id][chr][kmer] = {}
				id_kmers[kmer] = matching
	
			#connect kmers/edges
			for k in id_graph[id][chr]: 
				if k0[1] in k and k0[2] in k and k != kmer:
					#match ids with last kmer
					stillmatching = np.intersect1d(id_kmers[k], id_kmers[kmer])
					if len(stillmatching) > 1:
						id_graph[id][chr][k][kmer] = 0
						id_graph[id][chr][k][kmer] += len(stillmatching)


		else:
			print('no matches on', kmer)


		print(id_graph)
#alt:
#chr_of_interest = np.arange(1, 23, 1))

