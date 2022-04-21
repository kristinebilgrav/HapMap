import sys
import json
import database
import time
import numpy as np
from sklearn.cluster import KMeans
import os

# distutils: language=c++

os.system('source /home/kbilgrav/anaconda3/bin/activate')

def clustering(id_list):
	cdef dict labels = {}
	cdef list var_list = []
	cdef str id
	cdef str q
	cdef list varq
	cdef list alist
	cdef int n_clusters
	cdef dict label_to_cluster

	db = database.DB('/proj/nobackup/sens2017106/kristine/hapmap/hapmap.db')
	for id in id_list:
		q = ''' SELECT COUNT(*) FROM cleanblock WHERE id ='{}' AND chr='{}' UNION ALL SELECT COUNT(*) FROM cleanblock WHERE id ='{}' AND chr='{}';  '''.format(id, 'Y', id, 'X')
		varq = db.get_item(q) #tuple with number of variants on Y and X
		if id not in labels: 
			labels[id] = [varq[0][0], varq[1][0]]
		alist = [varq[0][0], varq[1][0] ]
		var_list.append( alist)

	vars = np.array(var_list)

	n_clusters = 2

	kmeans = KMeans(n_clusters = n_clusters, init = "k-means++", n_init = 40, max_iter = 62, random_state = 42)
	kmeans.fit(vars)
	cluster = kmeans.labels_

	label_to_cluster ={} 
	for i in labels: 
		item_number = list(labels.keys()).index(i)
		cluster_id = cluster[item_number]
		label_to_cluster[i] = cluster_id

		#if male 0: treat X as one PS and Y as one (ignore GT)

		#if female 1: continue as normal on X, ignore Y

	return label_to_cluster

def create_kmers(chr, qres, dict):
	for res in qres:
		pos = res[1].split(';')
		alt = res[2].split(';')

		my_snps = {}
		for s in range(0, len(pos)):
			my_snps[int(pos[s])] = alt[s]

		sorted_snps = sorted(my_snps.items())
		for i in range(0, len(sorted_snps) -2):

			j = i+1
			k = j+1

			kmer_a="{} {} {} {} {} {}".format(chr, str(sorted_snps[i][0]), sorted_snps[i][1], chr ,str(sorted_snps[j][0]), sorted_snps[j][1])
			kmer_b="{} {} {} {} {} {}".format(chr, str(sorted_snps[j][0]), sorted_snps[j][1], chr , str(sorted_snps[k][0]), sorted_snps[k][1])
			if kmer_a not in dict[chr]:
				dict[chr][kmer_a] = {}
	
			if kmer_b not in dict[chr][kmer_a]:
				dict[chr][kmer_a][kmer_b] = 0

			dict[chr][kmer_a][kmer_b] +=1			
	
#connect db
def main(str chr):
	
	db = database.DB('/proj/nobackup/sens2017106/kristine/hapmap/hapmap.db')

	start = time.time()
	cdef str idq = '''SELECT DISTINCT id FROM cleanblock ;  '''

	cdef list ids= []
	cdef tuple id_tuple

	for id_tuple in db.get_item(idq):
		ids.append(id_tuple[0])

	cdef dict master_dict = {}
	cdef list kcon_time = []

	if chr not in master_dict:
		master_dict[chr] = {}

	cdef list query2 = []
	cdef list loop = []

	cdef str GT

	cdef str kmer_a
	cdef str kmer_b

	cdef int i
	cdef int j
	cdef int k

	cdef list pos
	cdef list alt
	cdef str id

	if chr == 'Y' or chr == 'X':
		genders = clustering(ids)
	
	for id in ids:
		print(id)

		if chr == 'Y' and genders[id] == 0 or chr =='X' and genders[id] == 0: #male
			print(chr, 'male')
			#order by asc not working
			q = '''SELECT chr, GROUP_CONCAT(pos, ';'), GROUP_CONCAT(alt, ';') FROM cleanblock WHERE chr = '{}' AND  id = '{}' GROUP BY PS HAVING COUNT(pos) >=3 ORDER BY GROUP_CONCAT(pos) ASC; '''.format( chr, id)
			myq = db.get_item(q)

			create_kmers(chr, myq, master_dict)

		elif chr =='Y' and genders[id] == 1:
			print('female', chr, 'skip')
			continue

		else:
			print(chr, id)
			for GT in ["1|0","0|1" ]:
					
				q = '''SELECT chr, GROUP_CONCAT(pos, ';'), GROUP_CONCAT(alt, ';') FROM cleanblock WHERE (GT= '{}' OR GT = '1|1') AND chr = '{}' AND  id = '{}' GROUP BY PS HAVING COUNT(pos) >=3 ORDER BY GROUP_CONCAT(pos) ASC;  '''.format(GT , chr, id)
				myq = db.get_item(q) #tuple

				create_kmers(chr, myq, master_dict)



	f = open(chr + '_graph.json', 'w')
	json.dump(master_dict, f)
	f.close()
	quit()
